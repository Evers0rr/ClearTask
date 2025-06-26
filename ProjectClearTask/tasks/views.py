from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, View, TemplateView
)
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Task, Comments
from .forms import TaskForm,CommentForm
from django.urls import reverse_lazy

# Create your views here. OKAK 

class HomeView(TemplateView):
    template_name = 'based/home.html'

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)
    
class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    authentication_form = AuthenticationForm

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Task.objects.all()

        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')

        if status and status != 'all':
            queryset = queryset.filter(status=status)
        if priority and priority != 'all':
            queryset = queryset.filter(priority=priority)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', 'all')
        context['selected_priority'] = self.request.GET.get('priority', 'all')
        return context
    
class MyTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/my_task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.filter(author=self.request.user)

        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')

        if status and status != 'all':
            queryset = queryset.filter(status=status)
        if priority and priority != 'all':
            queryset = queryset.filter(priority=priority)

        return queryset.order_by('due_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', 'all')
        context['selected_priority'] = self.request.GET.get('priority', 'all')
        return context

      
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author or self.request.user.is_staff


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author or self.request.user.is_staff

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.order_by('-created_at')
        return context
    
class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
        return redirect('task-detail', pk=task.pk)
    
class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comments
    template_name = 'tasks/comment_confirm_delete.html'
    success_url = reverse_lazy('task-list')  

    def get_success_url(self):
        return self.object.task.get_absolute_url()  

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_staff
