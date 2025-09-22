from django.shortcuts import render, get_object_or_404, redirect
import requests
from django.views.decorators.csrf import csrf_exempt
from .forms import BugForm
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login
# from .models import Bug
# from .forms import BugForm, UserRegistrationForm

API_BASE = "http://127.0.0.1:8001/api/bugs/"

def index(request):
    return render(request,'index.html')

def bug_list(request):
    response = requests.get(API_BASE)
    bugs = response.json()
    return render(request, 'bug_list.html',{'bugs':bugs})

def bug_create(request):
    if request.method == "POST":
        form = BugForm(request.POST, request.FILES)
        if form.is_valid():
            data = {
                "title": form.cleaned_data["title"],
                "description": form.cleaned_data["description"],
                "status": form.cleaned_data["status"],
                "priority": form.cleaned_data["priority"],
            }
            files = {"screenshot": request.FILES.get("screenshot")} if request.FILES else None
            response = requests.post(API_BASE, data=data, files=files)
            if response.status_code == 201:
                return redirect("bug_list")
    else:
        form = BugForm()

    return render(request, "bug_form.html", {"form": form})

def bug_edit(request, bug_id):
    url = f"{API_BASE}{bug_id}/"
    if request.method == "POST":
        form = BugForm(request.POST, request.FILES)
        if form.is_valid():
            data = {
                "title": form.cleaned_data["title"],
                "description": form.cleaned_data["description"],
                "status": form.cleaned_data["status"],
                "priority": form.cleaned_data["priority"],
            }
            files = {"screenshot": request.FILES.get("screenshot")} if request.FILES else None
            response = requests.put(url, data=data, files=files)
            if response.status_code in [200, 204]:
                return redirect("bug_list")
            else:
                error = response.text
        else:
            error = "Form validation failed"
    else:
        response = requests.get(url)
        if response.status_code == 200:
            bug_data = response.json()
            form = BugForm(initial={
                "title": bug_data.get("title", ""),
                "description": bug_data.get("description", ""),
                "status": bug_data.get("status", "OPEN"),
                "priority": bug_data.get("priority", "MEDIUM"),
            })
            error = None
        else:
            form = BugForm()
            error = "Could not fetch bug"

    return render(request, "bug_form.html", {"form": form, "error": error})

def bug_delete(request, bug_id):
    url = f"{API_BASE}{bug_id}/"

    if request.method == "POST":
        response = requests.delete(url)
        # redirect if deleted successfully
        if response.status_code in [200, 204]:
            return redirect("bug_list")
        else:
            error = response.text
            return render(request, "bug_confirm_delete.html", {"error": error})

    # GET request → just show confirmation page
    return render(request, "bug_confirm_delete.html")



# def register(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             reported_by = form.save(commit=False)
#             reported_by.set_password(form.cleaned_data['password1'])
#             reported_by.save()
#             login(request,reported_by)
#             return redirect('bug_list')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'registration/register.html',{'form':form})