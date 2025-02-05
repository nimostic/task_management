from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelform,TaskDetailForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Count,Min,Max,Avg
from django.contrib import messages
# Create your views here.
 # home function return kore ( work with database,transform data, data pass, http response / json response)

def manager_dashboard(request):
   
   #getting task count 
   # total_task = tasks.count()
   # completed_task = Task.objects.filter(status = "COMPLETED").count()
   # in_progress = Task.objects.filter(status = "IN_PROGRESS").count()
   # pending_task = Task.objects.filter(status = "PENDING").count()
   
   type = request.GET.get('type','all')
   
   counts = Task.objects.aggregate(
      total = Count('id'),
      completed = Count('id',filter=Q(status='COMPLETED')),
      in_progress = Count('id',filter=Q(status='IN_PROGRESS')),
      pending = Count('id',filter=Q(status='PENDING')),
   )
   
   base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
   
   if type == 'completed':
      tasks = base_query.filter(status = 'COMPLETED')
   elif type == 'in-progress':
      tasks = base_query.filter(status = 'IN_PROGRESS')
   elif type == 'pending':
      tasks = base_query.filter(status = 'PENDING')
   elif type == 'all':
      tasks = base_query.all()
   
   
   context = {
      "tasks" : tasks,
      "counts": counts
   }
   return render(request,"dashboard/manager_dashboard.html",context)
def user_dashboard(request):
   return render(request,"dashboard/user_dashboard.html")

def test(request):
   names = ["Riyad","Rahim","Karim"]
   count = 0
   for name in names:
      count +=1
   context = {
      "names" : names,
      "age" :23,
      "count": count
   }
   return render(request,"test.html",context)

def create_task(request):
   #emp = Employee.objects.all()
   #form = TaskForm(employees = emp) # for GET
   task_form = TaskModelform() # for GET
   task_detail_form = TaskDetailForm()
   if request.method == "POST":
      task_form = TaskModelform(request.POST)
      task_detail_form = TaskDetailForm(request.POST)
      
      if task_form.is_valid() and task_detail_form.is_valid():
         ''' for Model Form data'''
         
         task = task_form.save()
         task_detail = task_detail_form.save(commit=False)
         task_detail.task = task
         task_detail.save()
         
         messages.success(request,"Task Created successfully")
         return redirect('create-task')
         
         '''for Django form data'''
         # data = form.cleaned_data
         # title = data.get('title')
         # description = data.get('description')
         # due_date = data.get('due_date')
         # assigned_to = data.get('assigned_to')  # list [1,3]
         
         # task = Task.objects.create(title = title,description= description,due_date = due_date)
         # # assign employee to tasks
         
         # for emp_id in assigned_to :
         #    employee = Employee.objects.get(id = emp_id)
         #    task.assigned_to.add(employee)
         
         # return HttpResponse("task added successfully")
   context = {"task_form":task_form,"task_detail_form":task_detail_form}
   return render(request,"task_form.html",context)

def update_task(request,id):
   task = Task.objects.get(id=id)
   task_form = TaskModelform(instance=task)
   
   if task.details:
      task_detail_form = TaskDetailForm(instance = task.details)
   
   if request.method == "POST":
      task_form = TaskModelform(request.POST,instance = task)
      task_detail_form = TaskDetailForm(request.POST,instance = task.details)
      
      if task_form.is_valid() and task_detail_form.is_valid():
         ''' for Model Form data'''
         
         task = task_form.save()
         task_detail = task_detail_form.save(commit=False)
         task_detail.task = task
         task_detail.save()
         
         messages.success(request,"Task Updated successfully")
         return redirect('update-task',id)
      
   context = {"task_form":task_form,"task_detail_form":task_detail_form}
   return render(request,"task_form.html",context)


def delete_task(request,id):
   if request.method == 'POST':
      task = Task.objects.get(id= id)
      task.delete()
      messages.success(request,'Task deleted successfully')
      return redirect('manager-dashboard')
   else:
      messages.error(request,'Something went wrong')
      return redirect('manager-dashboard')


def view_task(request):
   '''retrive all data from tasks'''
   # tasks = Task.objects.all()
   
   '''retrieve specific task'''
   # task_3 = Task.objects.get(pk=3)
   
   '''show the tasks that are completed'''
   # tasks = Task.objects.filter(status = "COMPLETED")
   
   '''show task whose priority is low'''
   # tasks = TaskDetail.objects.filter(priority = "L")
   
   '''show task whose due date is today'''
   #tasks = Task.objects.filter(due_date = date.today())
   
   '''show task whose priority isn't high'''
   #tasks = TaskDetail.objects.exclude(priority = "H")
   
   '''show the task that contain word 'paper' and status 'pending '''
   # tasks = Task.objects.filter(title__icontains = "paper",status = "PENDING")
   
   '''show the task which status are  in-progress or 'pending '''
   # tasks = Task.objects.filter(Q(status = "IN_PROGRESS") | Q(status = "PENDING"))
   
   # filter data na thakle error return dey na ejnno exists() use korte hoy
   
   #tasks = Task.objects.filter(status = "DJSFHJDS").exists()
   tasks = TaskDetail.objects.exclude(priority="L")
   return render(request,"show_task.html",{"tasks":tasks})
   