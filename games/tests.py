from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Game

class GameModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_game = Game.objects.create(
            author = test_user,
            title = 'Title of Blog',
            body = 'Words about the blog'
        )
        test_game.save()

    def test_blog_content(self):
        game = Game.objects.get(id=1)

        self.assertEqual(str(game.author), 'tester')
        self.assertEqual(game.title, 'Title of Blog')
        self.assertEqual(game.body, 'Words about the blog')

class APITest(APITestCase):
    def test_list(self):
        response = self.client.get(reverse('games_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail(self):

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_game = Game.objects.create(
            author = test_user,
            title = 'Title of Blog',
            body = 'Words about the blog'
        )
        test_game.save()

        response = self.client.get(reverse('games_detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id':1,
            'title': test_game.title,
            'body': test_game.body,
            'author': test_user.id,
        })


    def test_create(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        url = reverse('games_list')
        data = {
            "title":"Testing is Fun!!!",
            "body":"when the right tools are available",
            "author":test_user.id,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, test_user.id)

        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Game.objects.get().title, data['title'])

    def test_update(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_game = Game.objects.create(
            author = test_user,
            title = 'Title of Blog',
            body = 'Words about the blog'
        )

        test_game.save()

        url = reverse('games_detail',args=[test_game.id])
        data = {
            "title":"Testing is Still Fun!!!",
            "author":test_game.author.id,
            "body":test_game.body,
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, url)

        self.assertEqual(Game.objects.count(), test_game.id)
        self.assertEqual(Game.objects.get().title, data['title'])


    def test_delete(self):
        """Test the api can delete a game."""

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_game = Game.objects.create(
            author = test_user,
            title = 'Title of Blog',
            body = 'Words about the blog'
        )

        test_game.save()

        game = Game.objects.get()

        url = reverse('games_detail', kwargs={'pk': game.id})


        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, url)