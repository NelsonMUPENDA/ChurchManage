# views_user_management.py - Gestion des utilisateurs système
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q

from .forms import UserCreateForm, UserUpdateForm
from .permissions import admin_required

User = get_user_model()


@login_required
@admin_required
def user_management(request):
    """Liste et gestion des utilisateurs du système"""
    users = User.objects.all().order_by('-date_joined')
    
    # Recherche
    search = request.GET.get('q', '')
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    # Filtre par rôle
    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(role=role_filter)
    
    context = {
        'users': users,
        'search': search,
        'role_filter': role_filter,
        'active_page': 'account',
        'view': 'user_management',
        'role_choices': User.ROLE_CHOICES,
    }
    return render(request, 'dashboard/account.html', context)


@login_required
@admin_required
def user_create_admin(request):
    """Créer un nouvel utilisateur système"""
    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            # Récupérer le mot de passe avant de sauvegarder
            password = form.cleaned_data.get('password1')
            user = form.save()
            # Stocker l'ID utilisateur et le mot de passe en session pour l'afficher une fois
            request.session['new_user_id'] = user.pk
            request.session['new_user_password'] = password
            messages.success(request, f'Utilisateur {user.get_full_name()} créé avec succès!')
            return redirect('user-created-success')
    else:
        form = UserCreateForm()
    
    context = {
        'form': form,
        'action': 'Créer',
        'active_page': 'account',
        'view': 'user_form',
    }
    return render(request, 'dashboard/account.html', context)


@login_required
@admin_required
def user_created_success(request):
    """Afficher les informations de connexion après création d'utilisateur"""
    user_id = request.session.get('new_user_id')
    password = request.session.get('new_user_password')
    
    if not user_id or not password:
        messages.warning(request, 'Session expirée ou accès non autorisé.')
        return redirect('user-management')
    
    new_user = get_object_or_404(User, pk=user_id)
    
    context = {
        'new_user': new_user,
        'new_password': password,
        'active_page': 'account',
        'view': 'user_created',
    }
    
    # Supprimer les données de session après affichage (pour ne pas les afficher à nouveau)
    # Mais on les garde pour cette requête seulement
    del request.session['new_user_id']
    del request.session['new_user_password']
    
    return render(request, 'dashboard/account.html', context)


@login_required
@admin_required
def user_edit_admin(request, pk):
    """Modifier un utilisateur système (rôle et statut)"""
    target_user = get_object_or_404(User, pk=pk)
    
    # Empêcher la modification de soi-même via cette vue
    if target_user == request.user:
        messages.warning(request, 'Utilisez "Mon compte" pour modifier votre profil.')
        return redirect('user-management')
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=target_user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Utilisateur {target_user.get_full_name()} modifié avec succès!')
            return redirect('user-management')
    else:
        form = UserUpdateForm(instance=target_user)
    
    context = {
        'form': form,
        'target_user': target_user,
        'action': 'Modifier',
        'active_page': 'account',
        'view': 'user_form',
    }
    return render(request, 'dashboard/account.html', context)


@login_required
@admin_required
def user_delete_admin(request, pk):
    """Supprimer un utilisateur système"""
    target_user = get_object_or_404(User, pk=pk)
    
    # Empêcher l'auto-suppression
    if target_user == request.user:
        messages.error(request, 'Vous ne pouvez pas supprimer votre propre compte.')
        return redirect('user-management')
    
    # Empêcher la suppression d'un superadmin
    if target_user.is_superuser:
        messages.error(request, 'Impossible de supprimer un super administrateur.')
        return redirect('user-management')
    
    if request.method == 'POST':
        name = target_user.get_full_name()
        target_user.delete()
        messages.success(request, f'Utilisateur {name} supprimé avec succès!')
        return redirect('user-management')
    
    context = {
        'target_user': target_user,
        'active_page': 'account',
        'view': 'user_delete',
    }
    return render(request, 'dashboard/account.html', context)


@login_required
@admin_required
def user_toggle_active(request, pk):
    """Activer/Désactiver un utilisateur"""
    target_user = get_object_or_404(User, pk=pk)
    
    if target_user == request.user:
        messages.error(request, 'Vous ne pouvez pas désactiver votre propre compte.')
        return redirect('user-management')
    
    if target_user.is_superuser:
        messages.error(request, 'Impossible de modifier le statut d\'un super administrateur.')
        return redirect('user-management')
    
    target_user.is_active = not target_user.is_active
    target_user.save()
    
    status = 'activé' if target_user.is_active else 'désactivé'
    messages.success(request, f'Utilisateur {target_user.get_full_name()} {status}.')
    return redirect('user-management')
