from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save,m2m_changed,post_delete
from django.core.mail import send_mail
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    description = models.TextField(default="Default description")
    


class Task(models.Model):
    
    STATUS_CHOICES = [
        ('PENDING','Pending'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Completed')
    ]
    
    #many to one connection
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        default=1, #parent er obj create kore first() call id paiya ekhane bosate hobe
        related_name='task_p'
        )
    
    #many to many connection
    
    assigned_to = models.ManyToManyField("Employee",related_name='tasks') #tasks er maddome reverse query , employee er maddome tasks access korbo
    
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,default="PENDING"
    )
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) #jokhon create kore oi time e niye ney ar change hoy na
    updated_at = models.DateTimeField(auto_now=True) #change hote pare
    
    def __str__(self):
        return self.title
    
# one to one connection

class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS=(
        (HIGH,'High'),
        (MEDIUM,'Medium'),
        (LOW,'Low')
    ) 
    task = models.OneToOneField(
        Task,
        on_delete=models.DO_NOTHING,
        related_name='details',
    )
    #assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1,choices=PRIORITY_OPTIONS,default=LOW)
    notes = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Details from Task {self.task.title}"
    
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    description = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.name
    

@receiver(m2m_changed,sender = Task.assigned_to.through)
def notify_employees_on_task_creation(sender,instance,action, **kargs):
    if action == 'post_add':
        print(instance,instance.assigned_to.all())
        
        assigned_emails = [emp.email for emp in  instance.assigned_to.all()]
        print("checking.....",assigned_emails)
        send_mail(
        "New Task Created",
        f"You have been assigned to the task : {instance.title}",
        "lunasender143@gmail.com",
        assigned_emails,
        fail_silently=False,
)
        
@receiver(post_delete,sender = Task)
def delete_associate_details(sender,instance,**kargs):
    if instance.details:
        print(isinstance)
        instance.details.delete()
        
        print("deleted successfully")