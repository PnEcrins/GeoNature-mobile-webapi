from __future__ import with_statement

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import simplejson
from django.utils.datastructures import SortedDict
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.servers.basehttp import FileWrapper

from faune.utils import sync_db, query_db, commit_transaction, check_connection

from easydict import EasyDict

from shapely.wkt import loads
from geojson import dumps

import sqlite3 as lite
from shutil import copyfile

from tempfile import NamedTemporaryFile

import time
import datetime
import os
import tempfile


@csrf_exempt
def import_data(request):
    """
    Import data from json to DataBase
    """

    response_content = {}

    params = request.POST
    if params:
        data = params['data']
    else:
        response_content.append({
            'status': _("No POST param given")
        })
        response = HttpResponse()
        simplejson.dump(response_content, response,
                    ensure_ascii=False, separators=(',', ':'))
        return response

    res, response = check_token(request)
    if not res:
        return response

    json_data = simplejson.loads(data)

    d = EasyDict(json_data)

    bad_id = False
    # Check if ID are unique
    count_string = "SELECT count(*) FROM %s WHERE %s='%s'" % (settings.TABLE_SHEET, settings.FAUNE_TABLE_INFOS.get(settings.TABLE_SHEET).get('id_col'), d.id)
    cursor = query_db(count_string)
    row = cursor.fetchone()
    if row :
        datarow = zip([column[0] for column in cursor.description], row)
        val = datarow[0][1]
        if val == 1:
            bad_id = True
            response_content.update({
                'status_code': _("1"),
                'status_message': _("Existing ID in database (%s) (%s)") % (settings.TABLE_SHEET, d.id)
            })
    for taxon in d.taxons:
        count_string = "SELECT count(*) FROM %s WHERE %s='%s'" % (settings.TABLE_STATEMENT, settings.FAUNE_TABLE_INFOS.get(settings.TABLE_STATEMENT).get('id_col'), taxon.id)
        cursor = query_db(count_string)
        row = cursor.fetchone()
        if row :
            datarow = zip([column[0] for column in cursor.description], row)
            val = datarow[0][1]
            if val == 1:
                bad_id = True
                response_content.update({
                    'status_code': _("1"),
                    'status_message': _("Existing ID in database (%s) (%s)") % (settings.TABLE_STATEMENT, taxon.id)
                })
    
    if not bad_id: 
        try:
            objects = []
            new_feature = {}
            json_to_db = settings.FAUNE_TABLE_INFOS.get(settings.TABLE_SHEET).get('json_to_db_columns')
            
            # Insert into TABLE_SHEET
            new_feature[settings.FAUNE_TABLE_INFOS.get(settings.TABLE_SHEET).get('id_col')] = d.id
            new_feature['table_name'] = settings.TABLE_SHEET
            new_feature[json_to_db.get('dateobs')] = d.dateobs
            new_feature[json_to_db.get('initial_input')] = d.initial_input
            new_feature['supprime'] = 'False'
            new_feature['id_organisme'] = settings.FAUNA_ID_ORGANISM
            if json_data['input_type'] == 'fauna':
                new_feature['id_protocole'] = settings.FAUNA_ID_PROTOCOL
                new_feature['id_lot'] = settings.FAUNA_ID_LOT
            else:
                new_feature['id_protocole'] = settings.MORTALITY_ID_PROTOCOL
                new_feature['id_lot'] = settings.MORTALITY_ID_LOT

            # we need to transform into 2154
            new_feature[json_to_db.get('geometry')] = "transform(ST_GeomFromText('POINT(%s %s)', 4326),2154)" % (d.geolocation.longitude, d.geolocation.latitude)
            new_feature[json_to_db.get('accuracy')] = d.geolocation.accuracy
            objects.append(new_feature)
            cursor = sync_db(objects)

            # Insert into TABLE_STATEMENT
            statement_ids = []
            for taxon in d.taxons:
                statement_ids.append(taxon.id)
                objects = []
                new_feature = {}
                json_to_db = settings.FAUNE_TABLE_INFOS.get(settings.TABLE_STATEMENT).get('json_to_db_columns')
                new_feature['table_name'] = settings.TABLE_STATEMENT
                new_feature['supprime'] = 'False'
                new_feature[settings.FAUNE_TABLE_INFOS.get(settings.TABLE_STATEMENT).get('id_col')] = taxon.id
                new_feature[settings.FAUNE_TABLE_INFOS.get(settings.TABLE_SHEET).get('id_col')] = d.id
                new_feature[json_to_db.get('id')] = taxon.id_taxon
                new_feature[json_to_db.get('name_entered')] = taxon.name_entered
                if json_data['input_type'] == 'fauna':
                    new_feature[json_to_db.get('adult_male')] = taxon.counting.adult_male
                    new_feature[json_to_db.get('adult_female')] = taxon.counting.adult_female
                    new_feature[json_to_db.get('adult')] = taxon.counting.adult
                    new_feature[json_to_db.get('not_adult')] = taxon.counting.not_adult
                    new_feature[json_to_db.get('young')] = taxon.counting.young
                    new_feature[json_to_db.get('yearling')] = taxon.counting.yearling
                    new_feature[json_to_db.get('sex_age_unspecified')] = taxon.counting.sex_age_unspecified
                    new_feature[json_to_db.get('criterion')] = taxon.observation.criterion
                else:
                    new_feature[json_to_db.get('adult_male')] = taxon.mortality.adult_male
                    new_feature[json_to_db.get('adult_female')] = taxon.mortality.adult_female
                    new_feature[json_to_db.get('adult')] = taxon.mortality.adult
                    new_feature[json_to_db.get('not_adult')] = taxon.mortality.not_adult
                    new_feature[json_to_db.get('young')] = taxon.mortality.young
                    new_feature[json_to_db.get('yearling')] = taxon.mortality.yearling
                    new_feature[json_to_db.get('sex_age_unspecified')] = taxon.mortality.sex_age_unspecified
                    new_feature[json_to_db.get('sample')] = taxon.mortality.sample
                    new_feature[json_to_db.get('criterion')] = taxon.observation.criterion

                new_feature[json_to_db.get('comment')] = taxon.comment

                objects.append(new_feature)
                cursor = sync_db(objects)

            # Insert into TABLE_SHEET_ROLE (multiple observers enable)
            for observer in d.observers_id:
                objects = []
                new_feature = {}
                new_feature['table_name'] = settings.TABLE_SHEET_ROLE
                new_feature['id_cf'] = d.id
                new_feature['id_role'] = observer
                objects.append(new_feature)
                sync_db(objects)

            # Commit transaction
            commit_transaction()

            response_content.update({
                'status_code': _("0"),
                'status_message': "id_sheet: %s, ids_statements: %s" % (d.id, ','.join(map(str, statement_ids)))
            })
        #except Exception as e:
        except Exception, e:
            #  Insert rejected JSON into synchro_table (text format)
            archive_bad_data(data, json_data)

            response_content.update({
                'status_code': _("1"),
                'status_message': _("Bad json or data (%d)") % id_failed
            })
    else:
        archive_bad_data(data, json_data)

    response = HttpResponse()
    simplejson.dump(response_content, response,
                ensure_ascii=False, separators=(',', ':'))

    return response

