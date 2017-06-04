# -*- coding: utf-8 -*-
from django.test import TestCase
from hello.models import Contact
from model_mommy import mommy

# Create your tests here.


class SomeTestsModel(TestCase):

    def setUp(self):
        self.my_instance = mommy.make('hello.Contact', id=2, name=u'Олег', surname=u'Сенишин',
                                      bio=u'Працюю, після роботи, самостійно вивчаю Python, Django, JavaScript.'
                                      )

    def test_the_model(self):
        """Test the model Contact"""

        first_query = Contact.objects.get(id=2)
        self.assertEqual(first_query.name, self.my_instance.name)
        self.assertEqual(first_query.surname, self.my_instance.surname)
        self.assertEqual(first_query.bio, self.my_instance.bio)
        self.assertEqual(first_query.email, self.my_instance.email)
        self.assertEqual(first_query.date, self.my_instance.date)
        self.assertEqual(first_query.skype, self.my_instance.skype)
        self.assertEqual(first_query.contacts, self.my_instance.contacts)

    def test_that_data_base_is_not_empty(self):
        """ Test that data base is not empty first objects loads from fixtures and second I made with model_mommy"""

        object_list = Contact.objects.all()
        self.assertTrue(object_list)  # Test that database list is not empty

    def test_the_unicode_in_base(self):
        """Test in case unicode in base data """

        query = Contact.objects.get(id=2)
        self.assertEqual(query.__unicode__(), u'Олег Сенишин')
        self.assertEqual(query.bio, u'Працюю, після роботи, самостійно вивчаю Python, Django, JavaScript.')
