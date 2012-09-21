from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import simplejson
from django.utils.datastructures import SortedDict
from django.conf import settings
from django.utils.translation import ugettext as _

from faune.utils import sync_db, query_db, commit_transaction

import json
import time
import datetime

@csrf_exempt
def import_data(request):
    """
    Import data from json to DataBase
    """

    response_content = []
        
    params = request.POST
    if params:
        data = params['data']
    else:
        response_content.append({
            'status' : _("No POST param given")
        })
        response = HttpResponse()
        simplejson.dump(response_content, response,
                    ensure_ascii=False, separators=(',', ':'))                    
        return response
    
    if not check_token(request):
        response_content.append({
            'status' : _("You're not allowed to use this webservice")
        })
        response = HttpResponse()
        simplejson.dump(response_content, response,
                    ensure_ascii=False, separators=(',', ':'))                    
        return response

    json_data = simplejson.loads(data)
        
    try:
        # Insert into TABLE_SHEET
        objects = []
        new_feature = {}
        json_to_db = settings.FAUNE_TABLE_INFOS.get(settings.TABLE_SHEET).get('json_to_db_columns')
        new_feature[settings.FAUNE_TABLE_INFOS.get(settings.TABLE_SHEET).get('id_col')] = json_data['id']
        new_feature['table_name'] = settings.TABLE_SHEET
        new_feature[json_to_db.get('dateobs')] = json_data['dateobs']
        new_feature[json_to_db.get('initial_input')] = json_data['initial_input']
        new_feature['supprime'] = 'False'
        new_feature['id_organisme']= 2  # (parc national des ecrins = fk de utilisateurs.bib_organismes)
        if json_data['input_type'] == 'fauna':
            new_feature['id_protocole']= 140 # faune TODO: recuperer ces ID en dynamique, 142 pour mortalite
            new_feature['id_lot'] = 4 # faune
        else:
            new_feature['id_protocole']= 142 # mortality
            new_feature['id_lot'] = 15 # mortality

        # we need to transform into 2154
        new_feature[json_to_db.get('geometry')] = "transform(ST_GeomFromText('POINT(%s %s)', 4326),2154)" % (json_data['geolocation']['longitude'], json_data['geolocation']['latitude'])
        new_feature[json_to_db.get('accuracy')] = json_data['geolocation']['accuracy']
        new_feature[json_to_db.get('altitude')] = json_data['geolocation']['altitude']
        objects.append(new_feature)
        cursor = sync_db(objects)
        #id_fiche = cursor.fetchone()[0]

        # Insert into TABLE_STATEMENT
        objects = []
        new_feature = {}
        json_to_db = settings.FAUNE_TABLE_INFOS.get(settings.TABLE_STATEMENT).get('json_to_db_columns')
        new_feature['table_name'] = settings.TABLE_STATEMENT
        new_feature['supprime'] = 'False'
        new_feature[settings.FAUNE_TABLE_INFOS.get(settings.TABLE_STATEMENT).get('id_col')] = json_data['id']
        new_feature[settings.FAUNE_TABLE_INFOS.get(settings.TABLE_SHEET).get('id_col')] = json_data['id']
        new_feature[json_to_db.get('id')] = json_data['taxon']['id']
        new_feature[json_to_db.get('name_entered')] = json_data['taxon']['name_entered']
        if json_data['input_type'] == 'fauna':
            new_feature[json_to_db.get('adult_male')] = json_data['taxon']['counting']['adult_male']
            new_feature[json_to_db.get('adult_female')] = json_data['taxon']['counting']['adult_female']
            new_feature[json_to_db.get('adult')] = json_data['taxon']['counting']['adult']
            new_feature[json_to_db.get('not_adult')] = json_data['taxon']['counting']['not_adult']
            new_feature[json_to_db.get('young')] = json_data['taxon']['counting']['young']
            new_feature[json_to_db.get('yearling')] = json_data['taxon']['counting']['yearling']
            new_feature[json_to_db.get('sex_age_unspecified')] = json_data['taxon']['counting']['sex_age_unspecified']
            new_feature[json_to_db.get('criterion')] = json_data['taxon']['observation']['criterion']
        else :
            new_feature[json_to_db.get('adult_male')] = json_data['taxon']['mortality']['adult_male']
            new_feature[json_to_db.get('adult_female')] = json_data['taxon']['mortality']['adult_female']
            new_feature[json_to_db.get('adult')] = json_data['taxon']['mortality']['adult']
            new_feature[json_to_db.get('not_adult')] = json_data['taxon']['mortality']['not_adult']
            new_feature[json_to_db.get('young')] = json_data['taxon']['mortality']['young']
            new_feature[json_to_db.get('yearling')] = json_data['taxon']['mortality']['yearling']
            new_feature[json_to_db.get('sex_age_unspecified')] = json_data['taxon']['mortality']['sex_age_unspecified']
            new_feature[json_to_db.get('sample')] = json_data['taxon']['mortality']['sample']
        
        objects.append(new_feature)
        cursor = sync_db(objects)
        
        # Insert into TABLE_SHEET_ROLE
        objects = []
        new_feature = {}
        new_feature['table_name'] = settings.TABLE_SHEET_ROLE
            
        #new_feature['id_cf'] = id_fiche
        new_feature['id_cf'] = json_data['id']
        new_feature['id_role'] = json_data['observer_id']
        objects.append(new_feature)
        sync_db(objects)

        # Commit transaction
        commit_transaction();

        response_content.append({
            #'status' : "Import done - statement id = %s, sheet id = %s" % (id_releve, id_fiche)
            'status' : _("Import done - statement id = %s, sheet id = %s") % (json_data['id'], json_data['id'])
        })
            
    except:
        #  Insert rejected JSON into synchro_table (text format)
        now = datetime.datetime.now()
        objects = []
        new_feature = {}
        if json_data['input_type'] == 'fauna':
            new_feature['table_name'] = settings.TABLE_FAILED_JSON_FAUNA
        else :
            new_feature['table_name'] = settings.TABLE_FAILED_JSON_MORTALITY
        new_feature['date_import'] = "%d-%d-%d %d:%d:%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        new_feature['json'] = data
        objects.append(new_feature)
        cursor = sync_db(objects)
        id_failed = cursor.fetchone()[0]

        # Commit transaction
        commit_transaction();
        
        response_content.append({
            'status' : _("Bad json or data (%d)") % id_failed
        })
        
    response = HttpResponse()
    simplejson.dump(response_content, response,
                ensure_ascii=False, separators=(',', ':'))
                
    return response
    

