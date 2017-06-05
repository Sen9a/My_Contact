from django.db import models
from PIL import Image as Img
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    date = models.DateField()
    bio = models.TextField(blank=True)
    email = models.EmailField()
    skype = models.CharField(max_length=200)
    contacts = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos', blank=True)

    def save(self, *args, **kwargs):
        if self.image:
            new_image = Img.open(StringIO.StringIO(self.image.read()))
            new_image.thumbnail((200, 200), Img.ANTIALIAS)
            output = StringIO.StringIO()
            new_image.save(output, format='JPEG', quality=75)
            name = self.image.name.split('.')[0]
            output.seek(0)
            self.image = InMemoryUploadedFile(output, 'ImageField', "%s" % name, 'image/jpeg', output.len, None)
        super(Contact, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.surname)
