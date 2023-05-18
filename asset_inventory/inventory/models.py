from django.db import models


class User(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=40)
    username = models.CharField(max_length=20, blank=True, unique=True)
    department = models.CharField(max_length=50, blank=True)
    office = models.IntegerField(blank=True)


class Asset(models.Model):

    def __str__(self):
        return self.designation

    # when a user is deleted with assets on their name, the assets get moved to stock
    user = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    barcode = models.CharField(max_length=10, unique=True)
    serial_no = models.CharField(max_length=20, blank=True, null=True, unique=True)
    designation = models.CharField(max_length=20)
    other = models.CharField(max_length=50, blank=True)
