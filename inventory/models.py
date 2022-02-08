from django.db import models
from django.forms import ModelForm


class User(models.Model):

    def __str__(self):
        return self.nev

    nev = models.CharField(max_length=40)
    felhasznalo_nev = models.CharField(max_length=20, blank=True, unique=True)
    szervezeti_egyseg = models.CharField(max_length=50, blank=True)
    szoba_szam = models.IntegerField(blank=True)


class Asset(models.Model):

    def __str__(self):
        return self.megnevezes + ' ' + self.gep_szam + ' ' + self.vonalkod

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vonalkod = models.CharField(max_length=10, unique=True)
    gyari_szam = models.CharField(max_length=20, blank=True, null=True, unique=True)
    gep_szam = models.CharField(max_length=10, blank=True, null=True, unique=True)
    megnevezes = models.CharField(max_length=20)
    egyeb = models.CharField(max_length=50, blank=True)
