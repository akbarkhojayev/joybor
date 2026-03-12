from rest_framework.permissions import BasePermission, IsAdminUser
from .models import *
from rest_framework.exceptions import PermissionDenied

class IsStudent(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and Student.objects.filter(user=request.user).exists()

class IsDormitoryAdmin(BasePermission):
    def has_permission(self,request,view):
        if not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
           has_dormitory = Dormitory.objects.filter(admin=request.user).exists()
           if not has_dormitory:
               raise PermissionDenied
           return True
        return False

class IsOwnerOrIsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (request.user.is_superuser or obj.admin == request.user)


class IsAdminOrDormitoryAdmin(BasePermission):
    def has_permission(self, request, view):
        return IsAdminUser().has_permission(request, view) or IsDormitoryAdmin().has_permission(request, view)

class IsFloorLeader(BasePermission):
    """Qavat sardori (Floor Leader) uchun permission"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # User role 'sardor' bo'lishi va FloorLeader yozuvi bo'lishi kerak
        if hasattr(request.user, 'role') and request.user.role == 'sardor':
            return FloorLeader.objects.filter(user=request.user).exists()
        
        return False


class IsAdminOrFloorLeader(BasePermission):
    """Admin yoki Qavat sardori uchun permission"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin yoki Sardor
        if request.user.is_superuser:
            return True
        
        if hasattr(request.user, 'role'):
            if request.user.role == 'admin':
                return Dormitory.objects.filter(admin=request.user).exists()
            elif request.user.role == 'sardor':
                return FloorLeader.objects.filter(user=request.user).exists()
        
        return False
