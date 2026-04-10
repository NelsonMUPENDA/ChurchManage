from rest_framework.permissions import BasePermission

from rest_framework.permissions import SAFE_METHODS


def _department_name(user):
    try:
        member = getattr(user, 'member', None)
        if member and getattr(member, 'department', None):
            return (member.department.name or '').strip().lower()
    except Exception:
        return ''
    return ''


class RolePermission(BasePermission):
    allowed_roles = None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if getattr(request.user, 'is_staff', False):
            return True

        if self.allowed_roles is None:
            return True

        return getattr(request.user, 'role', None) in self.allowed_roles


class IsAdminOrSuperAdmin(RolePermission):
    allowed_roles = {'super_admin', 'pastor', 'admin', 'administrator'}


class IsSecretaryOrAdmin(RolePermission):
    allowed_roles = {'super_admin', 'pastor', 'admin', 'administrator', 'secretary', 'protocol_head'}


class IsTreasurerOrAdmin(RolePermission):
    allowed_roles = {'super_admin', 'pastor', 'admin', 'administrator', 'treasurer', 'financial_head'}


class IsDepartmentHeadOrAdmin(RolePermission):
    allowed_roles = {
        'super_admin',
        'pastor',
        'admin',
        'administrator',
        'department_head',
        'logistics_head',
        'evangelism_head',
    }


class IsLogisticsHeadOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if getattr(request.user, 'is_staff', False):
            return True

        role = getattr(request.user, 'role', None)
        if role in {'super_admin', 'pastor', 'admin', 'administrator'}:
            return True

        if role == 'logistics_head':
            return True

        if role != 'department_head':
            return False

        dep = _department_name(request.user)
        return ('logist' in dep) or ('logistique' in dep)


class IsEvangelismHeadOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if getattr(request.user, 'is_staff', False):
            return True

        role = getattr(request.user, 'role', None)
        if role in {'super_admin', 'pastor', 'admin', 'administrator'}:
            return True

        if role == 'evangelism_head':
            return True

        if role != 'department_head':
            return False

        dep = _department_name(request.user)
        return ('evang' in dep) or ('évang' in dep)


class IsAdminOrSuperAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if getattr(request.user, 'is_staff', False):
            return True

        return getattr(request.user, 'role', None) in {'super_admin', 'pastor', 'admin', 'administrator'}


class PublicReadAdminWrite(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if getattr(request.user, 'is_staff', False):
            return True

        return getattr(request.user, 'role', None) in {'super_admin', 'pastor', 'admin', 'administrator'}
