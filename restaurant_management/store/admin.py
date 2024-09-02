from django.contrib import admin
from .models import MenuItem,Order,Inventory,Reservation,Table

admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(Inventory)
admin.site.register(Reservation)
admin.site.register(Table)

