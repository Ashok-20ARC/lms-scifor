from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    allowed_roles=[]

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in self.allowed_roles

class IsStudent(RolePermission):
    """Allows access only to authenticated users with the role 'student'."""
    allowed_roles=['student']

class IsStaff(RolePermission):
    """Allows access only to authenticated users with the role 'staff'."""
    allowed_roles=['staff']

class IsAdmin(RolePermission):
    """Allows access only to authenticated users with the role 'admin'."""
    allowed_roles=['admin']

class IsEmailVerified(BasePermission):
    """Allows access only if user's email is verified."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active