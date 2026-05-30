from .models import Notification


def notifications_processor(request):
    if not request.user.is_authenticated:
        return {}

    unread = Notification.objects.filter(
        user=request.user,
        is_read=False,
        is_dismissed=False,
    ).select_related('equipment').order_by('-created_at')

    critical = unread.filter(status='critical')

    return {
        'unread_notifications': unread,
        'critical_notifications': critical,
        'unread_count': unread.count(),
    }