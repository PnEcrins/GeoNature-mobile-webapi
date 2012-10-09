import django
from django.test import TestCase


class FauneViewsTestCase(TestCase):
    def test_import(self):
        
        old_db = django.db.connections['default']
        django.db.connections['default'].settings_dict['NAME']
        try:
            #old_db = django.db.connections['default']
            django.db.connections['default'] = old_db.__class__(old_db.settings_dict)
            # you might want to print the settings dict to see what you need to update...
            django.db.connections['default'].settings_dict['NAME'] = real_db_name
            # test the db here
            
            data = open('faune/data.json').read()
            resp = self.client.post('/import/', {'data': data, 'token': '666'})

        finally:
            django.db.connections['default'] = old_db         
        

        # Check that data has been inserted
        #select dernier-releve from table_distante;
        
        # assertEqual ( data.animal, dernierreleve.animal)
        
        # at the end, remove inserted row in database
        
        
        self.assertEqual(resp.status_code, 200)
        
        
        
        
    #def test_export_sqlite(self):
    #    resp = self.client.post('/export/sqlite/', {'token': '666'})        
    #    self.assertEqual(resp.status_code, 200)
        
