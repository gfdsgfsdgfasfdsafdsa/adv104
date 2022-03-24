from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_categories')
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class AllCodes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_code_lists')
    category = models.ManyToManyField(Category, related_name='all_codes_categories')
    title = models.CharField(max_length=255)
    body = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Codes(models.Model):
    all = models.ForeignKey(AllCodes, on_delete=models.CASCADE, related_name='all_codes')
    title = models.CharField(max_length=255, blank=True, null=True)
    code = models.TextField()

    def __str__(self):
        return self.code

