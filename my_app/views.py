from django.shortcuts import render
from my_app.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def index(request):
    # if request.method == "GET":
    return render(request, 'my_app/index.html')


def register(request):
    registered = False

    if request.user.is_authenticated:
        return HttpResponseRedirect('/my_app/')

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

                profile.save()

                registered = True

                # return render(request, 'my_app/register.html', {
                #     'user_form': user_form,
                #     'profile_form': profile_form,
                #     'registered': registered,
                #     'user_form': UserForm(),
                #     'profile_form': UserProfileInfoForm()
                # })

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'my_app/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('../../my_app/')
    # return HttpResponseRedirect(reverse('index'))


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