def archive_bad_data(data, json_data):
    #  Insert rejected JSON into synchro_table (text format)
    now = datetime.datetime.now()
    objects = []
    new_feature = {}
    if json_data['input_type'] == 'fauna':
        new_feature['table_name'] = settings.TABLE_FAILED_JSON_FAUNA
    else:
        new_feature['table_name'] = settings.TABLE_FAILED_JSON_MORTALITY
    new_feature['date_import'] = "%d-%d-%d %d:%d:%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    new_feature['json'] = data
    objects.append(new_feature)
    cursor = sync_db(objects)
    id_failed = cursor.fetchone()[0]

    # Commit transaction
    commit_transaction()
    
    
    
@csrf_exempt
def export_sqlite(request):
    """
    Export all data in sqlite format
    """
    response_content = []
    res, response = check_token(request)
    if not res:
        return response
    
    # Create the .db file
    output = None
    src = "%s" % (settings.FAUNE_MOBILE_SQLITE_SAMPLE)
    try:
        with NamedTemporaryFile('w', suffix='.db') as f:
            output = f.name
            handle = open(src, 'r')
            f.write(handle.read())
            f.flush()

            # Create tables inside the DB
            con = lite.connect(output)
            #with con:
            cur = con.cursor()
            for create_string in settings.FAUNE_MOBILE_SQLITE_CREATE_QUERY:
                cur.execute(create_string)

            # Extra SQL to execute on database
            for insert_string in settings.FAUNE_MOBILE_SQLITE_EXTRA_SQL:
                cur.execute(insert_string)
            
            # Fill data
            tabTab = []
            tabTab.append(settings.TABLE_USER)
            tabTab.append(settings.TABLE_TAXA_UNITY)
            tabTab.append(settings.TABLE_TAXA)
            tabTab.append(settings.TABLE_CRITERION)
            for pg_table_name in tabTab:
                li_table_name = settings.FAUNE_TABLE_INFOS.get(pg_table_name).get('sqlite_name')
                where_string = settings.FAUNE_TABLE_INFOS.get(pg_table_name).get('where_string')
                if where_string != None:
                    where_string = "WHERE %s" % (where_string)
                else:
                    where_string = ""
                response_content = get_data(request, pg_table_name, where_string, False)
                for obj in response_content[settings.FAUNE_TABLE_INFOS.get(pg_table_name).get('json_name')]:
                    colTab = []
                    valTab = []
                    for key in obj:
                        colTab.append(key)
                        valTab.append(unicode(obj[key]).replace("'", "''"))
                    insert_string = "INSERT INTO %s (%s) values (%s)" % \
                                        (li_table_name,
                                        ",".join(colTab),
                                        "'" + "','".join(map(unicode, valTab)) + "'"
                                        )
                    cur.execute(insert_string)
            con.commit()
            con.close()
            
            wrapper = FileWrapper(file(output))
            response = HttpResponse(wrapper, content_type='application/x-sqlite3')
            response['Content-Length'] = os.path.getsize(output)
            response['Content-Disposition'] = 'attachment; filename=data.db'
    finally:
        pass
        #if output:
        #    os.unlink(output)

    return response


