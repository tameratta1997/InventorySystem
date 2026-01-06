from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/import/', views.product_import, name='product_import'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('pos/', views.pos_view, name='pos'),
    path('purchase/', views.purchase_view, name='purchase'),
    path('reports/', views.report_view, name='reports'),
    path('transaction/<str:type>/<int:id>/', views.transaction_detail, name='transaction_detail'),
    
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_create'),
    path('customers/import/', views.customer_import, name='customer_import'),
    path('customers/<int:pk>/edit/', views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    
    path('salespeople/', views.salesperson_list, name='salesperson_list'),
    path('salespeople/add/', views.salesperson_create, name='salesperson_create'),
    path('salespeople/import/', views.salesperson_import, name='salesperson_import'),
    path('salespeople/<int:pk>/edit/', views.salesperson_update, name='salesperson_update'),
    path('salespeople/<int:pk>/delete/', views.salesperson_delete, name='salesperson_delete'),
]

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'api/products', views.ProductViewSet)
router.register(r'api/categories', views.CategoryViewSet)

urlpatterns += router.urls
