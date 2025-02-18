from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save,m2m_changed,post_delete
from django.core.mail import send_mail
from tasks.models import Task

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