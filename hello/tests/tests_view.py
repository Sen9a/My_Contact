# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse, resolve
from hello.models import Contact
from model_mommy import mommy
from django.core import management
# Create your tests here.


class SomeTests(TestCase):

    def setUp(self):
        management.call_command('flush', interactive=False, load_initial_data=False)
        self.client = Client()
        self.my_instance = mommy.make('hello.Contact', id=1)
        self.response = self.client.get(reverse("my_info"))

    def test_the_info_view(self):
        """Test for the view returning hard-coded data for the template"""

        info_url = resolve('/')
        self.assertEqual(info_url.func.__name__, 'Info_view')
        self.assertEqual(self.response.status_code, 200)

    def test_for_template(self):
        """Test for template correctness"""
        self.assertTemplateUsed(self.response, 'my_info_template.html')

    def test_the_view_render_Contact_instance(self):
        """Test that view renders data from model"""

        my_info = self.response.context_data['info']
        self.assertIsInstance(my_info, Contact)

        model_instance = Contact.objects.first()
        self.assertIn(model_instance.name, self.response.content)
        self.assertIn(model_instance.surname, self.response.content)
        self.assertIn(model_instance.email, self.response.content)
        self.assertIn(model_instance.bio, self.response.content)
        self.assertIn(model_instance.skype, self.response.content)
        self.assertIn(model_instance.contacts, self.response.content)

    def test_the_unicode_in_data_base(self):
        """Test if unicode is in data base"""

        model_instance = Contact.objects.first()
        model_instance.name = u'Олег'
        model_instance.surname = u'Сенишин'
        model_instance.bio = u'Працюю, після роботи, самостійно вивчаю Python, Django, JavaScript.'
        model_instance.save()

        response = self.client.get(reverse("my_info"))

        model_instance = Contact.objects.get(id=1)

        self.assertIn(model_instance.name.encode('utf-8'), response.content)
        self.assertIn(model_instance.surname.encode('utf-8'), response.content)
        self.assertIn(model_instance.email.encode('utf-8'), response.content)
        self.assertIn(model_instance.bio.encode('utf-8'), response.content)
        self.assertIn(model_instance.skype.encode('utf-8'), response.content)
        self.assertIn(model_instance.contacts.encode('utf-8'), response.content)

    def test_in_case_base_data_is_empty(self):
        """Test that nothing breaks when database is empty"""

        Contact.objects.all().delete()
        obj_list = Contact.objects.all()
        self.assertFalse(obj_list)

        response = self.client.get(reverse("my_info"))
        my_info = response.context_data['info']
        self.assertIsNone(my_info)
        self.assertEqual(response.status_code, 200)
