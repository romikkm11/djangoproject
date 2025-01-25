from django.contrib import admin
from .models import Articles
from .models import Company

admin.site.register(Articles)
admin.site.register(Company)
