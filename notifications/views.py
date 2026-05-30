from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification


@login_required
def dismiss(request, pk):
    Notification.objects.filter(
        pk=pk,
        user=request.user
    ).update(is_read=True, is_dismissed=True)
    return JsonResponse({'status': 'ok'})


@login_required
def mark_all_read(request):
    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def notification_list(request):
    from django.shortcuts import render
    notifications = Notification.objects.filter(
        user=request.user,
        is_dismissed=False
    ).select_related('equipment').order_by('-created_at')
    return render(request, 'notifications/list.html', {
        'notifications': notifications
    })

