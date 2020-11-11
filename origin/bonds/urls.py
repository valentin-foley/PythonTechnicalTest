from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from bonds.views import BondViewSet, api_root



bond_list = BondViewSet.as_view({
	'get': 'list',
	'post': 'create',
})

bond_detail = BondViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy',
})
"""
user_list = UserViewSet.as_view({
	'get': 'list',
})

user_detail = UserViewSet.as_view({
	'get': 'retrieve'
})
"""
urlpatterns = format_suffix_patterns([
	path('', api_root),
	path('bonds/', bond_list, name='bond-list'),
	path('bonds/<int:pk>/', bond_detail, name='bond-detail'),
	path('login/', include('rest_framework.urls')),
])