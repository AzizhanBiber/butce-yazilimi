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
    path("bildirimler/", views.notifications, name="notifications"),
    path("bildirimler/<int:pk>/sil/", views.delete_notification, name="delete_notification"),
    path("bildirimler/<int:pk>/ac/" , views.open_notification, name="open_notification"),
    path("budgets/<int:pk>/yeni-versiyon/", views.create_new_version, name="create_new_version"),
    path("kaelm/<int:pk>/duzenle/", views.edit_budget_line, name="edit_budget_line"),
    path("kalem/<int:pk>/sil/", views.delete_budget_line, name="delete_budget_line"),
    path("budgets/<int:pk>/excel-disa-aktar/", views.export_budget_excel, name="export_budget_excel"),
    path("budgets/<int:pk>/excel-ice-aktar/", views.import_budget_excel, name="import_budget_excel"),
    path("rapor/ozet/", views.summary_report, name="summary_report"),
    path("rapor/trend/", views.trend_report, name="trend_report"),
    path("budgets/<int:pk>/pdf-indir/", views.export_budget_pdf, name="export_budget_pdf"),
    path("budgets/<int:pk>/sap-senkron/", views.sync_from_sap, name="sync_from_sap"),
]