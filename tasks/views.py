from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
 # home function return kore ( work with database,transform data, data pass, http response / json response)
def home(request):
   return HttpResponse("welcome to the task management system")
def contact(request):
    return HttpResponse("<h1 style = 'color:red' >this is contact page</h1>")
 

def show_task(request):
   return HttpResponse("this is a task page") 