from django.db import models
class Categoria(models.Model):
    CategoriaNombre=models.CharField(max_length='100',verbose_name='Nombre de categoria')
    Portadacategoria=models.ImageField(upload_to='portada', null=True)
    def __unicode__(self):
    	return self.CategoriaNombre
    class Meta:
    	verbose_name_plural='Categoria de Productos'
        ordering=['CategoriaNombre']

class Producto(models.Model):
    NombreProduc=models.CharField(max_length='100',verbose_name='Nombre de Producto')
    Precio=models.FloatField(null= True)
    Portada=models.ImageField(upload_to='portada', null=True)
    Estado=models.BooleanField(default=True)
    RegistroCateg=models.ForeignKey(Categoria)

    def __unicode__(self):
    	return self.NombreProduc
    class Meta:
    	verbose_name_plural='Productos Registrados'
        ordering=['RegistroCateg']

class Stock(models.Model):
    fecha_ing = models.DateField(verbose_name='Fecha de Registro',auto_now_add=True)
    fecha_venc=models.DateField(verbose_name='Fecha de Vencimiento')
    cantidad= models.IntegerField(verbose_name='Cantidad de Producto')
    unidad=models.CharField(max_length='100', verbose_name='Unidad')
    reg_pro=models.ForeignKey(Producto, null=True, blank=True)
    def __unicode__(self):
        return self.fecha_venc
    class Meta:
        verbose_name_plural='stock  de producto'
        ordering=['fecha_ing']

