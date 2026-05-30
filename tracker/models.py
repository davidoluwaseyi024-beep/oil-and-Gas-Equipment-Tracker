from django.db import models
from django.utils import timezone


class Equipment(models.Model):

    class Condition(models.TextChoices):
        GOOD = "good", "Good"
        FAIR = "fair", "Fair"
        POOR = "poor", "Poor"

    class Status(models.TextChoices):
        IN_SERVICE        = "in_service",        "In Service"
        UNDER_MAINTENANCE = "under_maintenance",  "Under Maintenance"
        OUT_OF_SERVICE    = "out_of_service",     "Out of Service"

    name              = models.CharField(max_length=200)
    serial_number     = models.CharField(max_length=100, unique=True)
    location          = models.CharField(max_length=200)
    condition         = models.CharField(max_length=10, choices=Condition.choices, default=Condition.GOOD)
    status            = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_SERVICE, db_index=True)
    critical          = models.BooleanField(default=False, db_index=True)
    last_service_date = models.DateField(null=True, blank=True)
    next_due_date     = models.DateField(null=True, blank=True, db_index=True)
    notes             = models.TextField(blank=True, default="")
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    @property
    def is_overdue(self):
        if self.next_due_date is None:
            return False
        return self.next_due_date < timezone.now().date()

    @property
    def days_until_due(self):
        if self.next_due_date is None:
            return None
        return (self.next_due_date - timezone.now().date()).days

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    class Meta:
        ordering = ["next_due_date"]
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"
