from django import forms
from .models import Contact, OrderQuery


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'type', 'message')


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderQuery
        fields = ('name', 'email', 'order_id', 'message')
