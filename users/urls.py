from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
    # Departments endpoints
    path('departments/', views.DepartmentList.as_view(), name='department-list'),
    path('department/<int:pk>/', views.DepartmentDetail.as_view(), name='department-detail'),

    # Designations endpoints
    path('designations/', views.DesignationListView.as_view(), name='designation-list'),
    path('create-designation/', views.DesignationCreateView.as_view(), name='designation-create'),
    path('designation/<int:pk>/', views.DesignationDetail.as_view(), name='designation-detail'),

    # Employees endpoints
    path('profile/', views.EmpListView.as_view(), name='single-employee-data'),
    path('employees/', views.EmployeeListView.as_view(), name='employees-list'),
    path('employee-registration/', views.EmployeeCreate.as_view(), name='employees-create'),
    path('employee/<int:pk>/', views.EmployeeDetail.as_view(), name='employee-detail')
]



















