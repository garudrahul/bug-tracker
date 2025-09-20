from django.shortcuts import render, get_object_or_404, redirect
import requests
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login
# from .models import Bug
# from .forms import BugForm, UserRegistrationForm

def index(request):
    return render(request,'index.html')

def bug_list(request):
    response = requests.get("http://127.0.0.1:8001/api/bugs/")
    bugs = response.json()
    return render(request, 'bug_list.html',{'bugs':bugs})

# @login_required
# def bug_create(request):
#     if request.method == "POST":
#         form = BugForm(request.POST , request.FILES)
#         if form.is_valid():
#             bug = form.save(commit=False)
#             bug.reported_by = request.user
#             bug.save()
#             return redirect('bug_list')
#     else:
#         form = BugForm()
#     return render(request, 'bug_form.html',{'form':form})

# @login_required
# def bug_edit(request, bug_id):
#     bug = get_object_or_404(Bug, pk=bug_id, reported_by=request.user)
#     if request.method == "POST":
#         form = BugForm(request.POST , request.FILES, instance=bug)
#         if form.is_valid():
#             bug = form.save(commit=False)
#             bug.reported_by = request.user
#             bug.save()
#             return redirect('bug_list')
#     else:
#         form = BugForm(instance=bug)
#     return render(request, 'bug_form.html',{'form':form})
    
# @login_required
# def bug_delete(request, bug_id):
#     bug = get_object_or_404(Bug, pk=bug_id, reported_by=request.user)
#     if request.method == "POST":
#         bug.delete()
#         return redirect('bug_list')
#     return render(request, 'bug_confirm_delete.html',{'bug':bug})

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