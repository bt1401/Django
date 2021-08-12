
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Title(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body_text = models.TextField()
    #image = models.ImageField(null=True, blank=True, upload_to="images/")
    date = models.DateTimeField()


    def __str__(self):
        return self.title +' | '+ str(self.author)

    def get_absolute_url(self):
        #return reverse("mysite:test-view", args=(str(self.id)))
        return reverse('mysite:admin-site')
    
