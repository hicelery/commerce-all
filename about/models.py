
from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
type = [
    ('bug report', 'Bug Report'),
    ('collaboration', 'Collaboration Request'),
    ('general', 'General Inquiry'),

]


class AboutPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    type = models.CharField(max_length=50, choices=type, default='general')
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Contact request from {self.name}"
