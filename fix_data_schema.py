import os
import django

# Setup Django Environment
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from inventory.models import Store, Product, Stock

def migrate_stock():
    print("Migrating stock data...")
    # 1. Get or Create Default Store
    default_store, created = Store.objects.get_or_create(
        name="Main Store", 
        defaults={'location': 'Default Location'}
    )
    if created:
        print(f"Created default store: {default_store.name}")
    else:
        print(f"Using default store: {default_store.name}")

    # 2. Iterate Products
    products = Product.objects.all()
    count = 0
    for p in products:
        if p.quantity != 0:
            # Check if stock entry exists
            stock, created = Stock.objects.get_or_create(store=default_store, product=p)
            if created or stock.quantity == 0:
                stock.quantity = p.quantity # Copy global quantity to store
                stock.save()
                print(f"Migrated {p.name}: {p.quantity} units -> {default_store.name}")
                count += 1
            else:
                 # Stock already exists, maybe from previous run?
                 # If we assume global quantity is the truth, we might overwrite. 
                 # But if partial migration happened, we might duplicate.
                 # Safe bet: If stock.quantity is 0, take global.
                 pass

    print(f"Migration complete. {count} products updated.")

if __name__ == '__main__':
    migrate_stock()
