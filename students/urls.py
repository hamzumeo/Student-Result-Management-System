from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='student_add'),
    path('students/edit/<int:pk>/', views.student_edit, name='student_edit'),
    path('students/delete/<int:pk>/', views.student_delete, name='student_delete'),

    # Results
    path('results/', views.result_list, name='result_list'),
    path('results/add/', views.add_result, name='result_add'),
    path('results/edit/<int:pk>/', views.edit_result, name='result_edit'),
    path('results/delete/<int:pk>/', views.delete_result, name='result_delete'),
]
