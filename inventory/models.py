from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Store(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    code = models.CharField(max_length=50, unique=True, db_index=True, help_text="Unique Product Code / Barcode")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Global quantity is now sum of Stock, but kept for legacy/cache compatibility temporarily
    # Ideally should be removed or made a property. We will use a property in views.
    quantity = models.IntegerField(default=0, help_text="Global total quantity") 
    min_stock_alert = models.IntegerField(default=10, help_text="Alert when stock falls below this level")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    supplier_name = models.CharField(max_length=100, blank=True, null=True, help_text="Optional Supplier Name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def total_stock(self):
        return self.stocks.aggregate(total=models.Sum('quantity'))['total'] or 0

    @property
    def is_low_stock(self):
        return self.total_stock <= self.min_stock_alert

class Stock(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='stocks')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('store', 'product') # One entry per product per store

    def __str__(self):
        return f"{self.store.name} - {self.product.name}: {self.quantity}"

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

class SalesPerson(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class StockLog(models.Model):
    ACTION_CHOICES = [
        ('ADD', 'Stock Added'),
        ('REMOVE', 'Stock Removed'),
        ('SALE', 'Sold'),
        ('PURCHASE', 'Purchased'),
        ('ADJUST', 'Adjustment'),
        ('TRANSFER_OUT', 'Transfer Out'),
        ('TRANSFER_IN', 'Transfer In'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='logs')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    quantity_change = models.IntegerField(help_text="Positive or negative change")
    reason = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.code} - {self.action} ({self.quantity_change})"

class Sale(models.Model):
    order_id = models.CharField(max_length=20, unique=True, editable=False, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    sales_person = models.ForeignKey(SalesPerson, on_delete=models.SET_NULL, null=True, blank=True)
    
    # New Fields for Store Management
    source_store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='sales_from', null=True) # Where items came from
    destination_store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='transfers_to', null=True, blank=True) # If transfer
    
    is_transfer = models.BooleanField(default=False)
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            prefix = 'TR-' if self.is_transfer else 'SO-'
            # Find last of this type
            last_sale = Sale.objects.filter(is_transfer=self.is_transfer).order_by('id').last()
            
            if not last_sale:
                self.order_id = f'{prefix}0001'
            else:
                 try:
                     last_id = last_sale.order_id
                     if last_id and last_id.startswith(prefix):
                        num = int(last_id.split('-')[1])
                        self.order_id = f'{prefix}{num + 1:04d}'
                     else:
                        self.order_id = f'{prefix}0001'
                 except (ValueError, IndexError, AttributeError):
                     self.order_id = f'{prefix}0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.date.strftime('%Y-%m-%d')}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price at the time of sale. 0 if transfer.")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        # If transfer, price is 0 (or handled by view logic, but double check here)
        if self.sale.is_transfer:
             self.unit_price = 0
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

class Purchase(models.Model):
    order_id = models.CharField(max_length=20, unique=True, editable=False, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    supplier = models.CharField(max_length=100, blank=True, null=True)
    
    # Store where goods are received
    destination_store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='purchases_in', null=True)
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            last_purchase = Purchase.objects.all().order_by('id').last()
            if not last_purchase:
                self.order_id = 'PO-0001'
            else:
                 try:
                     last_id = last_purchase.order_id
                     if last_id and last_id.startswith('PO-'):
                        num = int(last_id.split('-')[1])
                        self.order_id = f'PO-{num + 1:04d}'
                     else:
                        self.order_id = 'PO-0001'
                 except (ValueError, IndexError, AttributeError):
                     self.order_id = 'PO-0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.date.strftime('%Y-%m-%d')}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cost price at time of purchase")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_cost
        super().save(*args, **kwargs)
