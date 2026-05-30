from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone

from tracker.models import Equipment
from .models import Notification


STATUS_MESSAGES = {
    'in_service': (
        "🔧 Equipment '{name}' (S/N: {serial}) has  been placed IN SERVICE"
        "AT {location}."
    ),
    'under_maintenance': (
        "🛠️ Equipment '{name}' (S/N: {serial}) has been UNDER MAINTENANCE"
        "at {location}."
    ),
    'out_of_service': (
    "🚫Equipment '{name}' (S/N: {serial}) has been marked"
    "OUT OF SERVICE at {location}."
    ),
}
def get_all_staff():
    """Return all staff/admin users who receive notifications."""
    return User.objects.filter(is_staff=True)


def notification_already_exists( equipment, status_type):
    """
    Return Trues if an unread notification for this equipment
    and status_type already exists - prevents duplicates
    """
    return Notification.objects.filter(
        equipment=equipment,
        status=status_type,
        is_read=False,
        is_dismissed=False,
    ).exists()

def create_notification_for_all_staff(equipment, status_type, message):
    """Creates one notification per staff user."""
    for user in get_all_staff():
        Notification.objects.create(
            equipment=equipment,
            user=user,
            status=status_type,
            message=message,
        )

#Signal 1 this fires when status changes
#using pre_save to compare old and new status so we only notify

@receiver(pre_save, sender=Equipment)
def track_status_change(sender, instance, **kwargs):
    """
    store the previous status on the instance before saving
    we read this in post_save to detect is status changed.
    """
    if instance.pk:  #only for existing records not brand new records
        try:
            old = Equipment.objects.get(pk=instance.pk)
            instance._prev_save_status = old.status
            instance._prev_critical = old.critical
        except Equipment.DoesNotExist:
            instance._prev_status = None
            instance._prev_critical = None
        else:
            # Brand new equipment — no previous status
            instance._prev_status = None
            instance._prev_critical = None

@receiver(post_save, sender=Equipment)
def create_status_notification(sender, instance, created, **kwargs):
    """
    Fires after every Equipment save.
    Creates a notification when:
    1. A new Equipment is created (any status).
    2. An existing equipment's status changes
    3. Equipment is marked critical=True
    4. Equipment's next_due_date has passed. (overdue)
    """

    #shortcut variables
    name     = instance.name
    serial   = instance.serial_number
    location = instance.location


    #CASE 1: Brand new equipment was just created.
    if created:
        msg = (
            f"✅ New equipment '{name}' (S/N: {serial}) has been added"
            f"to the system at {location}."
            f"Status: {instance.get_status_display()}."
        )
        create_notification_for_all_staff(instance, instance.status, msg)

        # CASE 2: Status changed on existing equipment
    elif hasattr(instance, '_prev_status') and instance._prev_status != instance.status:
        if instance.status in STATUS_MESSAGES:
            msg = STATUS_MESSAGES[instance.status].format(
                name=name,
                serial=serial,
                location=location,
            )
            if not notification_already_exists(instance, instance.status):
                create_notification_for_all_staff(instance, instance.status, msg)

    #CASE 3 Critical flag just turned On

    if (
        hasattr(instance, '_prev_critical')
        and not instance._prev_critical
        and instance.critical
    ):
        msg = (
            f"🔴 CRITICAL ALERT: Equipment '{name}' (S/N: {serial})"
            f"at {location} has been flagged as CRITICAL and requires "
            f"immediate attention !"
        )
        if not notification_already_exists(instance, 'critical'):
            create_notification_for_all_staff(instance, 'critical', msg)

#CASE 4: Overdue check (next_due_date has passed)
    if instance.is_overdue:  # uses the @property on your model
        msg = (
            f"⚠️ OVERDUE: Equipment '{name}' (S/N: {serial}) at {location} "
            f"was due on {instance.next_due_date.strftime('%d %b %Y')} "
            f"and has not been serviced."
        )
        if not notification_already_exists(instance, 'overdue'):
            create_notification_for_all_staff(instance, 'overdue', msg)
