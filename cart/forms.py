from .models import Cart, CartItem, Order, OrderItem
from django import forms


class CheckoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # accept optional `user` kwarg; remove `approved` for non-staff users
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not (user and getattr(user, 'is_staff', False)):
            # hide/remove approved field for regular users
            self.fields.pop('approved', None)

    class Meta:
        model = Order
        fields = ('shipping_address',)


class DiscountCodeForm(forms.Form):
    """Form to input and apply a discount code."""
    code = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter discount code',
            'autocomplete': 'off'
        })
    )
