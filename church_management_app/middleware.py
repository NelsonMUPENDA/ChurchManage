from django.contrib import messages
from django.shortcuts import redirect

from .permissions import has_permission, is_admin_user


class ActionPermissionMiddleware:
    """Applique les restrictions d'actions (view/create/edit/delete/search/filter/export/print)
    en fonction des permissions configurées par l'admin.

    Le menu reste géré par le rôle (ROLE_PERMISSIONS).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not is_admin_user(request.user):
            module, action = self._infer_module_action(request)
            if module and action:
                if not has_permission(request.user, module, action):
                    messages.error(request, "Vous n'avez pas la permission d'effectuer cette action.")
                    return redirect('dashboard')

        return self.get_response(request)

    def _infer_module_action(self, request):
        """Déduit (module, action) depuis le nom d'url et/ou la méthode HTTP."""
        match = getattr(request, 'resolver_match', None)
        url_name = getattr(match, 'url_name', None)
        if not url_name:
            return (None, None)

        # Pages toujours accessibles si l'utilisateur a le menu via son rôle.
        # On restreint surtout les actions métiers.
        if url_name in {'home', 'login', 'logout', 'dashboard', 'account', 'account-edit'}:
            return (None, None)

        special_route_map = {
            'finance-list': ('finances', 'create' if request.method == 'POST' else 'view'),
            'diaconat': ('diaconat', 'edit' if request.method == 'POST' else 'view'),
            'attendance-event': ('diaconat', 'edit' if request.method == 'POST' else 'view'),
            'event-logistics-list': ('logistics', 'view'),
            'logistics-category-ajax': ('logistics', 'create'),
            'logistics-condition-ajax': ('logistics', 'create'),
            'reports': ('reports', 'view'),
            'report-members-detail': ('reports', 'view'),
            'report-finances-detail': ('reports', 'view'),
            'report-activities-detail': ('reports', 'view'),
            'report-attendance-detail': ('reports', 'view'),
            'report-sacraments-detail': ('reports', 'view'),
            'reports-export-excel': ('reports', 'export'),
            'reports-export-pdf': ('reports', 'export'),
        }
        if url_name in special_route_map:
            return special_route_map[url_name]

        # Normaliser module depuis le prefix du nom d'URL
        module = None
        action = None

        # Helpers
        def action_from_name(name):
            if 'create' in name or name.endswith('-add'):
                return 'create'
            if 'edit' in name or 'update' in name:
                return 'edit'
            if 'delete' in name or 'remove' in name:
                return 'delete'
            if 'export' in name:
                return 'export'
            if 'print' in name:
                return 'print'
            if 'list' in name or 'detail' in name:
                return 'view'
            return None

        action = action_from_name(url_name)

        # Mapper quelques préfixes aux modules
        prefix_map = {
            'member': 'members',
            'family': 'families',
            'homegroup': 'home_groups',
            'department': 'departments',
            'ministry': 'ministries',
            'event': 'events',
            'attendance': 'attendance',
            'finance': 'finances',
            'transaction': 'finances',
            'category': 'finances',
            'announcement': 'announcements',
            'training': 'trainings',
            'logistics': 'logistics',
            'diaconat': 'diaconat',
            'baptism': 'baptisms',
            'evangelisation': 'evangelisation',
            'marriage': 'marriages',
            'document': 'documents',
            'contact': 'contacts',
            'notification': 'notifications',
            'approval': 'approvals',
            'audit': 'audit_logs',
            'reports': 'reports',
            'service': 'settings',
            'activity': 'settings',
            'church': 'settings',
            'user': 'account',
        }

        # Cas spéciaux : urls sous diaconat pour la logistique
        if url_name.startswith('diaconat-logistics') or url_name.startswith('event-logistics'):
            module = 'logistics'
        else:
            base = url_name.split('-', 1)[0]
            module = prefix_map.get(base)

        # Pour les endpoints ajax de création dynamique, les traiter comme create
        if url_name.startswith('ajax-'):
            # On n'applique pas de blocage automatique ici par défaut pour éviter de casser l'UI.
            return (None, None)

        # Si pas d'action détectée, fallback: GET= view, POST= edit/create selon url
        if module and not action:
            action = 'view' if request.method == 'GET' else 'edit'

        return (module, action)
