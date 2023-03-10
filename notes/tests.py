from django.test import TestCase
from .models import Note, Category
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import datetime


def create_test_user():
    """Create a test user"""
    return User.objects.create_user(username='user', password='qwerty')


def create_test_note(category=None, reminder=None):
    """Create a test note"""
    return Note.objects.create(title='Test note', text='Test text', author=create_test_user(),
                               category=category, reminder=reminder)


class TestNotesCreation(TestCase):
    def test_note_creation(self):
        """Test that note is created correctly"""
        note = create_test_note()
        self.assertEqual(note.title, 'Test note')
        self.assertEqual(note.text, 'Test text')
        self.assertEqual(note.author.username, 'user')
        self.assertEqual(note.category, None)
        self.assertEqual(note.reminder, None)

    def test_note_creation_with_category(self):
        """Test that note is created correctly with category"""
        category = Category.objects.create(title='Test category')
        note = create_test_note(category=category)
        self.assertEqual(note.title, 'Test note')
        self.assertEqual(note.text, 'Test text')
        self.assertEqual(note.author.username, 'user')
        self.assertEqual(note.category.title, 'Test category')
        self.assertEqual(note.reminder, None)

    def test_note_creation_with_reminder(self):
        """Test that note is created correctly with reminder"""
        reminder = datetime.datetime.now(tz=timezone.utc)
        note = create_test_note(reminder=reminder)
        self.assertEqual(note.title, 'Test note')
        self.assertEqual(note.text, 'Test text')
        self.assertEqual(note.author.username, 'user')
        self.assertEqual(note.category, None)
        self.assertEqual(note.reminder, reminder)


class TestViews(TestCase):

    def test_new_note_view_if_user_logged_in(self):
        """Test that new note view returns 200 if user is logged in"""
        create_test_user()
        self.client.login(username='user', password='qwerty')
        response = self.client.get(reverse('new_note'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_form.html')

    def test_new_note_saved(self):
        """Test that new note is created and saved to the database if user is logged in"""
        user = create_test_user()
        self.client.login(username='user', password='qwerty')
        note_content = {
            'title': 'New note',
            'text': 'New text',
        }
        request = self.client.post(reverse('new_note'), note_content)
        note = Note.objects.get(author=user)
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, reverse('note_detail', args=[note.id]))
        self.assertEqual(note.title, 'New note')
        self.assertEqual(note.text, 'New text')
        self.assertEqual(note.author.username, 'user')

    def test_edit_note_view_if_user_logged_in(self):
        """Test that edit note view returns 200 if user is logged in"""
        note = create_test_note()
        self.client.login(username='user', password='qwerty')
        response = self.client.get(reverse('edit_note', args=[note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_form.html')

    def test_edit_note_view_saved(self):
        """Test that changes made to note are saved if user is logged in and edit note view is used"""
        note = create_test_note()
        self.client.login(username='user', password='qwerty')
        changes = {
            'title': 'New title',
            'text': 'New text',
        }
        request = self.client.post(reverse('edit_note', args=[note.id]), changes)
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, reverse('note_detail', args=[note.id]))
        note.refresh_from_db()
        self.assertEqual(note.title, 'New title')
        self.assertEqual(note.text, 'New text')

    def test_edit_note_view_if_user_not_logged_in(self):
        """Test that edit note view returns 302 if user is not logged in and redirects to note_detail"""
        note = create_test_note()
        response = self.client.get(reverse('edit_note', args=[note.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('note_detail', args=[note.id]))

    def test_delete_note_view_if_user_logged_in(self):
        """Test that ensures that delete_note view deletes note and redirects to homepage"""
        note = create_test_note()
        self.client.login(username='user', password='qwerty')
        response = self.client.get(reverse('delete_note', args=[note.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(pk=note.id).exists())
        self.assertEqual(response.url, reverse('home'))

    def test_delete_note_view_if_user_not_logged_in(self):
        """Test that ensures that delete_note view does not delete note and redirects to note detail page"""
        note = create_test_note()
        response = self.client.get(reverse('delete_note', args=[note.id]))
        self.assertTrue(Note.objects.filter(pk=note.id).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('note_detail', args=[note.id]))
