#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
class Perfil_user(models.Model):
    user = models.OneToOneField(User)
    nombre=models.CharField(max_length='100', verbose_name='Nombre')
    CI_NIT= models.IntegerField(verbose_name='CI/NIT',max_length='11')
    ap_paterno=models.CharField(max_length='100', verbose_name='Apellido Paterno')
    ap_materno=models.CharField(max_length='100', verbose_name='Apellido Materno')
    email=models.EmailField(verbose_name='E-mail')
    direcion=models.CharField(max_length='100',verbose_name='Dirección')
    user= models.ForeignKey(User,null=True, blank=True)
    def __unicode__(self):
        return self.user
    class Meta:
        verbose_name_plural= "perfil_user"