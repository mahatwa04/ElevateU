from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import json

from .models import EmailVerification
from .email_utils import generate_otp

User = get_user_model()


class OTPGenerationTestCase(TestCase):
    """Test OTP generation utility."""

    def test_otp_generation_length(self):
        """Test that OTP is 6 digits."""
        otp = generate_otp()
        self.assertEqual(len(otp), 6)

    def test_otp_is_numeric(self):
        """Test that OTP contains only digits."""
        otp = generate_otp()
        self.assertTrue(otp.isdigit())

    def test_otp_uniqueness(self):
        """Test that multiple OTPs are different."""
        otp1 = generate_otp()
        otp2 = generate_otp()
        self.assertNotEqual(otp1, otp2)


class RegisterAPITestCase(TestCase):
    """Test user registration endpoint."""

    def setUp(self):
        self.client = Client()
        self.register_url = '/api/auth/register/'

    def test_register_with_valid_bennett_email(self):
        """Test registration with valid @bennett.edu.in email."""
        data = {
            'username': 'testuser',
            'email': 'testuser@bennett.edu.in',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'field_of_interest': 'Computer Science',
        }
        response = self.client.post(self.register_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('user', response.json())
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'OTP sent to your campus email for verification.')

    def test_register_with_non_bennett_email(self):
        """Test registration fails with non-bennett.edu.in email."""
        data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'field_of_interest': 'Computer Science',
        }
        response = self.client.post(self.register_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json())

    def test_register_with_mismatched_passwords(self):
        """Test registration fails with mismatched passwords."""
        data = {
            'username': 'testuser',
            'email': 'testuser@bennett.edu.in',
            'password': 'TestPass123!',
            'password2': 'DifferentPass123!',
            'field_of_interest': 'Computer Science',
        }
        response = self.client.post(self.register_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_register_creates_email_verification_record(self):
        """Test that EmailVerification record is created on registration."""
        data = {
            'username': 'testuser',
            'email': 'testuser@bennett.edu.in',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'field_of_interest': 'Computer Science',
        }
        response = self.client.post(self.register_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        user = User.objects.get(email='testuser@bennett.edu.in')
        email_verifications = EmailVerification.objects.filter(user=user)
        self.assertEqual(email_verifications.count(), 1)
        self.assertFalse(email_verifications.first().is_verified)
        self.assertFalse(user.campus_verified)


class VerifyEmailAPITestCase(TestCase):
    """Test email verification endpoint."""

    def setUp(self):
        self.client = Client()
        self.verify_url = '/api/auth/verify-email/'
        
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@bennett.edu.in',
            password='TestPass123!',
            field_of_interest='Computer Science',
        )
        
        # Create OTP record
        self.otp = generate_otp()
        self.email_verification = EmailVerification.objects.create(
            user=self.user,
            otp_code=self.otp,
        )

    def test_verify_email_with_valid_otp(self):
        """Test email verification with valid OTP."""
        data = {
            'email': 'testuser@bennett.edu.in',
            'otp_code': self.otp,
        }
        response = self.client.post(self.verify_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())

        # Check user is now verified
        self.user.refresh_from_db()
        self.assertTrue(self.user.campus_verified)

        # Check EmailVerification record is marked as verified
        self.email_verification.refresh_from_db()
        self.assertTrue(self.email_verification.is_verified)

    def test_verify_email_with_invalid_otp(self):
        """Test email verification fails with invalid OTP."""
        data = {
            'email': 'testuser@bennett.edu.in',
            'otp_code': '000000',
        }
        response = self.client.post(self.verify_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_verify_email_with_expired_otp(self):
        """Test email verification fails with expired OTP."""
        # Set created_at to 11 minutes ago
        self.email_verification.created_at = timezone.now() - timedelta(minutes=11)
        self.email_verification.save()

        data = {
            'email': 'testuser@bennett.edu.in',
            'otp_code': self.otp,
        }
        response = self.client.post(self.verify_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('expired', response.json().get('non_field_errors', [{}])[0].lower() if response.json().get('non_field_errors') else False)

    def test_verify_already_verified_user(self):
        """Test email verification fails for already verified user."""
        self.user.campus_verified = True
        self.user.save()

        data = {
            'email': 'testuser@bennett.edu.in',
            'otp_code': self.otp,
        }
        response = self.client.post(self.verify_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_verify_email_nonexistent_user(self):
        """Test email verification fails for nonexistent user."""
        data = {
            'email': 'nonexistent@bennett.edu.in',
            'otp_code': self.otp,
        }
        response = self.client.post(self.verify_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