def export_taxon(request):
    """170
    Export taxon table from DataBase to mobile
    """
    return export_data(request, settings.TABLE_TAXA)


def export_family(request):
    """
    Export family table from DataBase to mobile
    """
    return export_data(request, settings.TABLE_FAMILY)


def export_unity(request):
    """
    Export unity table from DataBase to mobile
    """
    return export_data(request, settings.TABLE_UNITY)


def export_taxon_unity(request):
    """
    Export crossed taxon / unity table from DataBase to mobile
    """
    return export_data(request, settings.TABLE_TAXA_UNITY)


def export_criterion(request):
    """
    Export criterion table from DataBase to mobile
    """
    return export_data(request, settings.TABLE_CRITERION)


def export_user(request):
    """
    Export user table from DataBase to mobile
    """
    return export_data(request, settings.TABLE_USER)


def export_classes(request):
    """
    Export classes table from DataBase to mobile
    """
    return export_data(request, settings.TABLE_CLASSES)

@csrf_exempt
def export_unity_geojson(request):
    """
    Export unity table from DataBase as geojson format
    """

    response_content = []
    res, response = check_token(request)
    if not res:
        return response

    # Get infos
    table_name = settings.TABLE_UNITY_GEOJSON
    response_objects = []
    json_table_name = settings.FAUNE_TABLE_INFOS_GEOJSON.get(table_name).get('json_name')
    response_content = {"type": "FeatureCollection", "features": []}

    get_data_object_geojson(response_objects, table_name)

    response_content["features"] = response_objects

    response = HttpResponse()
    simplejson.dump(response_content, response,
                ensure_ascii=False, separators=(',', ':'))

    # Create the .geojson file
    output = None
    s = simplejson.dumps(response_content, ensure_ascii=True, encoding='utf-8')
    try:
        #with NamedTemporaryFile('w', delete=False, suffix='.geojson') as f:
        with tempfile.TemporaryFile('w', suffix='.geojson') as f:
            output = f.name
            s = s.replace(' ', '')
            f.write(s + "\n")
            f.flush()
            wrapper = FileWrapper(file(output))
            response = HttpResponse(wrapper, content_type='application/json')
            response['Content-Length'] = os.path.getsize(output)
            response['Content-Disposition'] = 'attachment; filename=unity.geojson'
    finally:
        if output:
            os.unlink(output)
    
    return response

