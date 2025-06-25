from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Task(models.Model):
    STATUS_CHOICES = [('todo','To do'),('in_progress','In Progress'),('done','Done')]
    PRIORITY_CHOICES = [('L','Low'),('M','Medium'),('H','High')]

    title = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='todo')
    priority = models.CharField(max_length=1,choices=PRIORITY_CHOICES,default='M')
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Завдання"
        verbose_name_plural = "Завдання"

    def __str__(self):
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.pk)])
    

class Comments(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"

    def __str__(self):
        return f'Юзер під нікнеймом:{self.author.username} написав коментар під завданням - {self.task.title}'
    


    



