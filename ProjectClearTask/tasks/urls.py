from django.urls import path
from .views import (
    TaskListView, TaskCreateView, TaskUpdateView, HomeView,
    TaskDeleteView, TaskDetailView, AddCommentView,DeleteCommentView,
    MyTaskListView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('task/new/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task-edit'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task/<int:pk>/comment/', AddCommentView.as_view(), name='add-comment'),
    path('comment/<int:pk>/delete/', DeleteCommentView.as_view(), name='delete-comment'),
    path('my-tasks/', MyTaskListView.as_view(), name='my-tasks'),

]

