from django.shortcuts import render,redirect
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
                return HttpResponse('Please confirm your email address to complete the registration')
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
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
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
    tasks = task.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = taskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = taskForm()
    context = {
        'tasks':tasks, 'form':form
    }
    return render(request, 'events/home.html', context = context)

@login_required
def update_task(request, task_no):
    try:
        get_task = task.objects.get(pk = task_no)
        form = taskForm(instance=get_task)
        if request.method == 'POST':
            form = taskForm(request.POST, instance=get_task)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                completed = form.cleaned_data.get('completed')
                print(title, completed)
                form.save()
                return redirect("/")
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
        return redirect("/")
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
        return redirect("/")
    context = {
        'task':task_list, 'form':form
    }
    return render(request, 'events/home.html',  context = context)


def reminder(title):
    pass

now = timezone.now()
task_re = task.objects.filter(remind_at__isnull = False)
mail_times = []
for time in task_re:
    mail_times.append(time.remind_at)
    if time.remind_at == now:
        reminder(time.title)
print(mail_times)