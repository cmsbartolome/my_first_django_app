from django.shortcuts import render
from my_app.forms import UserForm, UserProfileInfoForm, NotesForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from my_app.models import *
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def index(request):
    notes = Notes.objects.all()
    return render(request, 'my_app/index.html', {'notes': notes})


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/my_app/')

    if request.method == 'POST':
        err_msg = ''
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == '' or password == '':
            err_msg = 'Please enter your username and password'

            return render(request, 'my_app/login.html', {'err': err_msg})

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../../my_app/')

            else:
                err_msg = 'Account is inActive'
                return render(request, 'my_app/login.html', {'err': err_msg})
                # return HttpResponse('Account not active')

        else:
            # print("Someone tried to login and failed")
            # print("Username: {} and password {}".format(username, password))
            err_msg = 'Login failed!. Invalid username or password'

            return render(request, 'my_app/login.html', {'err': err_msg})
            # return HttpResponse('Login failed')

    else:
        err_msg = ''
        return render(request, 'my_app/login.html', {'err_msg': err_msg})


def register(request):
    registered = False

    if request.user.is_authenticated:
        return HttpResponseRedirect('/my_app/')

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # if user_form.is_valid() and profile_form.is_valid():
        if user_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # profile = profile_form.save(commit=False)
            # profile.user = user

            # if 'profile_pic' in request.FILES:
            #     profile.profile_pic = request.FILES['profile_pic']
            #     profile.save()
            registered = True

            messages.success(request, 'Registered successfully.')
            return HttpResponseRedirect('/my_app/register')

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'my_app/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('../../my_app/')
    # return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    user = get_object_or_404(User, id=request.user.id)

    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        password = request.POST.get('password')
        old_password = request.POST.get('old_password')

        if (request.POST.get('first_name') == "" or request.POST.get('last_name') == ""):
            err_msg = 'Please enter your Firstname and Lastname'
            return render(request, 'my_app/profile.html', {'err': err_msg})

        # if (request.POST.get('password') == ""):
        #     password = user.password

        if (request.POST.get('password') != ""):
            if (request.POST.get('password') != request.POST.get('confirm_password')):
                err_msg = 'Password confirmation do not match'
                return render(request, 'my_app/profile.html', {'err': err_msg})

            if (user.check_password(old_password) == False):
                err_msg = 'Old password do not match'
                return render(request, 'my_app/profile.html', {'err': err_msg})

            # else:
            #     password = user.set_password(password)

        user.first_name = firstname
        user.last_name = lastname

        if (request.POST.get('password') != ""):
            user.password = make_password(password)
        user.save()

        success_msg = 'Profile updated successfully'
        return render(request, 'my_app/profile.html', {'user': user, 'suc': success_msg})

    return render(request, 'my_app/profile.html', {'user': user})


@login_required
def createNotes(request):

    if request.method == 'POST':
        notes_form = NotesForm(data=request.POST)

        if notes_form.is_valid():
            created_by = get_object_or_404(User, id=request.user.id)
            instance = notes_form.save(commit=False)
            instance.createdBy = created_by
            instance.save()

            messages.success(request, 'Notes added Successfully.')
            return HttpResponseRedirect('/my_app/register')

    notes_form = NotesForm()
    return render(request, 'my_app/add_notes.html', {'notes_form': notes_form})


@login_required
def createNotes(request):

    if request.method == 'POST':
        notes_form = NotesForm(data=request.POST)

        if notes_form.is_valid():
            created_by = get_object_or_404(User, id=request.user.id)
            instance = notes_form.save(commit=False)
            instance.createdBy = created_by
            instance.save()

            messages.success(request, 'Notes added Successfully.')
            return HttpResponseRedirect('/my_app/add_notes')

    notes_form = NotesForm()
    return render(request, 'my_app/add_notes.html', {'notes_form': notes_form})


def updateNotes(request, pk):
    # notes = Notes.objects.get(id=pk)
    notes = get_object_or_404(Notes, id=pk)
    notes_form = NotesForm(instance=notes)

    if request.method == 'POST':
        notes_form = NotesForm(data=request.POST, instance=notes)

        if notes_form.is_valid():
            updated_on = datetime.now()
            instance = notes_form.save(commit=False)
            instance.updatedOn = updated_on
            instance.save()

        messages.success(request, 'Notes updated Successfully.')
        return HttpResponseRedirect('/my_app/update_notes/'+pk)

    return render(request, 'my_app/update_notes.html', {'notes_form': notes_form})


def deleteNotes(request, pk):
    # notes = Notes.objects.get(id=pk)
    notes = get_object_or_404(Notes, id=pk)
    item = notes

    if request.method == 'POST':
        notes.delete()

        return HttpResponseRedirect('/my_app/')

    return render(request, 'my_app/delete_notes.html', {'item': item})
