from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, force_authenticate
from bonds.models import Bond

class BondTestCase(APITestCase):
	def setUp(self):
		self.username = 'dummy_user'
		self.password = 'dummy_pass'
		self.user = User.objects.create(
			username=self.username,
			password = self.password
		)
		self.client.force_authenticate(user=self.user)
		
	def test_legal_name(self):
		self.client.login(
			username=self.username,
			password=self.password
		)
		response = self.client.post(
			'/bonds/',
			{
				'isin': 'XS2245555045',
				'size': 100000000,
				'currency': 'HKD',
				'maturity': '2020-12-07',
				'lei': '254900R882POXXVAK772'
			},
			format='json'
		)
		self.assertEqual(response.data['legal_name'], 'UBS AG')
		self.assertEqual(response.status_code, 201)
	
	def test_name_filter(self):
		self.client.login(
			username=self.username,
			password=self.password
		)
		self.client.post(
			'/bonds/',
			{
				'isin': 'FR0000131104',
				'size': 100000000,
				'currency': 'EUR',
				'maturity': '2025-02-28',
				'lei': 'R0MUWSFPU8MPRO8K5P83'
			},
			format='json'
		)
		self.client.post(
			'/bonds/',
			{
				'isin': 'XS2245555045',
				'size': 100000000,
				'currency': 'HKD',
				'maturity': '2020-12-07',
				'lei': '254900R882POXXVAK772'
			},
			format='json'
		)
		self.client.post(
			'/bonds/',
			{
				'isin': 'XS2190784715',
				'size': 100000000,
				'currency': 'JPY',
				'maturity': '2021-05-11',
				'lei': 'E58DKGMJYYYJLN8C3868'
			},
			format='json'
		)
		names = ['BNP PARIBAS', 'UBS AG', 'CREDIT SUISSE INTERNATIONAL']
		for name in names:
			response = self.client.get('http://127.0.0.1:8000/bonds/?legal_name={}'.format(name))
			for result in response.json()['results']:
				self.assertEqual(result['legal_name'], name)