from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import EquipmentForm
from .models import Equipment


def _stats():
    today = timezone.now().date()
    return {
        'total':       Equipment.objects.count(),
        'in_service':  Equipment.objects.filter(status=Equipment.Status.IN_SERVICE).count(),
        'maintenance': Equipment.objects.filter(status=Equipment.Status.UNDER_MAINTENANCE).count(),
        'out_service': Equipment.objects.filter(status=Equipment.Status.OUT_OF_SERVICE).count(),
        'overdue':     Equipment.objects.filter(next_due_date__lt=today).count(),
        'critical':    Equipment.objects.filter(critical=True).count(),
        'due_soon':    Equipment.objects.filter(
                           next_due_date__gte=today,
                           next_due_date__lte=today + timedelta(days=14)
                       ).count(),
    }


@login_required
def dashboard(request):
    today       = timezone.now().date()
    overdue_items  = Equipment.objects.filter(next_due_date__lt=today).order_by('next_due_date')[:5]
    due_soon_items = Equipment.objects.filter(
        next_due_date__gte=today,
        next_due_date__lte=today + timedelta(days=14)
    ).order_by('next_due_date')[:5]
    recent = Equipment.objects.order_by('-created_at')[:5]
    return render(request, 'tracker/dashboard.html', {
        'overdue_items': overdue_items,
        'due_soon_items': due_soon_items,
        'recent': recent,
        **_stats(),
    })


@login_required
def equipment_list(request):
    qs = Equipment.objects.all()
    q         = request.GET.get('q', '').strip()
    status    = request.GET.get('status', '')
    condition = request.GET.get('condition', '')
    critical  = request.GET.get('critical', '')
    sort      = request.GET.get('sort', 'next_due_date')

    if q:
        qs = qs.filter(Q(name__icontains=q)|Q(serial_number__icontains=q)|Q(location__icontains=q))
    if status:    qs = qs.filter(status=status)
    if condition: qs = qs.filter(condition=condition)
    if critical == 'yes': qs = qs.filter(critical=True)
    if sort in ['next_due_date','-next_due_date','name','-name','-updated_at']:
        qs = qs.order_by(sort)

    return render(request, 'tracker/equipment_list.html', {
        'equipments': qs, 'q': q, 'status': status,
        'condition': condition, 'critical': critical, 'sort': sort,
        'status_choices':    Equipment.Status.choices,
        'condition_choices': Equipment.Condition.choices,
        **_stats(),
    })


@login_required
def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    return render(request, 'tracker/equipment_detail.html', {'equipment': equipment, **_stats()})


@login_required
def equipment_overdue(request):
    today = timezone.now().date()
    equipments = Equipment.objects.filter(next_due_date__lt=today).order_by('next_due_date')
    return render(request, 'tracker/equipment_list.html', {
        'equipments': equipments, 'is_overdue_view': True,
        'status_choices': Equipment.Status.choices,
        'condition_choices': Equipment.Condition.choices,
        **_stats(),
    })


@login_required
def equipment_create(request):
    form = EquipmentForm(request.POST or None)
    if form.is_valid():
        eq = form.save()
        messages.success(request, f'"{eq.name}" was added successfully.')
        return redirect('tracker:equipment_detail', pk=eq.pk)
    return render(request, 'tracker/equipment_form.html', {'form': form, 'action': 'Add', **_stats()})


@login_required
def equipment_edit(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    form = EquipmentForm(request.POST or None, instance=equipment)
    if form.is_valid():
        form.save()
        messages.success(request, f'"{equipment.name}" updated successfully.')
        return redirect('tracker:equipment_detail', pk=equipment.pk)
    return render(request, 'tracker/equipment_form.html', {
        'form': form, 'equipment': equipment, 'action': 'Edit', **_stats()
    })


@login_required
def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        name = equipment.name
        equipment.delete()
        messages.success(request, f'"{name}" was deleted.')
        return redirect('tracker:equipment_list')
    return render(request, 'tracker/equipment_confirm_delete.html', {'equipment': equipment, **_stats()})
