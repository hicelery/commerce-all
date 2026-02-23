from django.test import TestCase
from django.contrib.auth.models import User
from .forms import ReviewForm


class TestReviewForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="myUsername",
            password="myPassword",
            email="test@test.com"
        )

    def test_form_is_valid(self):
        """ Test for all fields"""

        form = ReviewForm({
            'name': 'test name',
            'email': 'test@test.com',
            'product': 1,
            'user': self.user.id,
            'rating': 5,
            'title': 'Great product!',
            'comment': 'I really enjoyed using this product. Highly recommend it!'
        })
        self.assertTrue(form.is_valid(),
                        msg=f"Form is not valid errors: {form.errors}")
