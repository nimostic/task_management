from django.urls import path
from tasks.views import manager_dashboard,employee_dashboard,view_task,create_task,update_task,delete_task

urlpatterns = [
    path("manager-dashboard/",manager_dashboard,name="manager-dashboard"),
    path("user-dashboard/",employee_dashboard),
    path("create-task/",create_task,name='create-task'),
    path("show_task/",view_task),
    path("update-task/<int:id>/",update_task,name="update-task"),
    path("delete-task/<int:id>/",delete_task,name="delete-task")
]