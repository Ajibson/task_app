from django.shortcuts import render,redirect
from django.urls import reverse
from .models import *
from .forms import *
from django.core.mail import send_mail,BadHeaderError
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User  
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from datetime import timedelta

def signup(request):
    if request.method == 'POST':
        form = user_signup(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(username = username, email = email, password=password)
            user.is_active = False
            user.save()
            email_template_name = "events/acc_active_email.html"
            subject = "Account Acctivation"
            c = {
                    "email":form.cleaned_data.get('email'),
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Event Planner',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, 'myvtuservice@gmail.com' , [str(form.cleaned_data.get('email'))], fail_silently=False)
                return render(request, 'events/account_confirmation_sent.html')
            except BadHeaderError:
                #messages.error(request, 'please try again')
                form = user_signup() 
                context = {
                     'form':form
                    }
                return render(request, 'events/signup.html', context = context)
    else:  
        form = user_signup() 
    context = {
        'form':form
    }
    return render(request, 'events/signup.html', context = context)

def activate(request, uidb64, token):  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(id=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None:  
        user.is_active = True  
        user.save()  
        return render(request, 'events/account_confirmed.html') 
    else:  
        print('last')
        return HttpResponse('Activation link is invalid!')

def Login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username, password)
            #user = authenticate(username, password)
            user = authenticate(
                    request, 
                    username = form.cleaned_data.get('username'),
                    password = form.cleaned_data.get('password')
                    )
            print(user)
            if user is None:
                messages.error(request, "Wrong username or password")
                msg = 'Wrong username or password'
                return render(request, 'events/login.html', {'form':form, 'msg':msg})
            else:
                login(request, user)
                return redirect('home')
    else:
        form = loginForm()
        return render(request, 'events/login.html', {'form':form})
            
@login_required
def home(request):
    tasks = task.objects.filter(user = request.user).order_by('-due_at')
    now = timezone.now() + timedelta(hours = 1)
    if now.hour < 12:
        greetings = 'Good Morning'
    elif now.hour >= 12 and now.hour < 18:
        greetings = 'Good Afternoon'
    else:
        greetings = 'Good Evening'
    if request.method == 'POST':
        form = taskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added successfully')
            return redirect('home')
    else:
        form = taskForm()
    context = {
        'tasks':tasks, 'form':form, 'greetings':greetings
    }
    return render(request, 'events/home.html', context = context)

def profile_update(request):
    if request.method == 'POST':
        form = usersForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            db_user = User.objects.get(username = request.user.username)
            db_user.username = username
            db_user.email = email
            db_user.save()
            messages.success(request, 'profile updated successfully')
            return redirect('home')
    return redirect('home')



@login_required
def update_task(request, task_no):
    try:
        get_task = task.objects.get(pk = task_no)
        due_at_bf = get_task.due_at
        form = taskForm(instance=get_task)
        if request.method == 'POST':
            form = taskForm(request.POST, instance=get_task)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                completed = form.cleaned_data.get('completed')
                due_at = form.cleaned_data.get('due_at')
                percentage_completed = form.cleaned_data.get('percentage_completed')
                if due_at is None:
                    due_at = due_at_bf
                if completed == True and int(percentage_completed) < 100:
                    percentage_completed = 100
                save_task = form.save(commit = False)
                save_task.due_at = due_at
                save_task.percentage_completed = percentage_completed
                save_task.save()
                messages.success(request, 'Task updated successfully')
                return redirect("home")
    except task.DoesNotExist:
        return redirect('home')
    context = {
        'task':get_task, 'form':form
    }
    return render(request, 'events/update_task.html', context = context)

@login_required
def delete_task(request, task_no):
    get_task = task.objects.get(pk = task_no)
    form = taskForm(instance=get_task)
    if request.method == 'POST':
        task_to_delete = task.objects.get(pk = task_no)
        task_to_delete.delete()
        messages.success(request, 'Task deleted successfully')
        return redirect("home")
    context = {
        'task':get_task, 'form':form
    }
    return render(request, 'events/delete_task.html',  context = context)

@login_required
def task_reminder(request, task_no):
    get_task = task.objects.get(pk = task_no)
    task_list = task.objects.all()
    form = taskForm(instance=get_task)
    if request.method == 'POST':
        form = taskForm(request.POST, instance=get_task)
        form.save()
        return redirect("home")
    context = {
        'task':task_list, 'form':form
    }
    return render(request, 'events/home.html',  context = context)



#Password reset function

def password_reset_request(request):
    if request.method == "POST":
        form = ResetForms(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            associated_users = User.objects.filter(Q(email=user_email))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.html"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Event Planner',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'myvtuservice@gmail.com' , [user.email], fail_silently=False)
                        return redirect("password_reset_done")
                    except BadHeaderError:
                        messages.error(request, 'please try again')
                        return redirect('reset_password')
            else:
                messages.error(request, 'The email is not registered')
                return redirect('reset_password')                         
    else:
        form = ResetForms()
    return render(request, "registration/password_reset_form.html", {"password_reset_form":form})

def password_reset_confirm(request,uidb64,token):
    user_pk = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=user_pk)
    if request.method == 'POST':
        form = NewPasswordResetForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            user.set_password(password1)
            user.save()
            return redirect('password_reset_complete')
    else:
        form = NewPasswordResetForm()
    return render(request, 'registration/password_reset_confirm.html', {'form':form}) 