from django.shortcuts import render,HttpResponseRedirect
from .models import Post
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group

# Create your views here.
def home(request):
    posts=Post.objects.all()
    return render(request, 'blog/home.html',{'posts':posts})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user = request.user
        full_name=user.get_full_name()
        gps=user.groups.all()
        return render(request, 'blog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="Author")
            user.groups.add(group)
            messages.success(request,"Congratulation!! You have become an author ")
    else:
        form=SignUpForm()
    return render(request, 'blog/signup.html',{'form':form})

def user_login(request):
     if not request.user.is_authenticated:
        if request.method == "POST":
            form=LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                password=form.cleaned_data['password']
                user=authenticate(username=uname,password=password)
                if user is not None:
                    login(request,user)
                    messages.success(request,"You have successfully logged in")
                    return HttpResponseRedirect('/dashboard/')
                else:
                    messages.error(request,"Some thing went wrong")

        else:
            form=LoginForm()
        return render(request, 'blog/login.html',{'form':form})
     else:
         return HttpResponseRedirect('/dashboard/')
     
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form=PostForm(request.POST)
            if form.is_valid():
                # form.save()
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                pst=Post(title=title,desc=desc)
                pst.save()
                # it returns empty form
                form=PostForm()
        else:
            form=PostForm()
        return render(request, 'blog/addPost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


    

def update_post(request,id):

    if request.user.is_authenticated:
         if request.method == "POST":
             pi=Post.objects.get(pk=id)
             form=PostForm(request.POST,instance=pi)
             if form.is_valid():
                 form.save()
                 return HttpResponseRedirect('/dashboard/')
         else:
             pi=Post.objects.get(pk=id)
             form=PostForm(instance=pi)
         return render(request, 'blog/updatePost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/') 
    
def delete_post(request,id):
    if request.user.is_authenticated:
         if request.method == "POST":
             pi=Post.objects.get(pk=id)
             pi.delete()
         return HttpResponseRedirect('/dashboard/') 
    else:
        return HttpResponseRedirect('/login/') 

    

