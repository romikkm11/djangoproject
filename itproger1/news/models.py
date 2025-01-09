from django.db import models

class Articles(models.Model):
    title = models.CharField('Назва', max_length=50)
    anons = models.CharField('Анонс', max_length=250)
    full_text = models.TextField('Стаття')
    date = models.DateTimeField('Дата публікації')

    def __str__(self):
        return self.title  
    
    def get_absolute_url(self):
        return f'/news/{self.id}'
    
    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини!!!'
        
class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва")
    latitude = models.FloatField(verbose_name="Широта")
    longititude = models.FloatField(verbose_name="Довгота")

    def __str__(self):
        return self.name