from django.shortcuts import render, get_object_or_404, redirect
import requests
from django.views.decorators.csrf import csrf_exempt
from .forms import BugForm
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login
# from .models import Bug
# from .forms import BugForm, UserRegistrationForm

API_TOKEN_URL = "http://127.0.0.1:8001/api/token/"
API_REGISTER_URL = "http://127.0.0.1:8001/api/register/"
API_BASE = "http://127.0.0.1:8001/api/bugs/"
API_USERS = "http://127.0.0.1:8001/api/users/"

def index(request):
    return render(request,'index.html')

def bug_list(request):
    headers = {"Authorization": f"Bearer {request.session.get('access_token')}"}
    response = requests.get(API_BASE)
    bugs = response.json()
    return render(request, 'bug_list.html',{'bugs':bugs,"username": request.session.get("username")})

def bug_create(request):
    access_token = request.session.get("access_token")
    if not access_token:
        return redirect("login")
    
    response = requests.get(API_USERS)
    users = response.json() if response.status_code == 200 else []
    user_choices = [(u['id'], u['username']) for u in users]

    if request.method == "POST":
        form = BugForm(request.POST, request.FILES)
        form.fields['assigned_to'].choices = user_choices

        if form.is_valid():
            data = {
                "title": form.cleaned_data["title"],
                "description": form.cleaned_data["description"],
                "status": form.cleaned_data["status"],
                "priority": form.cleaned_data["priority"],
                "assigned_to": form.cleaned_data["assigned_to"] or None,
            }
            files = {"screenshot": request.FILES.get("screenshot")} if request.FILES else None
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(API_BASE, data=data, files=files, headers=headers)
            if response.status_code == 201:
                return redirect("bug_list")
    else:
        form = BugForm()
        form.fields['assigned_to'].choices = user_choices

    return render(request, "bug_form.html", {"form": form,"username": request.session.get("username")})

def bug_edit(request, bug_id):
    access_token = request.session.get("access_token")
    if not access_token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{API_BASE}{bug_id}/"

    response = requests.get(API_USERS)
    users = response.json() if response.status_code == 200 else []
    user_choices = [(u['id'], u['username']) for u in users]

    if request.method == "POST":
        form = BugForm(request.POST, request.FILES)
        form.fields['assigned_to'].choices = user_choices
        if form.is_valid():
            data = {
                "title": form.cleaned_data["title"],
                "description": form.cleaned_data["description"],
                "status": form.cleaned_data["status"],
                "priority": form.cleaned_data["priority"],
                "assigned_to": form.cleaned_data["assigned_to"],
            }
            files = {"screenshot": request.FILES.get("screenshot")} if request.FILES else None
            response = requests.put(url, data=data, files=files, headers=headers)
            if response.status_code in [200, 204]:
                return redirect("bug_list")
            else:
                error = response.text
        else:
            error = "Form validation failed"
    else:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            bug_data = response.json()
            form = BugForm(initial={
                "title": bug_data.get("title", ""),
                "description": bug_data.get("description", ""),
                "status": bug_data.get("status", "OPEN"),
                "priority": bug_data.get("priority", "MEDIUM"),
                "assigned_to": bug_data.get("assigned_to"),
            })
            form.fields['assigned_to'].choices = user_choices
            error = None
        else:
            form = BugForm()
            form.fields['assigned_to'].choices = user_choices
            error = "Could not fetch bug"

    return render(request, "bug_form.html", {"form": form, "error": error,"username": request.session.get("username")})

def bug_delete(request, bug_id):
    access_token = request.session.get("access_token")
    if not access_token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{API_BASE}{bug_id}/"

    if request.method == "POST":
        response = requests.delete(url, headers=headers)
        if response.status_code in [200, 204]:
            return redirect("bug_list")
        else:
            error = response.text
            return render(request, "bug_confirm_delete.html", {"error": error})

    return render(request, "bug_confirm_delete.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        response = requests.post(API_TOKEN_URL, data={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            tokens = response.json()
            request.session['access_token'] = tokens['access']
            request.session['refresh_token'] = tokens['refresh']
            request.session['username'] = username
            return redirect("bug_list")
        else:
            error = "Invalid username or password"

        return render(request, "registration/login.html", {"error": error})

    return render(request, "registration/login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        response = requests.post(API_REGISTER_URL, data={
            "username": username,
            "password": password,
            "email": email
        })

        if response.status_code == 201:
            # Registration successful → redirect to login
            return redirect("login")
        else:
            error = response.json().get("error", "Registration failed")
            return render(request, "registration/register.html", {"error": error})

    return render(request, "registration/register.html")

def logout_view(request):
    request.session.flush()  
    return redirect("bug_list") 