def export_taxon(request):
    """
    Export taxon table from DataBase to mobile
    """
    return export_data(request, settings.TABLE_TAXON)
    
    
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
    return export_data(request, settings.TABLE_TAXON_UNITY)


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

      
def export_data(request, table_name):
    """
    Export table_name data from DataBase to JSON
    """
    response_content = []
    if not check_token(request):
        response_content.append({
            'status' : _("You're not allowed to retreive information from this webservice")
        })
        response = HttpResponse()
        simplejson.dump(response_content, response,
                    ensure_ascii=False, separators=(',', ':'))                    
        return response
    
    # Get infos 
    response_objects = []
    json_table_name = settings.FAUNE_TABLE_INFOS.get(table_name).get('json_name')
    response_content = {json_table_name: []}
    
    get_data_object(response_objects, table_name)

    response_content[json_table_name] = response_objects
    
    response = HttpResponse()
    simplejson.dump(response_content, response,
                ensure_ascii=False, separators=(',', ':'))
                
    # get a string with JSON encoding the list
    s = simplejson.dumps(response_content, ensure_ascii=True, encoding='utf-8')
    f = open('/home/sbe/tmp/'+table_name+".json", 'w')
    f.write(s + "\n")
    f.close()
                
    return response


def check_token(request):
    """
    Check the validity of the token
    """
    
    if request.method == 'POST':
        if request.POST['token']:
            if request.POST['token'] == settings.TOKEN :
                return True
    return False

        
    
def get_data_object(response_content, table_name):
    """
    Perform a SELECT on the DB to retreive infos on associated object
    Param: table_name : name of the table
    """

    select_columns = settings.FAUNE_TABLE_INFOS.get(table_name).get('select_col')
    select_string = "SELECT %s FROM %s" \
                    % (select_columns, table_name)

    cursor = query_db(select_string)
    for row in cursor.fetchall():
        data = zip([ column[0] for column in cursor.description], row)
        feat_dict = SortedDict({})
        fid = ""
        for attr in data:
            key = attr[0]
            val = attr[1]
            if type(val).__name__ == "date":
                val = val.strftime("%d/%m/%Y")

            new_key = settings.FAUNE_TABLE_INFOS.get(table_name).get('db_to_json_columns').get(key)
            
            feat_dict[new_key] = val

        response_content.append(feat_dict)

    