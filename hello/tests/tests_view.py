# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse, resolve
from hello.models import Contact
from model_mommy import mommy
from django.core import management
from hello.form import My_add_data_form
from datetime import date
from django.contrib.auth.models import User
import json
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


class EditData(TestCase):
    def setUp(self):
        management.call_command('flush', interactive=False, load_initial_data=False)
        self.client = Client()
        self.my_instance = mommy.make('hello.Contact', id=1)
        self.response = self.client.get(reverse("to_form", args=str(self.my_instance.id)))
        my_admin = User.objects.create_superuser('admin', 'myemail@test.com', 'admin')

    def test_form(self):
        """Test form"""

        form = My_add_data_form(data={'name': 'Oleg'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['surname'] and form.errors['date']
                         and form.errors['email'] and form.errors['skype'],
                         ['This field is required.'])

    def test_form_date_validation(self):
        """Test for form date field validation"""

        form = My_add_data_form(data={'date': date(1800, 05, 03)})
        self.assertEqual(form.errors['date'], ['You already dead now'])
        form = My_add_data_form(data={'date': date(2200, 05, 03)})
        self.assertEqual(form.errors['date'], ['You not born yet'])

    def test_the_data_edit_url(self):
        """Test for the view returning hard-coded data for the template"""

        my_instance = Contact.objects.first()
        info_url = resolve('/to_form/%s/' % my_instance.id)
        self.assertEqual(info_url.func.__name__, 'my_edit_data')
        self.assertEqual(self.response.status_code, 200)

    def test_user_login_view(self):
        """Test login"""

        url = reverse('my_login')
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'username': 'admin'}, json.loads(response.content))

    def test_user_login_view_error(self):
        """Test login error"""

        url = reverse('my_login')
        data = {'username': 'Petro', 'password': "admin"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'user_error': "Your username and password didn't match."}, json.loads(response.content))

    def test_user_logout(self):
        """Test logout"""

        url = reverse('my_logout')
        response = self.client.post(url, format='json')
        self.assertEqual(json.loads(response.content), {'bay': 'Bay bay '})

    def test_that_view_return_errors_in_json(self):
        """Test that view return errors in Json format"""

        self.client.login(username='admin', password='admin')
        url = reverse("to_form", args=str(self.my_instance.id))
        response = self.client.post(url, data={'name': 'Oleg'}, format='json')
        self.assertEqual(response.status_code, 200)
        for c in json.loads(response.content):
            self.assertEqual(['This field is required.'], json.loads(response.content)[c])

    def test_that_view_saves_data_if_form_valid(self):
        """Test that view saves data if form valid"""

        self.client.login(username='admin', password='admin')
        url = reverse("to_form", args=str(self.my_instance.id))
        response = self.client.post(url, data={'name': 'Oleg', 'surname': 'Senyshyn', 'date': date(1995, 05, 03),
                                               'email': 'sen9a1990@gmail.com', 'skype': 'sen9a1990'}, format='json')
        self.assertEqual('Data has been edit', json.loads(response.content)['ok'])
        my_instance = Contact.objects.first()
        self.assertEqual('Oleg', my_instance.name)
        self.assertEqual('Senyshyn', my_instance.surname)
        self.assertEqual(date(1995, 05, 03), my_instance.date)
        self.assertEqual('sen9a1990@gmail.com', my_instance.email)
        self.assertEqual('sen9a1990', my_instance.skype)
