from django.test import TestCase
from django.contrib.auth.models import User
from .forms import CheckoutForm, DiscountCodeForm


class TestCheckoutForm(TestCase):
    """Tests for the CheckoutForm"""

    def setUp(self):
        """Create test users"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@test.com"
        )
        self.staff_user = User.objects.create_user(
            username="staffuser",
            password="staffpass123",
            email="staff@test.com"
        )
        self.staff_user.is_staff = True
        self.staff_user.save()

    # ========== BASIC FORM TESTS ==========
    def test_checkout_form_valid_data(self):
        """Test checkout form with valid data"""
        form_data = {
            'shipping_address': '123 Main St, New York, NY 10001',
            'shipping_method': 'standard'
        }
        form = CheckoutForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_checkout_form_empty_address(self):
        """Test checkout form with empty shipping address"""
        form_data = {
            'shipping_address': '',
            'shipping_method': 'standard'
        }
        form = CheckoutForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_checkout_form_required_field(self):
        """Test that shipping_address is required"""
        form = CheckoutForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('shipping_address', form.errors)
        self.assertIn('shipping_method', form.errors)

    def test_checkout_form_long_address(self):
        """Test checkout form with long address - CharField has max_length=255"""
        # CharField with max_length=255 won't accept 255+ characters
        long_address = "123 Very Long Street Name That Goes On And On, City, State, Country 12345"
        form_data = {
            'shipping_address': long_address,
            'shipping_method': 'standard'
        }
        form = CheckoutForm(data=form_data)
        # This form should be valid with a reasonably long address
        self.assertTrue(form.is_valid())

    # ========== FIELD VISIBILITY TESTS ==========
    def test_checkout_form_regular_user_no_approved_field(self):
        """Test that regular users don't see the approved field"""
        form = CheckoutForm(user=self.user)
        self.assertNotIn('approved', form.fields)

    def test_checkout_form_staff_user_no_approved_field(self):
        """Test that even staff users don't see the approved field"""
        form = CheckoutForm(user=self.staff_user)
        self.assertNotIn('approved', form.fields)

    def test_checkout_form_no_user_no_approved_field(self):
        """Test form without user still doesn't include approved field"""
        form = CheckoutForm()
        self.assertNotIn('approved', form.fields)

    def test_checkout_form_has_shipping_address_field(self):
        """Test that form has shipping_address field"""
        form = CheckoutForm()
        self.assertIn('shipping_address', form.fields)

    # ========== UNICODE AND SPECIAL CHARACTER TESTS ==========
    def test_checkout_form_unicode_address(self):
        """Test checkout form with unicode characters in address"""
        form_data = {
            'shipping_address': '東京都渋谷区 123-4, Japan',
            'shipping_method': 'standard'
        }
        form = CheckoutForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_checkout_form_special_characters_address(self):
        """Test checkout form with special characters in address"""
        form_data = {
            'shipping_address': "123 O'Reilly Ave, São Paulo, BR 01310-100",
            'shipping_method': 'standard'
        }
        form = CheckoutForm(data=form_data)
        self.assertTrue(form.is_valid())

    # ========== FORM INSTANCE TESTS ==========
    def test_checkout_form_model_form_inheriance(self):
        """Test that CheckoutForm is a ModelForm"""
        form = CheckoutForm()
        self.assertTrue(hasattr(form, 'save'))

    def test_checkout_form_widget_type(self):
        """Test that shipping_address uses TextInput widget"""
        form = CheckoutForm()
        from django.forms import TextInput
        self.assertIsInstance(form['shipping_address'].field.widget, TextInput)


class TestDiscountCodeForm(TestCase):
    """Tests for the DiscountCodeForm"""

    # ========== BASIC FORM TESTS ==========
    def test_discount_form_valid_code(self):
        """Test discount form with valid code input"""
        form_data = {
            'code': 'SAVE10'
        }
        form = DiscountCodeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_discount_form_empty_code(self):
        """Test discount form with empty code"""
        form_data = {
            'code': ''
        }
        form = DiscountCodeForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_discount_form_required_field(self):
        """Test that code field is required"""
        form = DiscountCodeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('code', form.errors)

    def test_discount_form_whitespace_only(self):
        """Test discount form with whitespace only - Django cleans whitespace"""
        form_data = {
            'code': '   '
        }
        form = DiscountCodeForm(data=form_data)
        # Django strips whitespace, so this becomes empty and fails validation
        self.assertFalse(form.is_valid())

    # ========== CODE FORMAT TESTS ==========
    def test_discount_form_uppercase_code(self):
        """Test discount form with uppercase code"""
        form_data = {
            'code': 'SUMMER20'
        }
        form = DiscountCodeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_discount_form_lowercase_code(self):
        """Test discount form with lowercase code"""
        form_data = {
            'code': 'summer20'
        }
        form = DiscountCodeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_discount_form_mixed_case_code(self):
        """Test discount form with mixed case code"""
        form_data = {
            'code': 'Summer20'
        }
        form = DiscountCodeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_discount_form_numeric_code(self):
        """Test discount form with numeric code"""
        form_data = {
            'code': '12345'
        }
        form = DiscountCodeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_discount_form_special_characters(self):
        """Test discount form with special characters"""
        form_data = {
            'code': 'SAVE-10_OFF'
        }
        form = DiscountCodeForm(data=form_data)
        self.assertTrue(form.is_valid())

    # ========== LENGTH TESTS ==========
    def test_discount_form_max_length_code(self):
        """Test discount form with code at max length (50 chars)"""
        form_data = {
            'code': 'A' * 50
        }
        form = DiscountCodeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_discount_form_exceeds_max_length(self):
        """Test discount form with code exceeding max length"""
        form_data = {
            'code': 'A' * 51
        }
        form = DiscountCodeForm(data=form_data)
        self.assertFalse(form.is_valid())

    # ========== FIELD PROPERTIES TESTS ==========
    def test_discount_form_has_code_field(self):
        """Test that form has code field"""
        form = DiscountCodeForm()
        self.assertIn('code', form.fields)

    def test_discount_form_code_is_char_field(self):
        """Test that code field is a CharField"""
        form = DiscountCodeForm()
        from django.forms import CharField
        self.assertIsInstance(form.fields['code'], CharField)

    def test_discount_form_placeholder_attribute(self):
        """Test that code field has placeholder"""
        form = DiscountCodeForm()
        widget_attrs = form.fields['code'].widget.attrs
        self.assertIn('placeholder', widget_attrs)

    def test_discount_form_css_class_attribute(self):
        """Test that code field has Bootstrap CSS class"""
        form = DiscountCodeForm()
        widget_attrs = form.fields['code'].widget.attrs
        self.assertIn('class', widget_attrs)
        self.assertIn('form-control', widget_attrs['class'])

    # ========== WIDGET TESTS ==========
    def test_discount_form_text_input_widget(self):
        """Test that code field uses TextInput widget"""
        form = DiscountCodeForm()
        from django.forms import TextInput
        self.assertIsInstance(form.fields['code'].widget, TextInput)

    def test_discount_form_autocomplete_off(self):
        """Test that autocomplete is disabled"""
        form = DiscountCodeForm()
        widget_attrs = form.fields['code'].widget.attrs
        self.assertEqual(widget_attrs.get('autocomplete'), 'off')
