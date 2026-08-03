from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django.utils import timezone
from .models import BudgetHeader, Department, ApprovalStep, ActualData
from .forms import BudgetHeaderForm, BudgetLineForm


@login_required
def dashboard(request):
    total_budgets = BudgetHeader.objects.count()
    departments = Department.objects.count()
    pending_approval = BudgetHeader.objects.filter(
        status__in=["dept_onay", "finans_onay", "ust_onay"]
    ).count()
    approved = BudgetHeader.objects.filter(status="onaylandi").count()

    dept_data = (
        BudgetHeader.objects.values("department__name")
        .annotate(total=Sum("lines__planned_amount"))
        .order_by("-total")
    )
    dept_labels = [d["department__name"] for d in dept_data]
    dept_values = [float(d["total"] or 0) for d in dept_data]

    context = {
        "total_budgets": total_budgets,
        "departments": departments,
        "pending_approval": pending_approval,
        "approved": approved,
        "dept_labels": dept_labels,
        "dept_values": dept_values,
    }
    return render(request, "budgets/dashboard.html", context)

@login_required
def budget_list(request):
    budgets = BudgetHeader.objects.select_related("department", "period").annotate(
        total_amount=Sum("lines__planned_amount")
    )
    if not request.user.is_superuser:
        budgets = budgets.filter(department__manager=request.user)
    return render(request, "budgets/budget_list.html", {"budgets": budgets})


@login_required
def budget_create(request):
    if request.method == "POST":
        form = BudgetHeaderForm(request.POST, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.created_by = request.user if request.user.is_authenticated else None
            budget.save()
            return redirect("budget_list")
    else:
        form = BudgetHeaderForm(user=request.user)
    return render(request, "budgets/budget_form.html", {"form": form})


@login_required
def budget_detail(request, pk):
    budget = get_object_or_404(BudgetHeader, pk=pk)
    if not request.user.is_superuser and budget.department.manager != request.user:
        messages.error(request, "Bu bütçeyi görüntüleme yetkiniz yok.")
        return redirect("budget_list")
    lines = budget.lines.all()
    if request.method == "POST":
        form = BudgetLineForm(request.POST)
        if form.is_valid():
            line = form.save(commit=False)
            line.budget_header = budget
            line.save()
            return redirect("budget_detail", pk=budget.pk)
    else:
        form = BudgetLineForm()
    total = sum(x.planned_amount for x in lines)
    return render(request, "budgets/budget_detail.html", {
        "budget": budget,
        "lines": lines,
        "form": form,
        "total": total,
    })


@login_required
def submit_for_approval(request, pk):
    budget = get_object_or_404(BudgetHeader, pk=pk)
    budget.status = "dept_onay"
    budget.save()
    ApprovalStep.objects.create(
        budget_header=budget,
        step_order=1,
        approver=None,
        status="bekliyor",
    )
    messages.success(request, "Bütçe onaya gönderildi.")
    return redirect("budget_detail", pk=budget.pk)



@login_required
def approve_budget(request, pk):
    budget = get_object_or_404(BudgetHeader, pk=pk)
if not request.user.is_superuser:
        messages.error(request, "Bu işlemi yapma yetkiniz yok.")
        return redirect("budget_detail", pk=budget.pk)
    budget.status = "onaylandi"
    budget.save()
    step = budget.approval_steps.filter(status="bekliyor").first()
    if step:
        step.status = "onaylandi"
        step.approver = request.user
        step.acted_at = timezone.now()
        step.save()
    messages.success(request, "Bütçe onaylandı.")
    return redirect("budget_detail", pk=budget.pk)


@login_required
def reject_budget(request, pk):
    budget = get_object_or_404(BudgetHeader, pk=pk)
    budget.status = "reddedildi"
    budget.save()
    step = budget.approval_steps.filter(status="bekliyor").first()
    if step:
        step.status = "reddedildi"
        step.approver = request.user
        step.acted_at = timezone.now()
        step.save()
    messages.warning(request, "Bütçe reddedildi.")
    return redirect("budget_detail", pk=budget.pk)

from .models import ActualData


@login_required
def variance_report(request):
    departments = Department.objects.all()
    if not request.user.is_superuser:
        departments = departments.filter(manager=request.user)

    report = []
    for dept in departments:
        planned = BudgetHeader.objects.filter(department=dept).aggregate(
            total=Sum("lines__planned_amount")
        )["total"] or 0
        actual = ActualData.objects.filter(department=dept).aggregate(
            total=Sum("actual_amount")
        )["total"] or 0
        if planned > 0:
            usage_percent = round((actual / planned) * 100, 1)
        else:
            usage_percent = 0
        variance = planned - actual
        report.append({
            "department": dept.name,
            "planned": planned,
            "actual": actual,
            "variance": variance,
            "usage_percent": usage_percent,
        })

    return render(request, "budgets/variance_report.html", {"report": report})