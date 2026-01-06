from django import forms
from .models import Product

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission

class ImportFileForm(forms.Form):
    file = forms.FileField(label='Select CSV or Excel file', widget=forms.FileInput(attrs={'class': 'form-file', 'accept': '.csv, .xlsx, .xls'}))

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('is_staff', 'is_superuser', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add permissions field dynamically
        self.fields['permissions'] = forms.ModelMultipleChoiceField(
            queryset=Permission.objects.filter(
                content_type__app_label='inventory',
                content_type__model__in=['product', 'category']
            ),
            widget=forms.CheckboxSelectMultiple,
            required=False,
            label="Assign Permissions (Products & Categories)"
        )

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.user_permissions.set(self.cleaned_data['permissions'])
        return user

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff', 'is_superuser']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permissions'] = forms.ModelMultipleChoiceField(
            queryset=Permission.objects.filter(
                content_type__app_label='inventory',
                content_type__model__in=['product', 'category']
            ),
            widget=forms.CheckboxSelectMultiple,
            required=False,
            label="Assign Permissions (Products & Categories)"
        )
        if self.instance.pk:
            self.fields['permissions'].initial = self.instance.user_permissions.all()

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.user_permissions.set(self.cleaned_data['permissions'])
        return user

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'category', 'purchase_price', 'selling_price', 'quantity', 'min_stock_alert', 'description', 'image', 'supplier_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Product Name'}),
            'code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Barcode/Code'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input'}),
            'min_stock_alert': forms.NumberInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'supplier_name': forms.TextInput(attrs={'class': 'form-input'}),
            'image': forms.FileInput(attrs={'class': 'form-file'}),
        }

from .models import Customer
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'address', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
             'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email (Optional)'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Address'}),
        }

from .models import SalesPerson
class SalesPersonForm(forms.ModelForm):
    class Meta:
        model = SalesPerson
        fields = ['name', 'phone', 'email', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email (Optional)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5'}),
        }
