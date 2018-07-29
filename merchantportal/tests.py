from django.test import TestCase

# Create your tests here.
from .models import FoodAndBeveragesDealItem

class FoodAndBeveragesDealItemTest(TestCase):

	def setUp(self):
		FoodAndBeveragesDealItem.objects.create(di_item="Chocolate Donut",di_quantity="20 ",dil_price="360")
		FoodAndBeveragesDealItem.objects.create(di_item="Choco Shake",di_quantity="100 gm",dil_price="210")

	def test_deal_item(self):
		deal_item_choco_donut = FoodAndBeveragesDealItem.objects.get(di_item="Chocolate Donut")
		deal_item_choco_shake = FoodAndBeveragesDealItem.objects.get(di_item="Choco Shake")
		self.assertEqual(deal_item_choco_donut.get_deal_item_details(),"Chocolate Donut cost is 360 Rupees.")
		self.assertEqual(deal_item_choco_shake.get_deal_item_details(),"Choco Shake cost is 210 Rupees.")