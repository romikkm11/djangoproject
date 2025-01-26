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
        
class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва")
    latitude = models.FloatField(verbose_name="Широта", null = True, blank = True)
    longititude = models.FloatField(verbose_name="Довгота", null = True, blank = True)

    def __str__(self):
        return self.name

class ServiceType(models.Model):
    name = models.CharField(max_length=200, verbose_name='Тип послуги')

    def __str__(self):
        return self.name
    
class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name='Послуга')
    type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Price(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.price