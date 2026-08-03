from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("budgets/", views.budget_list, name="budget_list"),
    path("budgets/yeni/", views.budget_create, name="budget_create"),
    path("budgets/<int:pk>/", views.budget_detail, name="budget_detail"),
    path("budgets/<int:pk>/gonder/", views.submit_for_approval, name="submit_for_approval"),
    path("budgets/<int:pk>/onayla/", views.approve_budget, name="approve_budget"),
    path("budgets/<int:pk>/reddet/", views.reject_budget, name="reject_budget"),
    path("rapor/sapma/", views.variance_report, name="variance_report"),
]