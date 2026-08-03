""" Veritabanı tabloları """
from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField("Departman Adı", max_length=100)
    manager = models.ForeignKey(User, verbose_name="Departman Yöneticisi", on_delete=models.SET_NULL, null=True, blank=True, related_name="managed_departments")

    class Meta:
        verbose_name = "Departman"
        verbose_name_plural = "Departmanlar"

    def __str__(self):
        return self.name


class Period(models.Model):
    name = models.CharField("Dönem Adı", max_length=100)
    start_date = models.DateField("Başlangıç Tarihi")
    end_date = models.DateField("Bitiş Tarihi")
    is_locked = models.BooleanField("Kilitli mi", default=False)

    class Meta:
        verbose_name = "Dönem"
        verbose_name_plural = "Dönemler"

    def __str__(self):
        return self.name


class Category(models.Model):
    BUDGET_TYPE_CHOICES = [
        ("uretim", "Üretim Bütçesi"),
        ("satis", "Satış Bütçesi"),
        ("maliyet", "Maliyet Bütçesi"),
        ("nakit", "Nakit Akışı Bütçesi"),
        ("personel", "Personel / İK Bütçesi"),
        ("yatirim", "Yatırım (CAPEX) Bütçesi"),
        ("pazarlama", "Pazarlama Bütçesi"),
        ("genel_yonetim", "Genel Yönetim Gideri Bütçesi"),
        ("arge", "Ar-Ge Bütçesi"),
        ("bakim_onarim", "Bakım-Onarım Bütçesi"),
    ]
    name = models.CharField("Kategori Adı", max_length=100)
    budget_type = models.CharField("Bütçe Türü", max_length=20, choices=BUDGET_TYPE_CHOICES)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name


class BudgetHeader(models.Model):
    STATUS_CHOICES = [
        ("taslak", "Taslak"),
        ("dept_onay", "Departman Onayında"),
        ("finans_onay", "Finans İncelemesinde"),
        ("ust_onay", "Üst Yönetim Onayında"),
        ("onaylandi", "Onaylandı"),
        ("reddedildi", "Reddedildi"),
    ]
    department = models.ForeignKey(Department, verbose_name="Departman", on_delete=models.CASCADE)
    period = models.ForeignKey(Period, verbose_name="Dönem", on_delete=models.CASCADE)
    budget_type = models.CharField("Bütçe Türü", max_length=20, choices=Category.BUDGET_TYPE_CHOICES)
    status = models.CharField("Durum", max_length=20, choices=STATUS_CHOICES, default="taslak")
    version_number = models.PositiveIntegerField("Versiyon No", default=1)
    created_by = models.ForeignKey(User, verbose_name="Oluşturan", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField("Oluşturulma Tarihi", auto_now_add=True)

    class Meta:
        verbose_name = "Bütçe"
        verbose_name_plural = "Bütçeler"

    def __str__(self):
        return f"{self.department} - {self.period} - {self.get_budget_type_display()}"


class BudgetLine(models.Model):
    budget_header = models.ForeignKey(BudgetHeader, verbose_name="Bütçe", on_delete=models.CASCADE, related_name="lines")
    category = models.ForeignKey(Category, verbose_name="Kategori", on_delete=models.PROTECT)
    planned_amount = models.DecimalField("Planlanan Tutar", max_digits=12, decimal_places=2)
    month = models.PositiveSmallIntegerField("Ay", null=True, blank=True)
    notes = models.TextField("Açıklama", blank=True)

    class Meta:
        verbose_name = "Bütçe Kalemi"
        verbose_name_plural = "Bütçe Kalemleri"

    def __str__(self):
        return f"{self.category} - {self.planned_amount}"


class ApprovalStep(models.Model):
    ACTION_CHOICES = [
        ("bekliyor", "Bekliyor"),
        ("onaylandi", "Onaylandı"),
        ("reddedildi", "Reddedildi"),
        ("revizyon", "Revizyon İstendi"),
    ]
    budget_header = models.ForeignKey(BudgetHeader, verbose_name="Bütçe", on_delete=models.CASCADE, related_name="approval_steps")
    step_order = models.PositiveSmallIntegerField("Sıra")
    approver = models.ForeignKey(User, verbose_name="Onaylayacak Kişi", on_delete=models.SET_NULL, null=True)
    status = models.CharField("Durum", max_length=20, choices=ACTION_CHOICES, default="bekliyor")
    comment = models.TextField("Yorum", blank=True)
    acted_at = models.DateTimeField("İşlem Tarihi", null=True, blank=True)

    class Meta:
        verbose_name = "Onay Adımı"
        verbose_name_plural = "Onay Adımları"

    def __str__(self):
        return f"{self.budget_header} - Adım {self.step_order}"


class ActualData(models.Model):
    department = models.ForeignKey(Department, verbose_name="Departman", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="Kategori", on_delete=models.CASCADE)
    period = models.ForeignKey(Period, verbose_name="Dönem", on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField("Ay")
    actual_amount = models.DecimalField("Gerçekleşen Tutar", max_digits=12, decimal_places=2)
    imported_at = models.DateTimeField("İçe Aktarım Tarihi", auto_now_add=True)

    class Meta:
        verbose_name = "Gerçekleşen Veri"
        verbose_name_plural = "Gerçekleşen Veriler"

    def __str__(self):
        return f"{self.department} - {self.category} - Ay {self.month}"