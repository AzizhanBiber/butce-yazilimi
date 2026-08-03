from django import forms
from .models import BudgetHeader, BudgetLine, Department


class BudgetHeaderForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and not user.is_superuser:
            self.fields["department"].queryset = Department.objects.filter(manager=user)

    class Meta:
        model = BudgetHeader
        fields = ["department", "period", "budget_type"]
        labels = {
            "department": "Departman",
            "period": "Dönem",
            "budget_type": "Bütçe Türü",
        }
        widgets = {
            "department": forms.Select(attrs={"class": "form-select"}),
            "period": forms.Select(attrs={"class": "form-select"}),
            "budget_type": forms.Select(attrs={"class": "form-select"}),
        }


class BudgetLineForm(forms.ModelForm):
    class Meta:
        model = BudgetLine
        fields = ["category", "planned_amount", "month", "notes"]
        labels = {
            "category": "Kategori",
            "planned_amount": "Planlanan Tutar (TL)",
            "month": "Ay (1-12)",
            "notes": "Açıklama",
        }
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "planned_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "month": forms.NumberInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }