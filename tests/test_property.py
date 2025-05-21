from odoo.tests.common import TransactionCase
from odoo import fields

class TestProperty(TransactionCase):

    def setUp(self,*args,**kwargs):
        super(TestProperty,self).setUp()

        self.property_01_record = self.env['property'].create({
            'ref' : 'PRT1000',
            'name': 'Luxury Apartment',
            'expected_price': 250000,
            'bedrooms': 3,
            'date_availability' : fields.Date.today()
            })

    def test_check_property_values(self):
        self.assertEqual(self.property_01_record.ref, 'PRT1000', "Property reference does not match")
        self.assertEqual(self.property_01_record.name, 'Luxury Apartment', "Property name does not match")
        self.assertEqual(self.property_01_record.excepted_price, 250000, "Property expected price does not match")
        self.assertEqual(self.property_01_record.bedrooms, 3, "Property bedrooms count does not match")
        self.assertEqual(self.property_01_record.date_availablity, fields.Date.today(), "Property availability date does not match")