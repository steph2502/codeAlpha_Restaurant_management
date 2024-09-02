
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import MenuItem, Order, Inventory, Reservation,Table
from .forms import OrderForm, ReservationForm  
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Sum ,F, Count, Q
from django.db.models.functions import TruncMonth

def menu(request):
    items = MenuItem.objects.all()
    return render(request, 'menu.html', {'items': items})

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, ("Order successfully taken!"))
            return redirect('process_order',order_id=order.id)
        else:
            messages.success(request, ("Invalid format!,try again"))
    else:
        form = OrderForm()
    tables = Table.objects.all()
    return render(request, 'place_order.html', {'form': form,'tables': tables})



def process_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    table = order.table 

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES):  
            order.status = status
            order.save()
            messages.success(request, "Order status updated successfully!")
        else:
            messages.error(request, "Invalid status value.")

        return redirect('menu') 

    context = {
        'order': order,
        'table_status': table.status if table else 'No Table Assigned',
    }

    return render(request, 'process_order.html', context)



def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
        else:
            messages.success(request, ("Invalid format!,try again"))
    else:
        form = ReservationForm()
    return render(request, 'make_reservation.html', {'form': form})

def manage_table(request):
    tables = Table.objects.all()
    return render(request, 'manage_table.html', {'tables': tables})

def manage_inventory(request):
    items = MenuItem.objects.all()
    
    if request.method == 'POST':
        menu_item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 0))
        item = get_object_or_404(MenuItem, id=menu_item_id)
        
        try:
            item.reduce_stock(quantity)
            message = "Stock successfully reduced."
        except ValueError as e:
            message = str(e)
        
        return render(request, 'manage_inventory.html', {'items': items, 'message': message})

    return render(request, 'manage_inventory.html', {'items': items})


def generate_report(request):
    total_revenue = Order.objects.filter(status='completed').aggregate(total_revenue=Sum(F('menu_item__price') * F('quantity')))['total_revenue']
    total_orders = Order.objects.filter(status='completed').count()
    avg_order_value = Order.objects.filter(status='completed').aggregate(avg_order_value=Sum(F('menu_item__price') * F('quantity')) / Count('id'))['avg_order_value']
    popular_items = Order.objects.filter(status='completed').values('menu_item__name').annotate(total_sold=Sum('quantity')).order_by('-total_sold')[:5]
    least_popular_items = Order.objects.filter(status='completed').values('menu_item__name').annotate(total_sold=Sum('quantity')).order_by('total_sold')[:5]
    low_stock_items = MenuItem.objects.filter(inventory__lt=10)
    revenue_per_month = Order.objects.filter(status='completed').annotate(month=TruncMonth('created_at')).values('month').annotate(total_revenue=Sum(F('menu_item__price') * F('quantity'))).order_by('month')

    return render(request, 'report.html', {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'popular_items': popular_items,
        'least_popular_items': least_popular_items,
        'low_stock_items': low_stock_items,
        'revenue_per_month': revenue_per_month,
    })