@csrf_exempt
def export_unity_polygons(request):
    """
    Export unity table from DataBase as text format
    One id,polygon per line
    """

    res, response = check_token(request)
    if not res:
        return response

    # Get infos
    table_name = settings.TABLE_UNITY_GEOJSON
    response_objects = []

    get_data_object_txt(response_objects, table_name)

    # Create the .txt file
    output = None
    export = ""
    try:
        with tempfile.TemporaryFile('w', suffix='.wkt') as f:
            output = f.name
            
            for polygon in response_objects:
                export = "%s%s\n" % (export, polygon)
                
            wrapper = FileWrapper(f)
            response = HttpResponse(export, content_type='application/txt')
            response['Content-Length'] = len(export)
            response['Content-Disposition'] = 'attachment; filename=unity.wkt'
    finally:
        pass
        #if output:
        #    os.unlink(output)
    
    return response
    

def export_data(request, table_name):
    """
    Export table_name data from DataBase to JSON
    """
    response_content = get_data(request, table_name, None, False)

    response = HttpResponse()
    simplejson.dump(response_content, response,
                ensure_ascii=False, separators=(',', ':'))

    return response


def get_data(request, table_name, where_string, testing):
    """
    Get table_name data from DataBase to object
    Param testing is for testing Data
    """
    response_content = []
    res, response = check_token(request)
    if not res:
        return response
    
    # Get infos
    response_objects = []
    json_table_name = settings.FAUNE_TABLE_INFOS.get(table_name).get('json_name')
    response_content = {json_table_name: []}

    get_data_object(response_objects, table_name, where_string, testing)

    response_content[json_table_name] = response_objects

    return response_content


def check_token(request):
    """
    Check the validity of the token
    """
    if request.method == 'POST':
        if request.POST['token']:
            if request.POST['token'] == settings.TOKEN:
                return True, None
    
    response_content = []
    response_content.append({
        'status': _("You're not allowed to retreive information from this webservice")
    })
    response = HttpResponse()
    simplejson.dump(response_content, response,
                ensure_ascii=False, separators=(',', ':'))

    return False, response


def get_data_object(response_content, table_name, where_string, testing):
    """
    Perform a SELECT on the DB to retreive infos on associated object
    Param: table_name : name of the table
    """
    test_string = ""
    if testing:
        test_string = " LIMIT 1"
    select_columns = settings.FAUNE_TABLE_INFOS.get(table_name).get('select_col')
    select_string = "SELECT %s FROM %s %s %s" \
                    % (select_columns, table_name, where_string, test_string)

    cursor = query_db(select_string)
    for row in cursor.fetchall():
        data = zip([column[0] for column in cursor.description], row)
        feat_dict = SortedDict({})
        for attr in data:
            key = attr[0]
            val = attr[1]
            if type(val).__name__ == "date":
                val = val.strftime("%d/%m/%Y")

            new_key = settings.FAUNE_TABLE_INFOS.get(table_name).get('db_to_json_columns').get(key)

            feat_dict[new_key] = val

        response_content.append(feat_dict)


def get_data_object_geojson(response_content, table_name):
    """
    Perform a SELECT on the DB to retreive infos on associated object, geojson format
    Param: table_name : name of the table
    """

    select_columns = settings.FAUNE_TABLE_INFOS_GEOJSON.get(table_name).get('select_col')
    select_string = "SELECT %s FROM %s" \
                    % (select_columns, table_name)

    cursor = query_db(select_string)
    i = 0  # feature index
    for row in cursor.fetchall():
        data = zip([column[0] for column in cursor.description], row)
        feat_dict = SortedDict({"type": "Feature", "id": i})
        properties_dict = SortedDict({})
        for attr in data:
            key = attr[0]
            val = attr[1]
            if type(val).__name__ == "date":
                val = val.strftime("%d/%m/%Y")

            if key == "geom":
                geom = loads(val)
                geometry_dict = dumps(geom)
            else:
                new_key = settings.FAUNE_TABLE_INFOS_GEOJSON.get(table_name).get('db_to_json_columns').get(key)
                properties_dict[new_key] = val

        feat_dict["properties"] = properties_dict
        feat_dict["geometry"] = simplejson.loads(geometry_dict)

        i = i + 1
        response_content.append(feat_dict)

        
