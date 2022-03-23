from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)



class AllCodes(models.Model):
    category = models.ManyToManyField(Category)


class Codes(models.Model):
    all = models.ForeignKey(AllCodes, on_delete=models.CASCADE, related_name='all_codes')
    

