""" Yönetim paneli """
from django.contrib import admin
from .models import Department, Period, Category, BudgetHeader, BudgetLine, ApprovalStep, ActualData, Notification, AuditLog


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "manager")


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "is_locked")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "budget_type")
    list_filter = ("budget_type",)


class BudgetLineInline(admin.TabularInline):
    model = BudgetLine
    extra = 1


@admin.register(BudgetHeader)
class BudgetHeaderAdmin(admin.ModelAdmin):
    list_display = ("department", "period", "budget_type", "status", "version_number", "created_by", "created_at")
    list_filter = ("status", "budget_type", "period")
    inlines = [BudgetLineInline]


@admin.register(ApprovalStep)
class ApprovalStepAdmin(admin.ModelAdmin):
    list_display = ("budget_header", "step_order", "approver", "status", "acted_at")
    list_filter = ("status",)


@admin.register(ActualData)
class ActualDataAdmin(admin.ModelAdmin):
    list_display = ("department", "category", "period", "month", "actual_amount")
    list_filter = ("period", "department")
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "description", "timestamp")
    list_filter = ("action",)
    readonly_fields = ("user", "action", "description", "timestamp")