def get_data_object_txt(response_content, table_name):
    """
    Perform a SELECT on the DB to retreive infos on associated object, txt format
    Param: table_name : name of the table
    """

    select_columns = settings.FAUNE_TABLE_INFOS_GEOJSON.get(table_name).get('select_col')
    select_string = "SELECT %s FROM %s" \
                    % (select_columns, table_name)

    cursor = query_db(select_string)
    for row in cursor.fetchall():
        data = zip([column[0] for column in cursor.description], row)
        stringGeometry = ""
        stringKey = ""
        for attr in data:
            key = attr[0]
            val = attr[1]

            if key == "geom":
                stringGeometry = val
            else:
                stringKey = val

        response_content.append("%s,%s" % (stringKey, stringGeometry))
        
@csrf_exempt
def check_status(request):
    """
    Check if database active and views are available
    """
    response_content = {}
    res, response = check_token(request)
    if not res:
        return response

    # check DB connection
    res_connection = check_connection();
    
    # check if views are availables
    res_views = True
    try:
        tabTab = []
        tabTab.append(settings.TABLE_USER)
        tabTab.append(settings.TABLE_TAXA_UNITY)
        tabTab.append(settings.TABLE_TAXA)
        tabTab.append(settings.TABLE_CRITERION)
        for pg_table_name in tabTab:
            li_table_name = settings.FAUNE_TABLE_INFOS.get(pg_table_name).get('sqlite_name')
            test_return = get_data(request, pg_table_name, None, True)
    except:
        res_views = False


    response_content.update({
        'status_code': _("0"),
        'status_message': "DB connection %d, Views available %d" % (res_connection, res_views)
        #'DB connection': res_connection,
        #'Views available': res_views
    })
    response = HttpResponse()
    simplejson.dump(response_content, response,
                ensure_ascii=False, separators=(',', ':'))
    return response

@csrf_exempt
def soft_version(request):
    """
    Return the version of the mobile soft (JSON)  by reading a json config file
    """
    response_content = {'apps': []}
    res, response = check_token(request)
    if not res:
        return response

    # read the version file
    version_file = "%sversion.json" % (settings.FAUNE_MOBILE_SOFT_PATH)
    
    try:
        json_data = open(version_file)   
        version_data = simplejson.load(json_data)
        json_data.close()
        
        for apps in version_data['apps']:
            response_content['apps'].append({
                "package": apps["package"],
                "versionCode": apps["versionCode"],
                "versionName": apps["versionName"],
                "apkName": apps["apkName"],
            })        
    except:
        response_content.update({
            'status_code': _("1"),
            'status_message': "Version file is not available"
        })
    
    response = HttpResponse()
    simplejson.dump(response_content, response,
                ensure_ascii=False, separators=(',', ':'))
    return response

    
@csrf_exempt
def soft_download(request, apk_name):
    """
    Return a downloadable file of the mobile soft
    """
    response_content = {}
    res, response = check_token(request)
    if not res:
        return response

    file_path = "%s%s" %  (settings.FAUNE_MOBILE_SOFT_PATH, apk_name)
    print file_path
    try:
        wrapper = FileWrapper(file(file_path))
        response = HttpResponse(wrapper, content_type='text/plain')
        response['Content-Length'] = os.path.getsize(file_path)
        response['Content-Disposition'] = 'attachment; filename=%s' % (apk_name)
    except :
        response_content.update({
            'status_code': _("1"),
            'status_message': "APK file is not available (%s)" % (apk_name)
        })
        response = HttpResponse()
        simplejson.dump(response_content, response,
                    ensure_ascii=False, separators=(',', ':'))
        return response
    
    return response
            