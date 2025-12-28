from django import forms
from .models import Product

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission

class ImportFileForm(forms.Form):
    file = forms.FileField(label='Select CSV or Excel file', widget=forms.FileInput(attrs={'class': 'form-file', 'accept': '.csv, .xlsx, .xls'}))

class CustomUserCreationForm(UserCreationForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permissions (Products & Categories)"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('is_staff', 'is_superuser', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter permissions for just our inventory models
        self.fields['permissions'].queryset = Permission.objects.filter(
            content_type__app_label='inventory',
            content_type__model__in=['product', 'category']
        )

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.user_permissions.set(self.cleaned_data['permissions'])
        return user

class CustomUserChangeForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permissions (Products & Categories)"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff', 'is_superuser']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permissions'].queryset = Permission.objects.filter(
            content_type__app_label='inventory',
            content_type__model__in=['product', 'category']
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
