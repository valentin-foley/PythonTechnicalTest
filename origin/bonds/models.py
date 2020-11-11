from django.db import models
import requests

class Bond(models.Model):
	isin = models.CharField(max_length=12)
	size = models.IntegerField()
	currency = models.CharField(max_length=3)
	maturity = models.CharField(max_length=10)
	lei = models.CharField(max_length=100)
	owner = models.ForeignKey('auth.User', related_name='bonds', on_delete=models.CASCADE)
	legal_name = models.CharField(max_length=100, default='')
	
	def save(self, *args, **kwargs):
		"""
		Use the gleif api to look up the lei of the bond
		"""
		lei = self.lei
		gleifdata = requests.get("https://leilookup.gleif.org/api/v2/leirecords?lei={}".format(lei))
		self.legal_name = gleifdata.json()[0]['Entity']['LegalName']['$']
		super(Bond, self).save(*args, **kwargs)
	
	class Meta:
		ordering = ['isin']