from django.contrib import admin
from api import models

# Register your models here.
class customer(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'digits', 'inviter', 'contact_by', 'discount')
class contact(admin.ModelAdmin):
    list_display = ('app', 'app_id')

class prudoct(admin.ModelAdmin):
    list_display = ('time', 'user_id', 'name', 'digits', 'inviter_id', 'price', 'discount', 'gift_d', 'use')

admin.site.register(models.customer, customer)
admin.site.register(models.product, prudoct)
admin.site.register(models.contact, contact)


