from django.db import models



class Table(models.Model):
    table_number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"


class Inventory(models.Model):
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.item_name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE,default=1)

    def is_in_stock(self):
        return self.inventory.quantity > 0  

    def reduce_stock(self, quantity):
        if self.is_in_stock() and self.inventory.quantity >= quantity:
            self.inventory.quantity -= quantity  
            self.inventory.save()  
        else:
            raise ValueError("Insufficient stock")

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    customer = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def total_cost(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"Order by {self.customer} for {self.menu_item.name}"

    



class Reservation(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    party_size = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.name} - {self.date}"


