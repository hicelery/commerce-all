from .models import ProductReview
from django import forms


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # accept optional `user` kwarg; remove `approved` for non-staff users
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not (user and getattr(user, 'is_staff', False)):
            # hide/remove approved field for regular users
            self.fields.pop('approved', None)

    class Meta:
        model = ProductReview
        fields = ('rating', 'title', 'comment', 'approved')
