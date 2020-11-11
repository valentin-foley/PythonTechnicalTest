from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from bonds.models import Bond
from bonds.serializers import BondSerializer
from bonds.permissions import IsOwner


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'bonds': reverse('bond-list', request=request, format=format)
	})

class BondViewSet(viewsets.ModelViewSet):
	serializer_class = BondSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwner]
	
	def get_queryset(self):
		queryset = Bond.objects.filter(owner=self.request.user)
		legal_name = self.request.query_params.get('legal_name', None)
		if legal_name is not None:
			queryset = queryset.filter(legal_name=legal_name)
		return queryset
	
	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)