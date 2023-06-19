from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from .models import Room, Genre, Message
from .forms import Roomform


# rooms = [
#     {'id': 1, 'name': 'room1'},
#     {'id': 2, 'name': 'room2'},
#     {'id': 3, 'name': 'room3'},
# ]

def user_login(request):

    page = 'login_page'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Incorrect Username or Password!")

    context ={'page': page}
    return render(request, 'base/login_page.html',context)

def user_signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request,user)
            return redirect('home')

    context ={'form': form}
    return render(request, 'base/login_page.html',context)

def user_logout(request):
    logout(request)
    return redirect('user_login')

# @login_required(login_url='user_login')
def home(request):

    user = request.user

    if user.is_authenticated:
        pass
    else:
        return redirect('user_login')

    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else: q=''
    rooms =Room.objects.filter(
        Q(name__icontains=q) |
        Q(genre__name__icontains=q) |
        Q(description__icontains=q) 
        )
    genres = Genre.objects.all()
    rooms_count = rooms.count()
    context = {'rooms': rooms, 'genres': genres, 'rooms_count': rooms_count, 'user': user}
    return render(request, 'base/home.html', context )

def room(request, pk):

    user = request.user

    if user.is_authenticated:
        pass
    else:
        return redirect('user_login')

    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    if request.method == "POST":
        new_message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('room_message')
        )
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages}
    return render(request, 'base/room.html',context)

def createRoom(request):

    user = request.user

    if user.is_authenticated:
        pass
    else:
        return redirect('user_login')

    form = Roomform()
    if request.method == 'POST':
        form = Roomform(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host=user
            room.save()
            return redirect('home')

    context ={'form': form, 'user': user}
    return render(request, 'base/createRoom.html', context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = Roomform(instance=room)
    if request.method == 'POST':
        form = Roomform(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/createRoom.html', context)

def deleteRoom(request,pk):

    user = request.user

    if user.is_authenticated:
        pass
    else:
        return redirect('user_login')

    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'base/delete.html', context)