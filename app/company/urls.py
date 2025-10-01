from django.urls import path
from .views import CompanyViewSet, MyCompanyView

company_detail = CompanyViewSet.as_view({'get': 'retrieve'})
company_create = CompanyViewSet.as_view({'post': 'create'})
company_update = MyCompanyView.as_view({'put': 'update'})
company_delete = MyCompanyView.as_view({'delete': 'destroy'})

company_employees = MyCompanyView.as_view({'get': 'employees', 'post': 'add_employee'})
company_employee_delete = MyCompanyView.as_view({'delete': 'employees_remove'})

urlpatterns = [
    path('companies/create/', company_create, name='company-create'),
    path('companies/<int:pk>/', company_detail, name='company-detail'),
    path('companies/update/', company_update, name='company-update'),
    path('companies/delete/', company_delete, name='company-delete'),

    path('companies/employees/', company_employees, name='company-employees'),
    path('companies/employees/<int:user_id>/', company_employee_delete, name='company-employee-remove'),
]
