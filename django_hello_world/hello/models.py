from django.db import models

# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    bio = models.TextField()
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=50)
    other_contacts = models.TextField(blank=True)

    def __unicode__(self):
        return "%s %s" % (self.name, self.last_name)
