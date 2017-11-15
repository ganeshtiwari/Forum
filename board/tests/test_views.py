from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..views import home, board_topics, new_topic
from ..models import Board, Topic, Post
from ..forms import NewTopicForm

# Create your tests here.
class HomeTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='This is django')
        url = reverse('board:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_to_index_view(self):
        view = resolve('/board/')
        self.assertEquals(view.func, home)
    
    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board:board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))

class BoardTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='This is django')
    
    def test_board_topics_view_success_status(self):
        url = reverse('board:board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board:board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/board/1/')
        self.assertEquals(view.func, board_topics)
    
    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board:board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        home_page_url = reverse('board:home')
        self.assertContains(response, 'href="{0}"'.format(home_page_url))
        new_topc_url = reverse('board:new_topic', kwargs={'pk': 1})
        self.assertContains(response, 'href="{0}"'.format(new_topc_url))



def NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='This is django')
        User.objects.create(username='john', email='john@gmail.com', password=123)

    def test_new_topic_view_success_status_code(self):
        url = reverse('board:new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)
    
    def test_new_topic_view_not_found_status_code(self):
        url = reverse('board:new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(self.response.status_code, 404)
    
    def test_new_topic_url_resolves_to_new_topic_view(self):
        view = resolve('/board/1/new')
        self.assertEquals(view.func, board_topics)
    
    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('board:new_topics', kwargs={'pk': 1})
        board_topics_url = reverse('board:board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):
        url = reverse('board:new_topic', kwargs={'pk': 1})
        response = client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_valid_new_topic_post_data(self):
        url = reverse('board:new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test subject',
            'message': 'Test message'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())
    
    def test_new_topic_invalid_post_data(self):
        url = reverse('board:new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)
    
    def test_new_topic_invalid_post_data_empty_fields(self):
        url = reverse('board:new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)        
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())
    
    def test_contains_form(self):
        url = reverse('board:new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)
    
    def test_new_topic_invalid_post_data(self):
        url = reverse('board:new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
