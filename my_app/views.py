from django.shortcuts import render
from my_app.forms import UserForm, UserProfileInfoForm, NotesForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from my_app.models import *
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q, Exists, OuterRef
from django.core import serializers 
from my_app.serializers import NoteSerializer


def index(request):
    if request.user.is_authenticated:
        keyword = request.GET.get('search') or ''

        if (keyword != ''):
            q_object = Q(owner=request.user.id) and Q(title__icontains=keyword) | Q(status__icontains=keyword) | Q(description__icontains=keyword) | Q(id__icontains=keyword) | Q(owner__username=keyword) | Q(owner__first_name=keyword) | Q(owner__last_name=keyword)
            notes_list = Notes.objects.filter(q_object)
        else:
            notes_list = Notes.objects.filter(owner=request.user.id)

        # notes_list = Notes.objects.get_queryset().order_by('id')
        page = request.GET.get('page', 1)

        paginator = Paginator(notes_list, 5)
        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            notes = paginator.page(1)
        except EmptyPage:
            notes = paginator.page(paginator.num_pages)
    else:
        notes = Notes.objects.all()
        keyword = ''

    return render(request, 'my_app/index.html', {'notes': notes, 'query':keyword})


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

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../../my_app/')

            else:
                err_msg = 'Account is in-active'
                return render(request, 'my_app/login.html', {'err': err_msg})
                # return HttpResponse('Account not active')

        else:
            # print("Username: {} and password {}".format(username, password))
            err_msg = 'Login failed'

            return render(request, 'my_app/login.html', {'err': err_msg})
            # return HttpResponse('Login failed')

    else:
        return render(request, 'my_app/login.html')


def register(request):
    registered = False

    if request.user.is_authenticated:
        return HttpResponseRedirect('/my_app/')

    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')
        portfolio = request.POST.get('portfolio_site')
        hasErrors = False

        if (firstname == ""):
            hasErrors = True
            messages.error(request, 'Firstname is required')

        if (firstname.isalpha is False):
            hasErrors = True
            messages.error(request, 'Firstname should contains letters only')

        if (lastname == ""):
            hasErrors = True
            messages.error(request, 'Lastname is required')

        if (lastname.isalpha is False):
            hasErrors = True
            messages.error(request, 'Lastname should contains letters only')
        
        if (email == ""):
            hasErrors = True
            messages.error(request, 'Email address is required')

        if (password == ""):
            hasErrors = True
            messages.error(request, 'Password is required')

        if password and len(password) < 9:
            hasErrors = True
            messages.error(request, 'Password length must be 10 characters long')

        if (conf_password == ""):
            hasErrors = True
            messages.error(request, 'Password confirmation is required')
        
        if (portfolio == ""):
            hasErrors = True
            messages.error(request, 'Portfolio site address is required')
        
        if (password and password != conf_password):
            hasErrors = True
            messages.error(request, 'Password confirmation do not match')
        
        if (email and User.objects.filter(email=email)):
            hasErrors = True
            messages.error(request, 'Email already exist')
        
        if (username and User.objects.filter(username=username)):
            hasErrors = True
            messages.error(request, 'Username already exist')

        if (hasErrors is True):
            return render(request, 'my_app/register.html', {'registered': registered})
    
        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        #user.set_password(user.password)
        user.save()

        profile = UserProfileInfo.objects.create()
        profile.portfolio_site = portfolio
        profile.user = user

        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
           
        profile.save()
        registered = True

        messages.success(request, 'Registered successfully.')

        return render(request, 'my_app/register.html', {'registered': registered})
        #return HttpResponseRedirect('/my_app/register')

    else:
        return render(request, 'my_app/register.html', {'registered': registered})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('../../my_app/')
    # return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    user = get_object_or_404(User, id=request.user.id)
    user_info = get_object_or_404(UserProfileInfo, user_id=request.user.id)

    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        password = request.POST.get('password')
        old_password = request.POST.get('old_password')
        portfolio = request.POST.get('portfolio_site')

        if (firstname == ""):
            err_msg = 'Firstname is required'
            return render(request, 'my_app/profile.html', {'user': user, 'user_info':user_info,'err': err_msg})
        
        if (lastname  == ""):
            err_msg = 'Lastname is required'
            return render(request, 'my_app/profile.html', {'user': user, 'user_info':user_info,'err': err_msg})
        
        if (portfolio == ""):
            err_msg = 'Portfolio is required'
            return render(request, 'my_app/profile.html', {'user': user, 'user_info':user_info,'err': err_msg})

        if (request.POST.get('password') != ""):
            if (request.POST.get('password') != request.POST.get('confirm_password')):
                err_msg = 'Password confirmation do not match'
                return render(request, 'my_app/profile.html', {'user': user, 'user_info':user_info,'err': err_msg})

            if (user.check_password(old_password) == False):
                err_msg = 'Old password do not match'
                return render(request, 'my_app/profile.html', {'user': user, 'user_info':user_info,'err': err_msg})

        user.first_name = firstname
        user.last_name = lastname

        if (request.POST.get('password') != ""):
            user.password = make_password(password)
        user.save()
        update_session_auth_hash(request, user)

        user_info.portfolio_site = portfolio

        if 'profile_pic' in request.FILES:
            user_info.profile_pic = request.FILES['profile_pic']
           
        user_info.save()

        success_msg = 'Profile updated successfully'
        return render(request, 'my_app/profile.html', {'user': user, 'user_info':user_info, 'suc': success_msg})

    return render(request, 'my_app/profile.html', {'user': user, 'user_info': user_info})


@login_required
def createNotes(request):

    if request.method == 'POST':
        notes_form = NotesForm(data=request.POST)
        print(request.POST)

        if notes_form.is_valid():
            created_by = get_object_or_404(User, id=request.user.id)
            instance = notes_form.save(commit=False)
            instance.owner = created_by
            instance.save()

            messages.success(request, 'Notes added Successfully.')
            return HttpResponseRedirect('/my_app/add_notes')

    notes_form = NotesForm()
    return render(request, 'my_app/add_notes.html', {'notes_form': notes_form})

@login_required
def updateNotes(request, pk):
    # notes = Notes.objects.get(id=pk)
    # Notes.objects.filter(id=pk)
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

@login_required
def deleteNotes(request, pk):
    # notes = Notes.objects.get(id=pk)
    # Notes.objects.filter(id=pk)
    notes = get_object_or_404(Notes, id=pk)
    item = notes

    if request.method == 'POST':
        notes.delete()

        return HttpResponseRedirect('/my_app/')

    return render(request, 'my_app/delete_notes.html', {'item': item})



def getData(request):
    if request.user.is_authenticated:
        notes = Notes.objects.all().filter(owner=request.user.id).order_by('-createdOn')[:5]

    return render(request, 'my_app/load_more.html', {'notes': notes})


def loadMore(request):
    if request.user.is_authenticated:
        offset = int(request.POST['offset'])
        limit = 5

        notes = Notes.objects.filter(owner=request.user.id).order_by('-createdOn')[offset:limit+offset]
        totalData = Notes.objects.filter(owner=request.user.id).count()
        #jsonData=serializers.serialize('json', notes)
        serializer = NoteSerializer(notes, many=True)

        if notes is not None:
            data = {
                'notes':serializer.data,
                'totalResult': totalData,
                'offset': offset
            }

            return JsonResponse(data, safe=False, status=200)
