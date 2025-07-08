# todo/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm # type: ignore # We'll create this form later for Bonus features

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optional: Log the user in immediately after registration
            # from django.contrib.auth import login
            # login(request, user)
            return redirect('login') # Redirect to login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        # Admin view: Show all users and all tasks
        all_users = User.objects.all().order_by('username')
        all_tasks = Task.objects.all().order_by('user__username', 'completed', 'created_at')
        context = {
            'all_users': all_users,
            'all_tasks': all_tasks,
            'is_admin': True,
        }
    else:
        # Normal user view: Show only their tasks
        user_tasks = Task.objects.filter(user=request.user).order_by('completed', 'created_at')
        context = {
            'user_tasks': user_tasks,
            'is_admin': False,
        }
    return render(request, 'todo/home.html', context)
# todo/views.py (add these to your existing views)

from django.http import HttpResponseRedirect # Add this import

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form, 'title': 'Create Task'})

@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user) # Ensure user owns the task
    
    # Handle GET request for marking complete/incomplete
    action = request.GET.get('action')
    if action == 'complete':
        task.completed = True
        task.save()
        return redirect('dashboard')
    elif action == 'incomplete':
        task.completed = False
        task.save()
        return redirect('dashboard')

    # Handle POST request for general updates (if you decide to have an edit form)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form, 'title': 'Update Task'})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user) # Ensure user owns the task
    if request.method == 'POST': # Using POST for deletion is safer
        task.delete()
        return redirect('dashboard')
    # For simplicity, we'll just delete on GET request from the dashboard link for this activity
    # In a real app, you'd likely use a confirmation page/modal with POST.
    task.delete()
    return redirect('dashboard')