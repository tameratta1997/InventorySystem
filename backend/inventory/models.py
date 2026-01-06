from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    quantity = models.IntegerField(default=0)
    min_stock_alert = models.IntegerField(default=10, help_text="Alert when stock falls below this level")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    supplier_name = models.CharField(max_length=100, blank=True, null=True, help_text="Optional Supplier Name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def is_low_stock(self):
        return self.quantity <= self.min_stock_alert

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
# ... existing StockLog code logic ...
    ACTION_CHOICES = [
        ('ADD', 'Stock Added'),
        ('REMOVE', 'Stock Removed'),
        ('SALE', 'Sold'),
        ('PURCHASE', 'Purchased'),
        ('ADJUST', 'Adjustment'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='logs')
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
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            last_sale = Sale.objects.all().order_by('id').last()
            if not last_sale:
                self.order_id = 'SO-0001'
            else:
                # Handle existing legacy sales without order_id gracefully if any, though we are adding a column
                 # Better to trust ID: But self.id is None on creation.
                 # Let's count + 1 or parse last string.
                 # Parsing is safer if rows are deleted.
                 try:
                     last_id = last_sale.order_id
                     if last_id and last_id.startswith('SO-'):
                        num = int(last_id.split('-')[1])
                        self.order_id = f'SO-{num + 1:04d}'
                     else:
                        self.order_id = 'SO-0001'
                 except (ValueError, IndexError, AttributeError):
                     self.order_id = 'SO-0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.date.strftime('%Y-%m-%d')}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price at the time of sale")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

class Purchase(models.Model):
    order_id = models.CharField(max_length=20, unique=True, editable=False, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    supplier = models.CharField(max_length=100, blank=True, null=True)
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
