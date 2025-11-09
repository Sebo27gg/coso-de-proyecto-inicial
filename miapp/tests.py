from django.test import TestCase

# Create your tests here.
from django.core.mail import send_mail

send_mail(
    "Password reset test",
    "This is a test email from Django",
    "allergeat111@gmail.com",
    ["aderesoadereso1@gmail.com"],
    fail_silently=False,
)