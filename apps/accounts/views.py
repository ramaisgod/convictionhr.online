from django.shortcuts import render, HttpResponseRedirect, HttpResponse, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .forms import *
from .models import User, ROLE_CHOICES
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.dashboard.views import my_dashboard


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        path = request.META['HTTP_REFERER']
        if user:
            login(request, user)
            # messages.success(request, "Login Success !!!")
            try:
                main_url = request.META['HTTP_ORIGIN']
                if not path == main_url + "/":
                    return HttpResponseRedirect(path)
                else:
                    return HttpResponseRedirect(reverse(home_page))
            except:
                return HttpResponseRedirect(reverse(home_page))
        else:
            messages.warning(request, "Invalid Credential !!!")
            try:
                return HttpResponseRedirect(path)
            except:
                return HttpResponseRedirect(reverse(home_page))
    return render(request, 'accounts/login.html', {})


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logout Successfully !!!")
        return HttpResponseRedirect(reverse(login_page))
    return HttpResponseRedirect(reverse(login_page))


@login_required
def change_password(request):
    if request.method == 'POST':
        new_pass1 = request.POST['newPassword1']
        new_pass2 = request.POST['newPassword2']
        if len(new_pass1) < 8:
            msg = "Password length should be minimum 8  !!!"
            messages.warning(request, msg)
            return render(request, 'accounts/change_password.html', {})
        if new_pass1 != new_pass2:
            msg = "Confirm Password does not match !!!"
            messages.warning(request, msg)
            return render(request, 'accounts/change_password.html', {})
        obj_User = User.objects.get(id=request.user.id)
        obj_User.set_password(new_pass1)
        obj_User.save()
        messages.success(request, "Password changed successfully. Please login with new password.")
        return HttpResponseRedirect(reverse(home_page))
    return render(request, 'accounts/change_password.html', {})


@login_required
def reset_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        obj_User = User.objects.filter(username=username)
        if len(obj_User) <= 0:
            msg = "Invalid username !!!"
            messages.warning(request, msg)
            return render(request, 'accounts/reset_password.html', {})
        obj_User = User.objects.get(username=username)
        default_password = "Welcome@" + str(username)
        obj_User.set_password(default_password)
        obj_User.save()
        messages.success(request, "Password reset successfully.")
        # return HttpResponseRedirect(reverse(home_page))
        return render(request, 'accounts/reset_password.html', {})
    return render(request, 'accounts/reset_password.html', {})


@login_required
def create_user(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            roles = form.cleaned_data['roles']
            # Check if username already exist
            usernameCount = User.objects.filter(username=username).count()
            emailCount = User.objects.filter(email=email).count()
            if usernameCount > 0:
                msg = "Username already exists !!!"
                messages.warning(request, msg)
                form = UserForm(request.POST)
                return render(request, 'accounts/create_user.html', {'form': form})
            if emailCount > 0:
                msg = "Email already exists !!!"
                messages.warning(request, msg)
                form = UserForm(request.POST)
                return render(request, 'accounts/create_user.html', {'form': form})
            obj.save()
            default_password = "Welcome@"+str(username)
            obj.set_password(default_password)
            obj.roles = roles
            obj.save()
            messages.success(request, "User account has been created successfully !!!")
            form = UserForm()
            return render(request, 'accounts/create_user.html', {'form': form})
        else:
            form = UserForm(request.POST)
            messages.warning(request, form.errors)
            return render(request, 'accounts/create_user.html', {'form': form})
    return render(request, 'accounts/create_user.html', {'form': form})


@login_required
def home_page(request):
    if request.user.user_type == 2:
        return render(request, 'layouts/customer/index.html', context={})
    elif request.user.user_type == 3:
        return HttpResponseRedirect(reverse(my_dashboard))
        # return render(request, 'accounts/index.html', context={})
    else:
        return render(request, 'layouts/candidate/index.html', context={})


@login_required
def emp_page(request):
    return render(request, 'accounts/index.html', context={})


@login_required
def user_roles(request):
    form = UserRoleForm()
    if request.method == 'POST':
        username = request.POST['username']
        user_roles = request.POST['roles']
        obj = User.objects.get(username=username)
        # obj.roles.add(*user_roles)
        # obj.roles.add(user_roles)
        obj.roles = user_roles
        obj.save()
        messages.success(request, "User roles has been updated !!!")
        form = UserRoleForm()
        return render(request, 'accounts/user_roles.html', {'form': form})
    else:
        form = UserRoleForm()
        return render(request, 'accounts/user_roles.html', {'form': form})


@login_required
def all_users(request):
    obj_user = User.objects.all().order_by('-last_login')
    role_dict = dict(ROLE_CHOICES)
    user_count = len(obj_user)
    page = request.GET.get('page', 1)
    paginator = Paginator(obj_user, 10)
    try:
        obj_user = paginator.page(page)
    except PageNotAnInteger:
        obj_user = paginator.page(1)
    except EmptyPage:
        obj_user = paginator.page(paginator.num_pages)
    return render(request, 'accounts/all_users.html', {'obj_user': obj_user, 'user_count': user_count, 'role_dict': role_dict})


@login_required
def online_users(request):
    role_dict = dict(ROLE_CHOICES)
    sessions = Session.objects.filter(expire_date__gte=now())
    user_list = []
    for session in sessions:
        data = session.get_decoded()
        user_list.append(data.get('_auth_user_id', None))
    obj_user = User.objects.filter(id__in=user_list).order_by('-last_login')
    user_count = len(obj_user)
    page = request.GET.get('page', 1)
    paginator = Paginator(obj_user, 10)
    try:
        obj_user = paginator.page(page)
    except PageNotAnInteger:
        obj_user = paginator.page(1)
    except EmptyPage:
        obj_user = paginator.page(paginator.num_pages)
    return render(request, 'accounts/online_users.html', {'obj_user': obj_user, 'user_count': user_count, 'role_dict': role_dict})



