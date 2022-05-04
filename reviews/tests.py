from django.test import TestCase, Client
from django.test import tag
from django.urls import reverse
from .models import Reviews
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from datetime import date


@tag('views')
class TestReviewView(TestCase):
    def test_list_review_uses_correct_template(self):
        today = date.today()

        test_user = User.objects.create_user(
                username='testuser3', password='testpw1'
                )
        review = Reviews.objects.create(user= test_user,
                                            text='first review',
                                            created_on=today,
                                            approved=False,
                                                is_active=False
                                                )
        response = self.client.get(reverse('reviews:reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review.html')


@tag('models')
class TestReiewsModels(TestCase):
    
    def test_review_string_method_returns_correct_output(self):
        today = date.today()

        test_user = User.objects.create_user(
                username='testuser3', password='testpw1'
                )
        review = Reviews.objects.create(user= test_user,
                                            text='first review',
                                            created_on=today,
                                            approved=False,
                                                is_active=False
                                                )

        self.assertEqual(str(review.user.username), 'testuser3')
        