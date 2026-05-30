from django.db import models
from tracker.models import Equipment
from django.contrib.auth.models import User
# Create your models here.


class Notification(models.Model):

    STATUS_CHOICES = [
        ('in_service', 'In Service'),
        ('under_maintenance', 'Under Maintenance'),
        ('out_of_service', 'Out Of Service'),
        ('critical', 'Critical'),
        ('overdue', 'Overdue'),
    ]

    equipment = models.ForeignKey(
        'tracker.Equipment',
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    status  = models.CharField(max_length=20, choices=STATUS_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_status_type_display()}] {self.equipment.name}"