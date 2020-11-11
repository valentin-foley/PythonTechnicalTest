from rest_framework import serializers
from bonds.models import Bond
from django.contrib.auth.models import User

class BondSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')
	class Meta:
		model = Bond
		fields = ['url', 'isin', 'size', 'currency', 'maturity', 'lei', 'owner', 'legal_name']

class UserSerializer(serializers.HyperlinkedModelSerializer):
	bonds = serializers.HyperlinkedRelatedField(many=True, view_name='bond-detail', read_only=True)
	
	class Meta:
		model = User
		fields = ['id', 'username', 'bonds']