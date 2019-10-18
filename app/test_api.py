import json
import unittest

from pos_microservice.pointOfSale.routes import pos
from pos_microservice import app


app.register_blueprint(pos)

app.testing = True
app_context = app.app_context()


class TestApi(unittest.TestCase):

    #test add pointOfSale
    def test_add_point_of_Sale(self):
        data = dict(designation='Carrefour Express Intilaka', localisation='36.839498,10.1177548',
                   address='Route Mnihla, CitÃ© Intilaka',
                    email='hadhemiwesleti@gmail.com', phone_number='16 70 248 248')

        with app.app_context():
            self.pointOfSale = app.test_client()

            response = self.pointOfSale.post('/addPointOfSale', data=json.dumps(data), content_type='application/json')

    #test delete pointOfSale
    def test_delete_pointOfSale(self):
        data = dict(list_id=1, enabled=True)
        with app.app_context():
            self.pointOfSale = app.test_client()
            response = self.pointOfSale.delete('/pointOfSale/<string:idPointOfSale>', data=json.dumps(data),
                                              content_type='application/json')

            self.assertEqual(response.status_code, 200)


     # Test: update pointOfSale

    def test_update_point_of_sale(self):
        data = dict(idPointOfSale=1, enabled=True)
        with app.app_context():
            self.pointOfSale = app.test_client()
            response = self.pointOfSale.put('/pointOfSale/<string:idPointOfSale>', data=json.dumps(data),
                                            content_type='application/json')
            self.assertEqual(response.status_code, 200)






    #test get all pointOfSale

    def test_get_points_of_Sal(self):
        with app.app_context():
            self.pointOfSale = app.test_client()
            response = self.pointOfSale.get(path='/pointsOfSale', content_type='application/json')
            self.assertEqual(response.status_code, 200)

    # test get single pointOfSale by designation

    def test_get_point_of_sale_designation(self):
        data = dict(designation='Carrefour Express Intilaka', enabled=True)
        with app.app_context():
            self.pointOfSale = app.test_client()
            response = self.pointOfSale.get('/pointOfSale/findOneByAddress/<string:designation>', data=json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 200)


    # test get single pointOfSale by address

    def test_get_point_of_sale_address(self):
        data = dict(address='Route Mnihla, CitÃ© Intilaka', enabled=True)
        with app.app_context():
            self.pointOfSale = app.test_client()
            response = self.pointOfSale.get('/pointOfSale/findOneByAddress/<string:address>', data=json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 200)



    # test get single pointOfSale by location

    def test_get_point_of_sale_localisation(self):
        data = dict(localisation='36.839498,10.1177548', enabled=True)
        with app.app_context():
            self.pointOfSale = app.test_client()
            response = self.pointOfSale.get('/pointOfSale/findOneByLocalisation/<string:localisation>', data=json.dumps(data),
                                            content_type='application/json')
            self.assertEqual(response.status_code, 200)









if __name__ == "__main__":
    unittest.main()
