from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelform
from tasks.models import Employee,Task
# Create your views here.
 # home function return kore ( work with database,transform data, data pass, http response / json response)

def manager_dashboard(request):
   return render(request,"dashboard/manager_dashboard.html")
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

def task_form(request):
   #emp = Employee.objects.all()
   #form = TaskForm(employees = emp) # for GET
   form = TaskModelform() # for GET
   if request.method == "POST":
      form = TaskModelform(request.POST)
      if form.is_valid():
         ''' for Model Form data'''
         form.save()
         
         return render(request,'task_form.html',{"form":form,"message":"task added successfully"})
         
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
   context = {"form":form}
   return render(request,"task_form.html",context)


def view_task(request):
   # retrive all data from tasks
   tasks = Task.objects.all()
   
   #retrieve specific task
   task_3 = Task.objects.get(pk=3)
   return render(request,"show_task.html",{"tasks":tasks,"task3":task_3})
   