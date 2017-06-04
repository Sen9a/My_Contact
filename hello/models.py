from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    date = models.DateField()
    bio = models.TextField(blank=True)
    email = models.EmailField()
    skype = models.CharField(max_length=200)
    contacts = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.surname)
