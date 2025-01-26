from django.contrib import admin
from .models import Articles
from .models import Company, ServiceType, Service, Price

admin.site.register(Articles)
admin.site.register(Company)
admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Price)
