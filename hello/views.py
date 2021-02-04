from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import QuerySet,Q
from django.shortcuts import redirect
from .forms import HelloForm,FriendForm,FindForm
from .models import Friend

def index(request):
    data=Friend.objects.all()
    prams={
        'title':'Hello',
        'data':data,
    }
    return render(request,'hello/index.html',prams)

#create model
def create(request):
    params={
        'title':'Hello',
        'form':HelloForm(),
    }
    if (request.method == 'POST'):
        name=request.POST['name']
        mail=request.POST['mail']
        gender='gender'in request.POST
        age=int(request.POST['age'])
        birth=request.POST['birthday']
        friend=Friend(name=name,mail=mail,gender=gender,age=age,birthday=birth)
        friend.save()
        return redirect(to='/hello')
    return render(request,'hello/create.html',params)

#update model
def edit(request,num):
    obj=Friend.objects.get(id=num)
    if(request.method == 'POST'):
        friend=FriendForm(request.POST,instance=obj)
        friend.save()
        return redirect(to='/hello')
    params={
        'title':'Hello',
        'id':num,
        'form':FriendForm(instance=obj),
    }
    return render(request,'hello/edit.html',params)

#delete model
def delete(request,num):
    friend=Friend.objects.get(id=num)
    if(request.method == 'POST'):
        friend.delete()
        return redirect(to='/hello')
    params={
        'title':'Hello',
        'id':num,
        'obj':friend,
    }
    return render(request,'hello/delete.html',params)

#find model
def find(request):
    if (request.method == 'POST'):
        form=FindForm(request.POST)
        find=request.POST['find']
        data=Friend.objects.filter(Q(name__contains=find)|Q(mail__contains=find))
        msg='Result: '+str(data.count())
    else: 
        msg='search words'
        form=FindForm()
        data=Friend.objects.all()
    params={
        'title':'Hello',
        'message':msg,
        'form':form,
        'data':data,
    }
    return render(request,'hello/find.html',params)
