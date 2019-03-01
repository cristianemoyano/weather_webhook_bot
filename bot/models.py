from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    '''
        An abstract base class model that provides self updating
        ``created`` and ``modified`` fields.
    '''
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class SocialAccount(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField()
    social = models.CharField(max_length=250, blank=True, null=True)


class SocialPages(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    category = models.CharField(max_length=250, blank=True, null=True)
    page_name = models.CharField(max_length=250, blank=True, null=True)
    page_id = models.CharField(max_length=250, blank=True, null=True)
    page_tasks = models.TextField()
    default = models.BooleanField(default=False)

    def __str__(self):
        return '%s -  %s' % (self.page_name, self.category)
