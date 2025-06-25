from django.contrib import admin
from .models import Task, Comments

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'due_date', 'created_at', 'author')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at')
    search_fields = ('text',)
    ordering = ('-created_at',)