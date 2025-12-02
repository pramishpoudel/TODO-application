from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from  .models import TodoItem
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
def signup(request):
    if request.method == "POST":
        fnm = request.POST.get('fnm')
        email=request.POST.get('emailid')
        password = request.POST.get('pwd')
        my_user = User.objects.create_user(fnm,email,password)
        my_user.save()
        
    return render(request,'signup.html')


def logins(request):
    if request.method == "POST":
        fnm = request.POST.get('fnm')
        password = request.POST.get('pwd')
        my_user = authenticate(request,username=fnm,password=password)
        if my_user is not None:
            login(request,my_user)
            return redirect('/todo')
        else:
            return redirect('/logins')

    return render(request,"logins.html")


def todo(request):
    if request.method == "POST":
        title = request.POST.get('title')
        print(title)
        objs = TodoItem(title=title,user=request.user)
        objs.save()
        res = TodoItem.objects.filter(user=request.user).order_by('-date')
        return redirect('/todo',{'res':res})
    res = TodoItem.objects.filter(user=request.user).order_by('-date')
    return render(request,'todo.html',{'res':res})

def delete_todo(request,srno):
    print(srno)
    obj=TodoItem.objects.get(srno=srno)
    obj.delete()
    return redirect('/todo')

@login_required(login_url='/logins')
def edit_todo(request, srno):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj =  TodoItem.objects.get(srno=srno)
        obj.title = title
        obj.save()
        return redirect('/todo')

    obj = TodoItem.objects.get(srno=srno)
    return render(request, 'edit_todo.html', {'obj': obj})


def signout(request):
    logout(request)
    return redirect('/logins')

