from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('todo-list/', views.todoList, name="todo-list"),
    path('todo-detail/<int:id>/', views.todoDetail, name="todo-Detail"),
    path('todo-create/', views.todoCreate, name="todo-Create"),
    path('todo-update/<int:id>/', views.todoUpdate, name="todo-update"),
    path('todo-delete/<int:id>/', views.todoDelete, name="todo-delete"),
]
