from django.contrib import admin
from .models import (CarModel,CarMake)


# Register your models here.
# admin.site.register(CarModel)
# admin.site.register(CarMake)
# CarModelInline class
class CarModelInline(admin.TabularInline):
    model=[CarModel,CarMake]
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['delerid', 'name']
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name', 'description']

# Register models here
admin.site.register(CarModel,CarModelAdmin)
admin.site.register(CarMake,CarMakeAdmin)