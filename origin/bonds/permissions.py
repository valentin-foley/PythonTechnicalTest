from rest_framework import permissions

class IsOwner(permissions.BasePermission):
	"""
	Only allow owner of object to view or edit
	"""
	
	def has_object_permission(self, request, view, obj):
		return obj.owner == request.user