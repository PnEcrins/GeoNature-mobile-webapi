import django
from django.test import TestCase
from django.utils import simplejson
from easydict import EasyDict
from main.utils import query_db, commit_transaction
import datetime

class MainViewsTestCase(TestCase):
    def test_import(self):
        
        old_db = django.db.connections['default']
        django.db.connections['default'].settings_dict['NAME']
        try:
            django.db.connections['default'] = old_db.__class__(old_db.settings_dict)
            django.db.connections['default'].settings_dict['NAME'] = 'geonaturedb'
            
            data = open('main/data.json').read()
            json_data = simplejson.loads(data)
            inputData = EasyDict(json_data)
            
            resp = self.client.post('/import/', {'data': data, 'token': '666'})
            self.assertEqual(resp.status_code, 200)
            
            json_data = simplejson.loads(resp.content)
            d = EasyDict(json_data)
            
            # Check that data has been inserted
            # sheet
            selectString = "SELECT insee, dateobs,altitude_saisie, altitude_sig, altitude_retenue, supprime, pdop, the_geom_27572, the_geom_2154, saisie_initiale, id_organisme, srid_dessin, id_protocole, id_lot, the_geom_3857 FROM contactfaune.t_fiches_cf WHERE id_cf = %s" % (d.id_sheet)
            cursor = query_db(selectString)
            assertDict = {
                'insee': lambda val: self.assertEqual(val, None),
                'dateobs': lambda val: self.assertEqual(val, datetime.date(2012, 9, 19)),
                'altitude_saisie': lambda val: self.assertEqual(val, None),
                'altitude_sig': lambda val: self.assertEqual(val, 0),
                'altitude_retenue': lambda val: self.assertEqual(val,0),
                'supprime': lambda val: self.assertEqual(val, False),
                'pdop': lambda val: self.assertEqual(val, 22),
                'the_geom_27572': lambda val: self.assertEqual(val, '0101000020B46B000096855BCD99DA1241B26AFE7355364141'),
                'the_geom_local': lambda val: self.assertEqual(val, '01010000206A080000A0C81FCB83E915418E90CC4D16875941'),
                'saisie_initiale': lambda val: self.assertEqual(val, 'pda'),
                'id_organisme': lambda val: self.assertEqual(val, 2),
                'srid_dessin': lambda val: self.assertEqual(val, 2154),
                'id_protocole': lambda val: self.assertEqual(val, 140),
                'id_lot': lambda val: self.assertEqual(val, 4),
                'the_geom_3857': lambda val: self.assertEqual(val, '0101000020110F00002A6DE372E38404C18C60D12226D15641')
            }            
            for row in cursor.fetchall():
                data = zip([column[0] for column in cursor.description], row)
                for key, val in data:
                    assertDict[key](val)

            ids_statements = d.ids_statements.split(',')
            # statement 1
            selectString = "SELECT id_releve_cf, id_nom, id_critere_cf, am, af, ai, na, sai, jeune, yearling, cd_ref_origine, nom_taxon_saisi, commentaire, supprime, prelevement FROM contactfaune.t_releves_cf WHERE id_cf = %s and id_releve_cf = %s" % (d.id_sheet, ids_statements[0])
            cursor = query_db(selectString)
            assertDict = {
                'id_releve_cf': lambda val: self.assertEqual(val,401382208),
                'id_nom': lambda val: self.assertEqual(val,1),
                'id_critere_cf': lambda val: self.assertEqual(val,1),
                'am': lambda val: self.assertEqual(val,1),
                'af': lambda val: self.assertEqual(val,0),
                'ai': lambda val: self.assertEqual(val,0),
                'na': lambda val: self.assertEqual(val,0),
                'sai': lambda val: self.assertEqual(val,0),
                'jeune': lambda val: self.assertEqual(val,0),
                'yearling': lambda val: self.assertEqual(val,0),
                'cd_ref_origine': lambda val: self.assertEqual(val,267),
                'nom_taxon_saisi': lambda val: self.assertEqual(val,'taxon 1'),
                'commentaire': lambda val: self.assertEqual(val,'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'),
                'supprime': lambda val: self.assertEqual(val,False),
                'prelevement': lambda val: self.assertEqual(val,False)
            }            
            for row in cursor.fetchall():
                data = zip([column[0] for column in cursor.description], row)
                for key, val in data:
                    assertDict[key](val)

            # statement 2
            selectString = "SELECT id_releve_cf, id_nom, id_critere_cf, am, af, ai, na, sai, jeune, yearling, cd_ref_origine, nom_taxon_saisi, commentaire, supprime, prelevement FROM contactfaune.t_releves_cf WHERE id_cf = %s and id_releve_cf = %s" % (d.id_sheet, ids_statements[1])
            cursor = query_db(selectString)
            assertDict = {
                'id_releve_cf': lambda val: self.assertEqual(val,401382405),
                'id_nom': lambda val: self.assertEqual(val,2),
                'id_critere_cf': lambda val: self.assertEqual(val,2),
                'am': lambda val: self.assertEqual(val,0),
                'af': lambda val: self.assertEqual(val,2),
                'ai': lambda val: self.assertEqual(val,0),
                'na': lambda val: self.assertEqual(val,0),
                'sai': lambda val: self.assertEqual(val,0),
                'jeune': lambda val: self.assertEqual(val,0),
                'yearling': lambda val: self.assertEqual(val,0),
                'cd_ref_origine': lambda val: self.assertEqual(val,259),
                'nom_taxon_saisi': lambda val: self.assertEqual(val,'taxon 2'),
                'commentaire': lambda val: self.assertEqual(val,'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'),
                'supprime': lambda val: self.assertEqual(val,False),
                'prelevement': lambda val: self.assertEqual(val,False)
            }            
            for row in cursor.fetchall():
                data = zip([column[0] for column in cursor.description], row)
                for key, val in data:
                    assertDict[key](val)
                    
            
            # Observers
            for observer in inputData.observers_id:
                selectString = "SELECT count(*) FROM contactfaune.cor_role_fiche_cf WHERE id_cf = %s AND id_role = %s" % (d.id_sheet, observer)
                cursor = query_db(selectString)
                row = cursor.fetchone()
                self.assertEqual(row[0],1)

        finally:
            # At the end, remove inserted row in database
            deleteString = "DELETE FROM contactfaune.t_releves_cf WHERE id_cf = %s" % (d.id_sheet)
            query_db(deleteString)
            deleteString = "DELETE FROM contactfaune.t_fiches_cf WHERE id_cf = %s" % (d.id_sheet)
            query_db(deleteString)
            deleteString = "DELETE FROM contactfaune.cor_role_fiche_cf WHERE id_cf = %s and id_role in (%s)" % (d.id_sheet, ','.join(map(str, inputData.observers_id)))
            query_db(deleteString)
            commit_transaction()
            
            django.db.connections['default'] = old_db         
        
        
        
    #def test_export_sqlite(self):
    #    resp = self.client.post('/export/sqlite/', {'token': '666'})        
    #    self.assertEqual(resp.status_code, 200)
        
