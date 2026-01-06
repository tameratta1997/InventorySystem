from django.contrib import admin
from .models import Category, Product, StockLog, Sale, SaleItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'purchase_price', 'selling_price', 'quantity', 'is_low_stock')
    search_fields = ('name', 'code')
    list_filter = ('category',)
    readonly_fields = ('created_at', 'updated_at')

    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True

@admin.register(StockLog)
class StockLogAdmin(admin.ModelAdmin):
    list_display = ('product', 'action', 'quantity_change', 'user', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('product__name', 'product__code', 'reason')

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'date')
    inlines = [SaleItemInline]
