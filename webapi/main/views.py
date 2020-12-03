# -*- coding: utf-8 -*-
from __future__ import with_statement

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.utils.http import http_date
from django.template import RequestContext, loader
from django.utils import simplejson
from django.utils.datastructures import SortedDict
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.servers.basehttp import FileWrapper
from django.db import connections, transaction

import logging
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
import json


from main.utils import sync_db, query_db, commit_transaction, check_connection

logger = logging.getLogger(__name__)

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
        response_content.update({
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

    if json_data['input_type'] == 'flora':
        response = import_data_flora(json_data, data)
    else:
        response = import_data_occtax_gn2(json_data, data)
    return response


@csrf_exempt
def import_data_fmi(json_data, data):
    """
    Import data for fauna, mortality and invertebrate (fmi)
    """

    response_content = {}

    if json_data['input_type'] == 'fauna' or json_data['input_type'] == 'mortality':
        table_infos = settings.OCCTAX_TABLE_INFOS
        table_sheet = settings.TABLE_OCCTAX_SHEE
        table_statement = settings.TABLE_FAUNA_STATEMENT
        database_id = settings.DB_OCCTAX_GN2
    if json_data['input_type'] == 'invertebrate':
        table_infos = settings.INV_TABLE_INFOS
        table_sheet = settings.TABLE_INV_SHEET
        table_statement = settings.TABLE_INV_STATEMENT
        database_id = settings.DB_INV

    local_srid = settings.LOCAL_SRID

    d = EasyDict(json_data)

    bad_id = False
    # Check if ID are unique
    count_string = "SELECT count(*) FROM %s WHERE %s='%s'" % (table_sheet, table_infos.get(table_sheet).get('id_col'), d.id)
    cursor = query_db(count_string, database_id)
    row = cursor.fetchone()
    if row:
        datarow = zip([column[0] for column in cursor.description], row)
        val = datarow[0][1]
        if val == 1:
            bad_id = True
            response_content.update({
                'status_code': _("1"),
                'status_message': _("Existing ID in database (%s) (%s)") % (table_sheet, d.id)
            })
    for taxon in d.taxons:
        count_string = "SELECT count(*) FROM %s WHERE %s='%s'" % (table_statement, table_infos.get(table_statement).get('id_col'), taxon.id)
        cursor = query_db(count_string, database_id)
        row = cursor.fetchone()
        if row:
            datarow = zip([column[0] for column in cursor.description], row)
            val = datarow[0][1]
            if val == 1:
                bad_id = True
                response_content.update({
                    'status_code': _("1"),
                    'status_message': _("Existing ID in database (%s) (%s)") % (table_statement, taxon.id)
                })

    if not bad_id:
        qualification = get_qualification(json_data)

        try:
            objects = []
            new_feature = {}
            json_to_db = table_infos.get(table_sheet).get('json_to_db_columns')

            # Insert into TABLE_SHEET
            new_feature[table_infos.get(table_sheet).get('id_col')] = d.id
            new_feature['table_name'] = table_sheet
            date_obs = d.dateobs.split(" ")
            new_feature[json_to_db.get('dateobs')] = date_obs[0]
            if json_data['input_type'] == 'invertebrate':
                new_feature[json_to_db.get('heure')] = date_obs[1].split(":")[0]
                new_feature[json_to_db.get('environment')] = d.environment

            new_feature[json_to_db.get('initial_input')] = d.initial_input
            new_feature['supprime'] = 'False'

            new_feature['id_protocole'] = qualification['protocol']
            new_feature['id_organisme'] = qualification['organism']
            new_feature['id_lot'] = qualification['lot']

            # we need to transform into local srid
            new_feature[json_to_db.get('geometry')] = "st_transform(ST_GeomFromText('POINT(%s %s)', 4326),%d)" % (d.geolocation.longitude, d.geolocation.latitude,local_srid)
            new_feature[json_to_db.get('accuracy')] = d.geolocation.accuracy
            objects.append(new_feature)
            cursor = sync_db(objects, table_infos, database_id)

            # Insert into TABLE_STATEMENT
            statement_ids = []
            for taxon in d.taxons:
                statement_ids.append(taxon.id)
                objects = []
                new_feature = {}
                json_to_db = table_infos.get(table_statement).get('json_to_db_columns')
                new_feature['table_name'] = table_statement
                new_feature['supprime'] = 'False'
                new_feature[table_infos.get(table_statement).get('id_col')] = taxon.id
                new_feature[table_infos.get(table_sheet).get('id_col')] = d.id
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
                if json_data['input_type'] == 'mortality':
                    new_feature[json_to_db.get('adult_male')] = taxon.mortality.adult_male
                    new_feature[json_to_db.get('adult_female')] = taxon.mortality.adult_female
                    new_feature[json_to_db.get('adult')] = taxon.mortality.adult
                    new_feature[json_to_db.get('not_adult')] = taxon.mortality.not_adult
                    new_feature[json_to_db.get('young')] = taxon.mortality.young
                    new_feature[json_to_db.get('yearling')] = taxon.mortality.yearling
                    new_feature[json_to_db.get('sex_age_unspecified')] = taxon.mortality.sex_age_unspecified
                    new_feature[json_to_db.get('sample')] = taxon.mortality.sample
                    new_feature[json_to_db.get('criterion')] = taxon.observation.criterion
                if json_data['input_type'] == 'invertebrate':
                    new_feature[json_to_db.get('adult_male')] = taxon.counting.adult_male
                    new_feature[json_to_db.get('adult_female')] = taxon.counting.adult_female
                    new_feature[json_to_db.get('adult')] = taxon.counting.adult
                    new_feature[json_to_db.get('not_adult')] = taxon.counting.not_adult
                    new_feature[json_to_db.get('criterion')] = taxon.observation.criterion

                new_feature[json_to_db.get('comment')] = taxon.comment

                objects.append(new_feature)
                cursor = sync_db(objects, table_infos, database_id)

            # Insert into TABLE_SHEET_ROLE (multiple observers enable)
            for observer in d.observers_id:
                objects = []
                new_feature = {}

                if json_data['input_type'] == 'fauna' or json_data['input_type'] == 'mortality':
                    new_feature['table_name'] = settings.TABLE_OCCTAX_SHEET_ROLE
                    new_feature['id_cf'] = d.id
                if json_data['input_type'] == 'invertebrate':
                    new_feature['table_name'] = settings.TABLE_INV_SHEET_ROLE
                    new_feature['id_inv'] = d.id

                new_feature['id_role'] = observer
                objects.append(new_feature)
                sync_db(objects, table_infos, database_id)

            # Commit transaction
            commit_transaction(database_id)

            response_content.update({
                'status_code': _("0"),
                'status_message': "id_sheet: %s, ids_statements: %s" % (d.id, ','.join(map(str, statement_ids)))
            })
        except Exception, e:
            #  Insert rejected JSON into synchro_table (text format)
            id_failed = archive_bad_data(data, json_data)

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


@csrf_exempt
def import_data_occtax_gn2(json_data, data):
    """
    Import data for GN2 occtax
    """

    response_content = {}

    table_infos = settings.OCCTAX_TABLE_INFOS
    table_sheet = settings.TABLE_OCCTAX_SHEET
    table_statement = settings.TABLE_OCCTAX_STATEMENT
    table_counting = settings.TABLE_OCCTAX_COUNTING
    database_id = settings.DB_OCCTAX_GN2


    local_srid = settings.LOCAL_SRID

    d = EasyDict(json_data)

    bad_id = False
    # Check if ID are unique
    count_string = "SELECT count(*) FROM %s WHERE %s='%s'" % (table_sheet, table_infos.get(table_sheet).get('id_col'), d.id)
    cursor = query_db(count_string, database_id)
    row = cursor.fetchone()
    if row:
        datarow = zip([column[0] for column in cursor.description], row)
        val = datarow[0][1]
        if val == 1:
            bad_id = True
            response_content.update({
                'status_code': _("1"),
                'status_message': _("Existing ID in database (%s) (%s)") % (table_sheet, d.id)
            })
    for taxon in d.taxons:
        count_string = "SELECT count(*) FROM %s WHERE %s='%s'" % (table_statement, table_infos.get(table_statement).get('id_col'), taxon.id)
        cursor = query_db(count_string, database_id)
        row = cursor.fetchone()
        if row:
            datarow = zip([column[0] for column in cursor.description], row)
            val = datarow[0][1]
            if val == 1:
                bad_id = True
                response_content.update({
                    'status_code': _("1"),
                    'status_message': _("Existing ID in database (%s) (%s)") % (table_statement, taxon.id)
                })

    if not bad_id:
        try:
            objects = []
            new_feature = {}
            # get default nomenclature 
            default_nomenclatures = get_default_nomenclatures(database_id)
            # Insert into TABLE_SHEET
            new_feature[table_infos.get(table_sheet).get('id_col')] = d.id
            new_feature['table_name'] = table_sheet
            date_obs = d.dateobs.split(" ")
            new_feature['date_min'] = date_obs[0]
            new_feature['date_max'] = date_obs[0]
            if json_data['input_type'] == 'invertebrate':
                new_feature['hour_min'] = date_obs[1]
                new_feature['hour_max'] = date_obs[1]
            new_feature['id_nomenclature_grp_typ'] = default_nomenclatures.get('TYP_GRP')

            # get altitude from database function
            query_altitude = "SELECT * FROM ref_geo.fct_get_altitude_intersection(ST_SetSRID(ST_MakePoint('{}','{}'), 4326))".format(
                d.geolocation.longitude, d.geolocation.latitude
            )
            cursor = query_db(query_altitude, database_id)
            row = cursor.fetchone()
            if row:
                try:
                    new_feature['altitude_min'] = int(row[0])
                    new_feature['altitude_max'] = int(row[1])
                except ValueError:
                    logger.info('Erreur while parsing altitude')
            new_feature['meta_device_entry'] = d.initial_input

            # default id_dataset for per app
            new_feature['id_dataset'] = settings.DEFAULT_ID_DATASET.get(json_data['input_type'])

            # write to the database in 4326 column -> the trigger write in geom_local
            new_feature['geom_4326'] = "ST_GeomFromText('POINT(%s %s)', 4326)" % (d.geolocation.longitude, d.geolocation.latitude)
            new_feature['precision'] = d.geolocation.accuracy
            objects.append(new_feature)
            cursor = sync_db(objects, table_infos, database_id)

            # Insert into TABLE_STATEMENT = occurrence
            statement_ids = []
            for taxon in d.taxons:
                statement_ids.append(taxon.id)
                objects = []
                new_feature = {}
                new_feature['table_name'] = table_statement
                new_feature['id_releve_occtax'] = d.id
                
                # get cd_nom from id_nom
                new_feature['cd_nom'] = get_cdnom_from_idnom(database_id, taxon.id_taxon)
                new_feature['nom_cite'] = taxon.name_entered

                new_feature['id_nomenclature_obs_technique'] = default_nomenclatures.get('METH_OBS')
                new_feature['id_nomenclature_behaviour'] = default_nomenclatures.get('OCC_COMPORTEMENT')
                
                if json_data['input_type'] != 'mortality':
                    new_feature['id_nomenclature_bio_condition'] = default_nomenclatures.get('ETA_BIO')
                else:
                    new_feature['id_nomenclature_bio_condition'] = get_id_nomenclature('ETA_BIO', '3')
                new_feature['id_nomenclature_bio_status'] = default_nomenclatures.get('STATUT_BIO')
                new_feature['id_nomenclature_naturalness'] = default_nomenclatures.get('NATURALITE')
                new_feature['id_nomenclature_exist_proof'] = default_nomenclatures.get('PREUVE_EXIST')
                new_feature['id_nomenclature_observation_status'] = default_nomenclatures.get('STATUT_OBS')
                new_feature['id_nomenclature_blurring'] = default_nomenclatures.get('DEE_FLOU')
                new_feature['id_nomenclature_source_status'] = default_nomenclatures.get('STATUT_SOURCE')
                new_feature['id_nomenclature_determination_method'] = default_nomenclatures.get('METH_DETERMIN')
                new_feature['meta_v_taxref'] = None

                # set nomenclature from criterion mapping
                MAPPING_CRITERION = settings.FAUNA_MAPPING_CRITERION_NOMENCLATURE_STATEMENT if json_data['input_type'] in ('mortality', 'fauna') else settings.INV_MAPPING_CRITERION_NOMENCLATURE_STATEMENT
                for nomenclature in MAPPING_CRITERION:
                    for mapping in nomenclature['mapping_id']:
                        if taxon.observation.criterion in mapping['id_criterion_origin']:
                            new_feature[nomenclature['nomenclature_type_target']] = get_id_nomenclature(*mapping['id_nomenclature_target'])
                #column, id_nomenclature = settings.MAPPING_CRITERION_NOMENCLATURE_STATEMENT.get(taxon.observation.criterion, (None, None))
                # if column is not None:
                #     new_feature[column] = id_nomenclature

                new_feature['comment'] = taxon.comment

                objects.append(new_feature)
                cursor = sync_db(objects, table_infos, database_id)
                # get generated id_occurrence
                id_occurence = cursor.fetchone()[0]

                commit_transaction(database_id)

                # Insert into TABLE_SHEET_ROLE (multiple observers enable)
                for observer in d.observers_id:
                    objects = []
                    new_feature = {}
                    new_feature['table_name'] = settings.TABLE_OCCTAX_SHEET_ROLE
                    new_feature['id_releve_occtax'] = d.id

                    new_feature['id_role'] = observer
                    objects.append(new_feature)
                    sync_db(objects, table_infos, database_id)

                # Push in counting
                # set the counting under 'counting" key for mortality JSON
                if json_data['input_type'] == 'mortality':
                    taxon.counting = taxon.mortality
                    taxon.pop('mortality')
                if taxon.counting.adult_male > 0:
                    objects = []
                    count_feature = {'table_name': table_counting, 'id_occurrence_occtax': id_occurence}
                    # column, id_nomenclature = settings.MAPPING_CRITERION_NOMENCLATURE_COUNTING.get(taxon.observation.criterion, (None, None))
                    # if column is not None:
                    #     count_feature[column] = id_nomenclature
                    # adulte
                    count_feature['id_nomenclature_life_stage'] = get_id_nomenclature('STADE_VIE', '2')
                    # male
                    count_feature['id_nomenclature_sex'] = get_id_nomenclature('SEXE', '3')
                    # obj de dénombrement = Individu
                    count_feature['id_nomenclature_obj_count'] = get_id_nomenclature('OBJ_DENBR', 'IND')
                    # type denembrement = NSP
                    count_feature['id_nomenclature_type_count'] = get_id_nomenclature('TYP_DENBR', 'NSP')
                    count_feature['count_min'] = taxon.counting.adult_male
                    count_feature['count_max'] = taxon.counting.adult_male
                    
                    cursor = sync_db([count_feature], table_infos, database_id)

                if taxon.counting.adult_female > 0:
                    objects = []
                    count_feature = {'table_name': table_counting, 'id_occurrence_occtax': id_occurence}
                    # adulte
                    count_feature['id_nomenclature_life_stage'] = get_id_nomenclature('STADE_VIE', '2')
                    # sexe = femelle
                    count_feature['id_nomenclature_sex'] = get_id_nomenclature('SEXE', '2')
                    # obj de dénombrement = Individu
                    count_feature['id_nomenclature_obj_count'] = get_id_nomenclature('OBJ_DENBR', 'IND')
                    # type denembrement = NSP
                    count_feature['id_nomenclature_type_count'] = get_id_nomenclature('TYP_DENBR', 'NSP')


                    count_feature['count_min'] = taxon.counting.adult_female
                    count_feature['count_max'] = taxon.counting.adult_female
                    cursor = sync_db([count_feature], table_infos, database_id)


                if taxon.counting.adult > 0:
                    count_feature = {'table_name': table_counting, 'id_occurrence_occtax': id_occurence}
                    # adulte
                    count_feature['id_nomenclature_life_stage'] = get_id_nomenclature('STADE_VIE', '2')
                    # sexe = inconnu
                    count_feature['id_nomenclature_sex'] = get_id_nomenclature('SEXE', '0')
                    # obj de dénombrement = Individu
                    count_feature['id_nomenclature_obj_count'] = get_id_nomenclature('OBJ_DENBR', 'IND')
                    # type denembrement = NSP
                    count_feature['id_nomenclature_type_count'] = get_id_nomenclature('TYP_DENBR', 'NSP')

                    count_feature['count_min'] = taxon.counting.adult
                    count_feature['count_max'] = taxon.counting.adult
                    cursor = sync_db([count_feature], table_infos, database_id)
                if taxon.counting.not_adult > 0:
                    count_feature = {'table_name': table_counting, 'id_occurrence_occtax': id_occurence}
                    # stade devie = inconnu
                    count_feature['id_nomenclature_life_stage'] = get_id_nomenclature('STADE_VIE', '3')
                    # sexe = inconnu
                    count_feature['id_nomenclature_sex'] = get_id_nomenclature('SEXE', '0')
                    # obj de dénombrement = Individu
                    count_feature['id_nomenclature_obj_count'] = get_id_nomenclature('OBJ_DENBR', 'IND')
                    # type denembrement = NSP
                    count_feature['id_nomenclature_type_count'] = get_id_nomenclature('TYP_DENBR', 'NSP')

                    count_feature['count_min'] = taxon.counting.not_adult
                    count_feature['count_max'] = taxon.counting.not_adult
                    cursor = sync_db([count_feature], table_infos, database_id)

                if taxon.counting.yearling > 0:
                    count_feature = {'table_name': table_counting, 'id_occurrence_occtax': id_occurence}
                    # stade de vie = immature
                    count_feature['id_nomenclature_life_stage'] = get_id_nomenclature('STADE_VIE', '4')
                    # sexe = inconnu
                    count_feature['id_nomenclature_sex'] = get_id_nomenclature('SEXE', '0')
                    # obj de dénombrement = Individu
                    count_feature['id_nomenclature_obj_count'] = get_id_nomenclature('OBJ_DENBR', 'IND')
                    # type denembrement = NSP
                    count_feature['id_nomenclature_type_count'] = get_id_nomenclature('TYP_DENBR', 'NSP')

                    count_feature['count_min'] = taxon.counting.yearling
                    count_feature['count_max'] = taxon.counting.yearling
                    cursor = sync_db([count_feature], table_infos, database_id)

                if taxon.counting.young > 0:
                    count_feature = {'table_name': table_counting, 'id_occurrence_occtax': id_occurence}
                    # stade de vie = immature
                    count_feature['id_nomenclature_life_stage'] = get_id_nomenclature('STADE_VIE', '3')
                    # sexe = inconnu
                    count_feature['id_nomenclature_sex'] = get_id_nomenclature('SEXE', '0')
                    # obj de dénombrement = Individu
                    count_feature['id_nomenclature_obj_count'] = get_id_nomenclature('OBJ_DENBR', 'IND')
                    # type denembrement = NSP
                    count_feature['id_nomenclature_type_count'] = get_id_nomenclature('TYP_DENBR', 'NSP')

                    count_feature['count_min'] = taxon.counting.young
                    count_feature['count_max'] = taxon.counting.young
                    cursor = sync_db([count_feature], table_infos, database_id)

                if taxon.counting.sex_age_unspecified > 0:
                    count_feature = {'table_name': table_counting, 'id_occurrence_occtax': id_occurence}
                    # stade devie = inconnu
                    count_feature['id_nomenclature_life_stage'] = get_id_nomenclature('STADE_VIE', '0')
                    # sexe = inconnu
                    count_feature['id_nomenclature_sex'] = get_id_nomenclature('SEXE', '0')
                    # obj de dénombrement = Individu
                    count_feature['id_nomenclature_obj_count'] = get_id_nomenclature('OBJ_DENBR', 'IND')
                    # type denembrement = NSP
                    count_feature['id_nomenclature_type_count'] = get_id_nomenclature('TYP_DENBR', 'NSP')

                    count_feature['count_min'] = taxon.counting.sex_age_unspecified
                    count_feature['count_max'] = taxon.counting.sex_age_unspecified
                    cursor = sync_db([count_feature], table_infos, database_id)


            # Commit transaction
            commit_transaction(database_id)

            response_content.update({
                'status_code': _("0"),
                'status_message': "id_sheet: %s, ids_statements: %s" % (d.id, ','.join(map(str, statement_ids)))
            })
        except Exception as e:

            #  Insert rejected JSON into synchro_table (text format)
            id_failed = archive_bad_data(data, json_data)

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


@csrf_exempt
def import_data_flora(json_data, data):
    """
    Import data for flora
    """

    response_content = {}

    table_infos = settings.FLORA_TABLE_INFOS
    table_apresence = settings.TABLE_FLORA_T_APRESENCE
    table_zprospection = settings.TABLE_FLORA_T_ZPROSPECTION
    database_id = settings.DB_FLORA

    d = EasyDict(json_data)

    bad_id = False
    # Check if ID are unique
    count_string = "SELECT count(*) FROM %s WHERE %s='%s'" % (table_zprospection, table_infos.get(table_zprospection).get('id_col'), d.id)
    cursor = query_db(count_string, database_id)
    row = cursor.fetchone()
    if row:
        datarow = zip([column[0] for column in cursor.description], row)
        val = datarow[0][1]
        if val == 1:
            bad_id = False
            response_content.update({
                'status_code': _("1"),
                'status_message': _("Existing ID in database (%s) (%s)") % (table_zprospection, d.id)
            })
    for taxon in d.taxons:
        for area in taxon.areas:
            count_string = "SELECT count(*) FROM %s WHERE %s='%s'" % (table_apresence, table_infos.get(table_apresence).get('id_col'), area.id)
            cursor = query_db(count_string, database_id)
            row = cursor.fetchone()
            if row:
                datarow = zip([column[0] for column in cursor.description], row)
                val = datarow[0][1]
                if val == 1:
                    bad_id = True
                    response_content.update({
                        'status_code': _("1"),
                        'status_message': _("Existing ID in database (%s) (%s)") % (table_apresence, area.id)
                    })
        # even the json offers a list, there's only one taxa
        break

    if not bad_id:
        qualification = get_qualification(json_data)

        try:
            objects = []
            new_feature = {}
            json_to_db = table_infos.get(table_zprospection).get('json_to_db_columns')
            areas_ids = []
            for taxon in d.taxons:
                # Insert into ZPROSPECTION
                new_feature[table_infos.get(table_zprospection).get('id_col')] = d.id
                new_feature['table_name'] = table_zprospection
                date_obs = d.dateobs.split(" ")
                new_feature[json_to_db.get('dateobs')] = date_obs[0]
                new_feature[json_to_db.get('initial_input')] = d.initial_input
                new_feature['supprime'] = 'False'
                new_feature[json_to_db.get('name_entered')] = taxon.name_entered
                new_feature[json_to_db.get('id_taxon')] = taxon.id_taxon

                new_feature['id_protocole'] = qualification['protocol']
                new_feature['id_organisme'] = qualification['organism']
                new_feature['id_lot'] = qualification['lot']

                # we need to transform geometry into local srid
                string_geom = get_geometry_string_from_coords(taxon.prospecting_area.feature.geometry.coordinates, taxon.prospecting_area.feature.geometry.type)
                new_feature[json_to_db.get('geometry')] = string_geom

                objects.append(new_feature)
                cursor = sync_db(objects, table_infos, database_id)

                # Insert into APRESENCE
                for area in taxon.areas:
                    areas_ids.append(area.id)
                    objects = []
                    new_feature = {}
                    json_to_db = table_infos.get(table_apresence).get('json_to_db_columns')
                    new_feature['table_name'] = table_apresence
                    new_feature['supprime'] = 'False'
                    new_feature[table_infos.get(table_apresence).get('id_col')] = area.id
                    new_feature[table_infos.get(table_zprospection).get('id_col')] = d.id
                    new_feature[json_to_db.get('id')] = area.id
                    new_feature[json_to_db.get('phenology')] = area.phenology
                    # round 'computed_area' value
                    new_feature[json_to_db.get('computed_area')] = int(round(area.computed_area))

                    if area.frequency.type == "estimation":
                        new_feature[json_to_db.get('frequenceap')] = area.frequency.value
                        new_feature[json_to_db.get('id_frequence_methodo_new')] = settings.FLORA_FREQUENCY_ESTIMATION
                    if area.frequency.type == "transect":
                        new_feature[json_to_db.get('frequenceap')] = area.frequency.value
                        new_feature[json_to_db.get('nb_transects_frequence')] = area.frequency.transects
                        new_feature[json_to_db.get('nb_points_frequence')] = area.frequency.transect_no  # TODO check
                        new_feature[json_to_db.get('nb_contacts_frequence')] = area.frequency.transect_yes  # TODO check
                        new_feature[json_to_db.get('longueur_pas')] = area.frequency.computed_recommended_step
                        new_feature[json_to_db.get('id_frequence_methodo_new')] = settings.FLORA_FREQUENCY_TRANSECT

                    string_geom = get_geometry_string_from_coords(area.feature.geometry.coordinates, area.feature.geometry.type)
                    new_feature[json_to_db.get('geometry')] = string_geom

                    if area.counting.type == "none":
                        new_feature[json_to_db.get('id_comptage_methodo')] = settings.FLORA_COUNTING_NONE
                    if area.counting.type == "exhaustive":
                        new_feature[json_to_db.get('total_steriles')] = area.counting.total_sterile
                        new_feature[json_to_db.get('total_fertiles')] = area.counting.total_fertile
                        new_feature[json_to_db.get('id_comptage_methodo')] = settings.FLORA_COUTING_EXHAUSTIVE
                    if area.counting.type == "sampling":
                        new_feature[json_to_db.get('total_steriles')] = area.counting.total_sterile
                        new_feature[json_to_db.get('total_fertiles')] = area.counting.total_fertile
                        new_feature[json_to_db.get('nb_placettes_comptage')] = area.counting.plots
                        new_feature[json_to_db.get('surface_placette_comptage')] = area.counting.plot_surface
                        new_feature[json_to_db.get('effectif_placettes_steriles')] = area.counting.sterile
                        new_feature[json_to_db.get('effectif_placettes_fertiles')] = area.counting.fertile
                        new_feature[json_to_db.get('id_comptage_methodo')] = settings.FLORA_COUTING_SAMPLING

                    new_feature[json_to_db.get('comment')] = area.comment

                    objects.append(new_feature)
                    cursor = sync_db(objects, table_infos, database_id)

                    # Physiognomies
                    for physiognomy in area.physiognomy:
                        objects = []
                        new_feature = {}

                        new_feature['table_name'] = settings.TABLE_FLORA_COR_AP_PHYSIONOMIE
                        new_feature['indexap'] = area.id
                        new_feature['id_physionomie'] = physiognomy
                        objects.append(new_feature)
                        sync_db(objects, table_infos, database_id)

                    # Disturbances
                    for disturbance in area.disturbances:
                        objects = []
                        new_feature = {}

                        new_feature['table_name'] = settings.TABLE_FLORA_COR_AP_PERTURB
                        new_feature['indexap'] = area.id
                        new_feature['codeper'] = disturbance
                        objects.append(new_feature)
                        sync_db(objects, table_infos, database_id)

                break  # even the json offers a list, there's only one taxa

            # Insert into TABLE_SHEET_ROLE (multiple observers enable)
            for observer in d.observers_id:
                objects = []
                new_feature = {}

                new_feature['table_name'] = settings.TABLE_FLORA_COR_ZP_OBS
                new_feature['indexzp'] = d.id

                new_feature['codeobs'] = observer
                objects.append(new_feature)
                sync_db(objects, table_infos, database_id)

            # Commit transaction
            commit_transaction(database_id)

            # Sync external DB
            if settings.SYNC_DB_CMD:
                cmd = "%s%s" % (settings.SYNC_DB_CMD, d.id)
                os.system(cmd)

            response_content.update({
                'status_code': _("0"),
                'status_message': "id_prospection: %s, ids_areass: %s" % (d.id, ','.join(map(str, areas_ids)))
            })
        except Exception, e:
            ###  Insert rejected JSON into synchro_table (text format)
            id_failed = archive_bad_data(data, json_data)

            response_content.update({
                'status_code': _("1"),
                # 'status_message': _("Bad json or data (%d)") % id_failed
                'status_message': _("Bad json or data (%s)") % e
            })
    else:
        archive_bad_data(data, json_data)

    response = HttpResponse()
    simplejson.dump(response_content, response,
                ensure_ascii=False, separators=(',', ':'))

    return response


def get_geometry_string_from_coords(coords_list, type):

    coords = []
    extra_parenthesis = ""
    local_srid = settings.LOCAL_SRID

    if type == "Point":
        string_geom = "st_transform(ST_GeomFromText('POINT("
    if type == "LineString":
        string_geom = "st_transform(ST_GeomFromText('LINESTRING("
    if type == "Polygon":
        string_geom = "st_transform(ST_GeomFromText('POLYGON(("
        extra_parenthesis = ")"

    if type == "Point":
        coords.append("%s %s" % (coords_list[0], coords_list[1]))
    if type == "LineString":
        for coord in coords_list:
            coords.append("%s %s" % (coord[0], coord[1]))
    if type == "Polygon":
        # Maybe in the future we will manage polygon with hole
        # In that case coords_list[0] will be the main shape, and coords_list[1], coords_list[2]... the holes
        for coord in coords_list[0]:
            coords.append("%s %s" % (coord[0], coord[1]))
        # close the shape
        for coord in coords_list[0]:
            coords.append("%s %s" % (coord[0], coord[1]))
            break


    #string_geom = "%s%s)%s', 4326),27572)" % (string_geom, ",".join(coords), extra_parenthesis)
    string_geom = "%s%s)%s', 4326),%d)" % (string_geom, ",".join(coords), extra_parenthesis, local_srid)

    return string_geom


def archive_bad_data(data, json_data):
    #  Insert rejected JSON into synchro_table (text format)
    now = datetime.datetime.now()
    objects = []
    new_feature = {}
    if json_data['input_type'] in ('fauna', 'mortality', 'invertebrate'):
        new_feature['table_name'] = settings.TABLE_FAILED_JSON_OCCTAX
        table_infos = settings.OCCTAX_TABLE_INFOS
        database_id = settings.DB_OCCTAX_GN2
    if json_data['input_type'] == 'flora':
        new_feature['table_name'] = settings.TABLE_FAILED_JSON_FLORA
        table_infos = settings.FLORA_TABLE_INFOS
        database_id = settings.DB_FLORA

    new_feature['date_import'] = "%d-%d-%d %d:%d:%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    new_feature['json'] = data
    objects.append(new_feature)
    cursor = sync_db(objects, table_infos, database_id)
    id_failed = cursor.fetchone()[0]

    # Commit transaction
    commit_transaction(database_id)

    return id_failed


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
    src = "%s" % (settings.MOBILE_SQLITE_SAMPLE)
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

            tables_infos = {'fauna': settings.OCCTAX_TABLE_INFOS, 'invertebrate': settings.INV_TABLE_INFOS, 'flora': settings.FLORA_TABLE_INFOS}

            for create_string in settings.MOBILE_SQLITE_CREATE_QUERY:
                cur.execute(create_string)

            # Extra SQL to execute on database
            for insert_string in settings.MOBILE_SQLITE_EXTRA_SQL:
                cur.execute(insert_string)

            # Fill data (global)
            table_infos = settings.GLOBAL_TABLE_INFOS
            tabTab = []
            tabTab.append({'table_name': settings.TABLE_USERS})
            for current_tab in tabTab:
                # ->pg_table_name = utilisateurs.v_nomade_observateurs_all
                pg_table_name = current_tab['table_name']
                li_table_name = table_infos.get(pg_table_name).get('sqlite_name')
                where_string = table_infos.get(pg_table_name).get('where_string')
                complement_string = table_infos.get(pg_table_name).get('groupby_string')
                database_id = table_infos.get('database_id')
                if where_string != None:
                    where_string = "WHERE %s" % (where_string)
                else:
                    where_string = ""
                if complement_string != None:
                    complement_string = "GROUP BY %s" % (complement_string)
                else:
                    complement_string = ""
                response_content = get_data(request, pg_table_name, where_string, complement_string, table_infos, False, database_id)
                for obj in response_content[table_infos.get(pg_table_name).get('json_name')]:
                    colTab = []
                    valTab = []
                    mask = 0
                    for key in obj:
                        if key == "mode":
                            # fauna, flora, inv
                            mask = 00000000
                            if "fauna" in obj[key]:
                                mask += 11000000
                            if "inv" in obj[key]:
                                mask += 100000
                            if "flora" in obj[key]:
                                mask += 10000

                            mask = int("%s" % (mask), 2)

                            colTab.append("filter")
                            valTab.append(mask)
                        else:
                            colTab.append(key)
                            valTab.append(unicode(obj[key]).replace("'", "''"))

                    insert_string = "INSERT INTO %s (%s) values (%s)" % \
                                        (li_table_name,
                                        ",".join(colTab),
                                        "'" + "','".join(map(unicode, valTab)) + "'"
                                        )
                    cur.execute(insert_string)

            # Fill data (fauna, invertebrate...)
            for mode in tables_infos:
                table_infos = tables_infos[mode]
                tabTab = []
                if mode == "fauna":
                    # filter : tells if we have calculate a filter
                    tabTab.append({'table_name': settings.TABLE_GN2_TAXA_UNITY, 'filter': False})
                    tabTab.append({'table_name': settings.TABLE_GN2_TAXA, 'filter': True})
                    tabTab.append({'table_name': settings.TABLE_FAUNA_CRITERION, 'filter': False})
                if mode == "invertebrate":
                    # on ne recalcule pas les corespodance pour inverterbré, car tout est dans la table
                    # gn_synthese.cor_area_taxon et dans a la vue  gn_synchronomade.v_nomade_cor_area_taxon
                    #tabTab.append({'table_name': settings.TABLE_INV_TAXA_UNITY, 'filter': False})
                    tabTab.append({'table_name': settings.TABLE_INV_TAXA, 'filter': True})
                    tabTab.append({'table_name': settings.TABLE_INV_CRITERION, 'filter': False})
                    tabTab.append({'table_name': settings.TABLE_INV_ENVIRONEMENTS, 'filter': False})
                if mode == "flora":
                    tabTab.append({'table_name': settings.TABLE_FLORA_TAXA, 'filter': True})
                    tabTab.append({'table_name': settings.TABLE_FLORA_INCLINES, 'filter': False})
                    tabTab.append({'table_name': settings.TABLE_FLORA_DISTURBANCES, 'filter': False})
                    tabTab.append({'table_name': settings.TABLE_FLORA_PHENOLOGY, 'filter': False})
                    tabTab.append({'table_name': settings.TABLE_FLORA_PHYSIOGNOMY, 'filter': False})
                    tabTab.append({'table_name': settings.TABLE_FLORA_VISU_FP, 'filter': False})
                    tabTab.append({'table_name': settings.TABLE_FLORA_SEARCH, 'filter': False})
                for current_tab in tabTab:
                    pg_table_name = current_tab['table_name']
                    apply_filter = current_tab['filter']
                    li_table_name = table_infos.get(pg_table_name).get('sqlite_name')
                    where_string = table_infos.get(pg_table_name).get('where_string')
                    database_id = table_infos.get('database_id') 
                    if where_string != None:
                        where_string = "WHERE %s" % (where_string)
                    else:
                        where_string = ""
                    response_content = get_data(request, pg_table_name, where_string, None, table_infos, False, database_id)
                    for obj in response_content[table_infos.get(pg_table_name).get('json_name')]:
                        colTab = []
                        valTab = []
                        mask = 0
                        for key in obj:
                            # special case for fauna (mortality)
                            if pg_table_name == settings.TABLE_GN2_TAXA and mode == "fauna" and key == "cf":
                                if obj[key] == True:
                                    mask = int('11000000', 2)
                                else:
                                    mask = int('01000000', 2)
                            else:
                                colTab.append(key)
                                valTab.append(unicode(obj[key]).replace("'", "''"))

                        # if filter on this table
                        # apply a binary mask
                        # 1-faune, 2-mortality, 3-invertebrate, 4-flore
                        if apply_filter:
                            if pg_table_name != settings.TABLE_GN2_TAXA:
                                if mode == "fauna":
                                    mask = int('11000000', 2)

                            if mode == "invertebrate":
                                mask = int('00100000', 2)

                            if mode == "flora":
                                mask = int('00010000', 2)

                            colTab.append("filter")
                            valTab.append(mask)

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
            response["Last-Modified"] = http_date()
            response['Content-Length'] = os.path.getsize(output)
            response['Content-Disposition'] = 'attachment; filename=data.db'

            #header('Last-Modified: '.gmdate('D, d M Y H:i:s', filemtime($fn)).' GMT', true, 304);
    finally:
        pass
        #if output:
        #    os.unlink(output)

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
    # same table for fauna or invertebrate
    table_name = settings.TABLE_GN2_UNITY_GEOJSON
    table_infos_geojson = settings.OCCTAX_TABLE_INFOS_GEOJSON
    database_id = settings.DB_OCCTAX_GN2

    response_objects = []

    get_data_object_txt(response_objects, table_name, table_infos_geojson, database_id)

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
            response['Last-Modified'] = http_date()
            response['Content-Length'] = len(export)
            response['Content-Disposition'] = 'attachment; filename=unity.wkt'
    finally:
        pass
        #if output:
        #    os.unlink(output)

    return response

def get_qualification(json_data):
    """
    Build the corresponding qualification metadata from given JSON input or
    build the default one from settings
    """

    qualification = {}
    input_type = json_data['input_type']

    logger.debug(_("input type: %s") % input_type)

    try:
        qualification['organism'] = json_data['qualification']['organism']
    except KeyError as ke:
        qualification['organism'] = getattr(settings, input_type.upper() + '_ID_ORGANISM', 0)
        logger.debug(_("No organism ID found, use default: %s") % qualification['organism'])

        pass

    try:
        qualification['protocol'] = json_data['qualification']['protocol']
    except KeyError as ke:
        qualification['protocol'] = getattr(settings, input_type.upper() + '_ID_PROTOCOL', 0)
        logger.debug(_("No protocol ID found, use default: %s") % qualification['protocol'])

        pass

    try:
        qualification['lot'] = json_data['qualification']['lot']
    except KeyError as ke:
        qualification['lot'] = getattr(settings, input_type.upper() + '_ID_LOT', 0)
        logger.debug(_("No lot ID found, use default: %s") % qualification['lot'])

        pass

    return qualification

def get_data(request, table_name, where_string, complement_string, table_infos, testing, database_id):
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
    json_table_name = table_infos.get(table_name).get('json_name')
    response_content = {json_table_name: []}

    get_data_object(response_objects, table_name, where_string, complement_string, table_infos, testing, database_id)

    response_content[json_table_name] = response_objects

    return response_content


def check_token(request):
    """
    Check the validity of the token
    """

    # HACK TODO: remove temporary check token
    if request.method == 'POST':
        # if request.POST['token']:
        #     if request.POST['token'] == settings.TOKEN:
        return True, None

    response_content = []
    response_content.append({
        'status': _("You're not allowed to retreive information from this webservice")
    })
    response = HttpResponse(status=404)
    simplejson.dump(response_content, response,
                ensure_ascii=False, separators=(',', ':'))

    return False, response


def get_data_object(response_content, table_name, where_string, complement_string, table_infos, testing, database_id):
    """
    Perform a SELECT on the DB to retrieve infos on associated object
    Param: table_name : name of the table
    """
    test_string = ""
    if testing:
        test_string = " LIMIT 1"
    select_columns = table_infos.get(table_name).get('select_col')
    select_string = "SELECT %s FROM %s %s %s %s" \
                    % (select_columns, table_name, where_string, complement_string, test_string)

    cursor = query_db(select_string, database_id)
    for row in cursor.fetchall():
        data = zip([column[0] for column in cursor.description], row)
        feat_dict = SortedDict({})
        for attr in data:
            key = attr[0]
            val = attr[1]
            if type(val).__name__ == "date":
                val = val.strftime("%d/%m/%Y")

            new_key = table_infos.get(table_name).get('db_to_json_columns').get(key)

            feat_dict[new_key] = val

        response_content.append(feat_dict)


def get_data_object_txt(response_content, table_name, table_infos_geojson, database_id):
    """
    Perform a SELECT on the DB to retreive infos on associated object, txt format
    Param: table_name : name of the table
    """

    select_columns = table_infos_geojson.get(table_name).get('select_col')
    select_string = "SELECT %s FROM %s" \
                    % (select_columns, table_name)

    cursor = query_db(select_string, database_id)
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
    res_connection_fauna = check_connection(settings.DB_OCCTAX_GN2)
    res_connection_inv = check_connection(settings.DB_INV)
    res_connection_flora = check_connection(settings.DB_FLORA)

    tables_infos = {'fauna': settings.OCCTAX_TABLE_INFOS, 'invertebrate': settings.INV_TABLE_INFOS}

    # check if views are availables
    res_views = True
    try:
        for mode in tables_infos:
            table_infos = tables_infos[mode]
            tabTab = []
            if mode == "fauna":
                tabTab.append(settings.TABLE_OCCTAX_SHEET_ROLE)
                tabTab.append(settings.TABLE_GN2_TAXA_UNITY)
                tabTab.append(settings.TABLE_GN2_TAXA)
                tabTab.append(settings.TABLE_FAUNA_CRITERION)
                database_id = settings.DB_OCCTAX_GN2
            if mode == "invertebrate":
                tabTab.append(settings.TABLE_INV_USER)
                tabTab.append(settings.TABLE_INV_TAXA_UNITY)
                tabTab.append(settings.TABLE_INV_TAXA)
                tabTab.append(settings.TABLE_INV_CRITERION)
                database_id = settings.DB_INV
            if mode == "flora":
                database_id = settings.DB_FLORA
                #TODO

            for pg_table_name in tabTab:
                li_table_name = table_infos.get(pg_table_name).get('sqlite_name')
                test_return = get_data(request, pg_table_name, None, None, table_infos, True, database_id)
    except:
        res_views = False

    response_content.update({
        'status_code': _("0"),
        'status_message': "DB connection FAUNA %d, DB connection INVERTEBRATE %d, DB connection FLORA %d, Views available %d" % (res_connection_fauna, res_connection_inv, res_connection_flora, res_views)
    })
    response = HttpResponse()
    simplejson.dump(response_content, response,
                ensure_ascii=False, separators=(',', ':'))
    return response


@csrf_exempt
def soft_version(request):
    """
    Return the version of the mobile soft (JSON) by reading a json config file
    """
    response_content = {'apps': []}
    res, response = check_token(request)

    if not res:
        return response

    # read the version file
    version_file = os.path.join(
        os.path.normpath(settings.MOBILE_SOFT_PATH),
        'version.json')

    try:
        json_data = open(version_file)
        version_data = simplejson.load(json_data)
        json_data.close()

        for apps in version_data['apps']:
            response_content['apps'].append({
                "package": apps["package"],
                "sharedUserId": apps["sharedUserId"],
                "versionCode": apps["versionCode"],
                "versionName": apps["versionName"],
                "apkName": apps["apkName"],
            })
    except:
        response_content.update({
            'status_code': _("1"),
            'status_message': "Version file is not available ('%s')" % (version_file)
        })

    return HttpResponse(
        simplejson.dumps(response_content),
        content_type="application/json")


@csrf_exempt
def soft_download(request, apk_name):
    """
    Return a downloadable file of the mobile soft
    """
    response_content = {}
    res, response = check_token(request)
    if not res:
        return response

    file_path = "%s%s" % (settings.MOBILE_SOFT_PATH, apk_name)
    try:
        wrapper = FileWrapper(file(file_path))
        response = HttpResponse(wrapper, content_type='text/plain')
        response['Content-Length'] = os.path.getsize(file_path)
        response['Content-Disposition'] = 'attachment; filename=%s' % (apk_name)
    except:
        response_content.update({
            'status_code': _("1"),
            'status_message': "APK file is not available (%s)" % (apk_name)
        })
        response = HttpResponse(status=404)
        simplejson.dump(response_content, response,
                    ensure_ascii=False, separators=(',', ':'))
        return response

    return response


@csrf_exempt
def data_download(request, file_name, organism_name=None,):
    """
    Return the required file
    """
    response_content = {}
    res, response = check_token(request)
    if not res:
        return response

    if organism_name:
        file_path = "%s%s/%s" % (settings.MOBILE_FILE_PATH, organism_name, file_name)
    else:
        file_path = "%s%s" % (settings.MOBILE_FILE_PATH, file_name)

    try:
        wrapper = FileWrapper(file(file_path))
        response = HttpResponse(wrapper, content_type='text/plain')
        response["Last-Modified"] = http_date(os.stat(file_path).st_mtime)
        response['Content-Length'] = os.path.getsize(file_path)
        response['Content-Disposition'] = 'attachment; filename=%s' % (file_name)
    except:
        response_content.update({
            'status_code': _("1"),
            'status_message': "File is not available (%s)" % (file_name)
        })
        response = HttpResponse(status=404)
        simplejson.dump(response_content, response,
                    ensure_ascii=False, separators=(',', ':'))
        return response

    return response


# NOT USED ANYMORE :
####################

def export_taxon(request):
    """170
    Export taxon table from DataBase to mobile
    """
    return export_data(request, settings.TABLE_GN2_TAXA)


#def export_family(request):
    #"""
    #Export family table from DataBase to mobile
    #"""
    #return export_data(request, settings.TABLE_FAUNA_FAMILY)


def export_unity(request):
    """
    Export unity table from DataBase to mobile
    """
    return export_data(request, settings.TABLE_GN2_UNITY)


def export_taxon_unity(request):
    """
    Export crossed taxon / unity table from DataBase to mobile
    """
    return export_data(request, settings.TABLE_GN2_TAXA_UNITY)


def export_criterion(request):
    """
    Export criterion table from DataBase to mobile
    """
    return export_data(request, settings.TABLE_FAUNA_CRITERION)


def export_user(request):
    """
    Export user table from DataBase to mobile
    """
    return export_data(request, settings.TABLE_OCCTAX_SHEET_ROLE)


def export_classes(request):
    """
    Export classes table from DataBase to mobile
    """
    return export_data(request, settings.TABLE_OCCTAX_CLASSES)


def export_data(request, table_name):
    """
    Export table_name data from DataBase to JSON
    """
    response_content = get_data(request, table_name, None, None, False)

    response = HttpResponse()
    simplejson.dump(response_content, response,
                ensure_ascii=False, separators=(',', ':'))

    return response


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
    table_name = settings.TABLE_GN2_UNITY_GEOJSON
    response_objects = []
    json_table_name = settings.OCCTAX_TABLE_INFOS_GEOJSON.get(table_name).get('json_name')
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
            response['Last-Modified'] = http_date()
            response['Content-Length'] = os.path.getsize(output)
            response['Content-Disposition'] = 'attachment; filename=unity.geojson'
    finally:
        if output:
            os.unlink(output)

    return response


def get_data_object_geojson(response_content, table_name):
    """
    Perform a SELECT on the DB to retreive infos on associated object, geojson format
    Param: table_name : name of the table
    """

    select_columns = settings.OCCTAX_TABLE_INFOS_GEOJSON.get(table_name).get('select_col')
    select_string = "SELECT %s FROM %s" \
                    % (select_columns, table_name)

    cursor = query_db(select_string, database_id)
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
                new_key = settings.OCCTAX_TABLE_INFOS_GEOJSON.get(table_name).get('db_to_json_columns').get(key)
                properties_dict[new_key] = val

        feat_dict["properties"] = properties_dict
        feat_dict["geometry"] = simplejson.loads(geometry_dict)

        i = i + 1
        response_content.append(feat_dict)

def get_default_nomenclatures(database_id):
    """
    Return default nomenclature for occtax
    """
    query = """
            SELECT * FROM pr_occtax.defaults_nomenclatures_value
            """
    # Connect to correct DB
    cursor = connections[database_id].cursor()
    # Execute SQL
    cursor.execute(query)
    res = cursor.fetchall()
    return {r[0]: r[4] for r in res}


def get_cdnom_from_idnom(database_id, idnom):
    """
    Return cd_nom from a given id_nom
    """
    query = """
            SELECT cd_nom FROM taxonomie.bib_noms WHERE id_nom = {}
            """.format(idnom)
    # Connect to correct DB
    cursor = connections[database_id].cursor()
    # Execute SQL
    cursor.execute(query)
    res = cursor.fetchone()
    return res[0] if res is not None else res


def get_id_nomenclature(mnemonic_code, cd_nomenclature):
    """
    Return id_nomenclature from a given mnemonic type and a cd_nomenclature
    """

    query = "SELECT ref_nomenclatures.get_id_nomenclature('{}', '{}')".format(mnemonic_code, cd_nomenclature)
    cursor = connections[settings.DB_OCCTAX_GN2].cursor()
    cursor.execute(query)
    res = cursor.fetchone()
    return res[0] if res is not None else res
