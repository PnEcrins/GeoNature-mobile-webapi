
from django.test import TestCase


class FauneViewsTestCase(TestCase):
    def test_import(self):
        
        data = open('faune/data.json').read()
        resp = self.client.post('/import/', {'data': data, 'token': '666'})

        # Check that data has been inserted
        #select dernier-releve from table_distante;
        
        # assertEqual ( data.animal, dernierreleve.animal)
        
        # at the end, remove inserted row in database
        
        
        self.assertEqual(resp.status_code, 200)
        
        
        
    #def test_export_sqlite(self):
    #    resp = self.client.post('/export/sqlite/', {'token': '666'})        
    #    self.assertEqual(resp.status_code, 200)
        
