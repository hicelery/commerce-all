from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestEnterView(TestCase):
    """Test enter_page view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@test.com"
        )

    def test_enter_view_loads(self):
        """Test enter view returns 200 status"""
        response = self.client.get(reverse('enter:enter'))
        self.assertEqual(response.status_code, 200)

    def test_enter_view_uses_correct_template(self):
        """Test correct template is used"""
        response = self.client.get(reverse('enter:enter'))
        self.assertTemplateUsed(response, 'enter/home.html')

    def test_enter_view_anonymous_user(self):
        """Test enter view accessible to anonymous users"""
        response = self.client.get(reverse('enter:enter'))
        self.assertEqual(response.status_code, 200)

    def test_enter_view_authenticated_user(self):
        """Test enter view accessible to authenticated users"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('enter:enter'))
        self.assertEqual(response.status_code, 200)

    def test_enter_view_post_request(self):
        """Test enter view handles POST requests"""
        response = self.client.post(reverse('enter:enter'))
        self.assertIn(response.status_code, [200, 405])

    def test_enter_view_head_request(self):
        """Test enter view handles HEAD requests"""
        response = self.client.head(reverse('enter:enter'))
        self.assertIn(response.status_code, [200, 405])

    def test_enter_view_url_name(self):
        """Test that enter URL name resolves correctly"""
        url = reverse('enter:enter')
        self.assertEqual(url, '/')

    def test_enter_view_response_type(self):
        """Test that response is HTML"""
        response = self.client.get(reverse('enter:enter'))
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_enter_view_context_exists(self):
        """Test that response has context"""
        response = self.client.get(reverse('enter:enter'))
        self.assertIsNotNone(response.context)

    def test_enter_view_multiple_requests(self):
        """Test that view handles multiple consecutive requests"""
        response1 = self.client.get(reverse('enter:enter'))
        response2 = self.client.get(reverse('enter:enter'))
        response3 = self.client.get(reverse('enter:enter'))
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)

    def test_enter_view_after_logout(self):
        """Test enter view after user logout"""
        self.client.login(username='testuser', password='testpass123')
        self.client.logout()
        response = self.client.get(reverse('enter:enter'))
        self.assertEqual(response.status_code, 200)

    def test_enter_view_no_redirect(self):
        """Test that enter view doesn't redirect"""
        response = self.client.get(reverse('enter:enter'), follow=False)
        self.assertEqual(response.status_code, 200)

    def test_enter_view_with_query_params(self):
        """Test enter view handles query parameters"""
        response = self.client.get(reverse('enter:enter') + '?param=value')
        self.assertEqual(response.status_code, 200)

    def test_enter_view_method_not_found(self):
        """Test enter view behavior"""
        response = self.client.get(reverse('enter:enter'))
        self.assertIsNotNone(response.content)

    def test_enter_view_response_is_not_empty(self):
        """Test that enter view returns content"""
        response = self.client.get(reverse('enter:enter'))
        self.assertGreater(len(response.content), 0)

    def test_enter_view_permission_anonymous(self):
        """Test no login required for enter view"""
        response = self.client.get(reverse('enter:enter'), follow=False)
        # Should not redirect to login page
        self.assertNotEqual(response.status_code, 302)
        self.assertEqual(response.status_code, 200)
