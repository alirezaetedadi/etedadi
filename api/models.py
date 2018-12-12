from django.db import models
# Create your models here.


class contact(models.Model):
    app = models.CharField(max_length=50)
    app_id = models.IntegerField(null=True)

    def __str__(self):
        return self.app


class customer(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    digits = models.CharField(max_length=13, unique=True, null=True)
    inviter = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_DEFAULT, default=1)
    contact_by = models.ForeignKey(contact, null=True, on_delete=models.SET_NULL)
    discount = models.CharField(max_length=10,default="0")
    def __str__(self):
        return self.name

class product(models.Model):
    time = models.DateTimeField()
    user_id = models.ForeignKey(customer, on_delete=models.CASCADE, related_name='buyer', null=True, blank=True)
    inviter_id = models.ForeignKey(customer, on_delete=models.SET_NULL,related_name='invit', null=True)
    price = models.CharField(max_length=9)
    discount = models.CharField(max_length=9, default=0)
    gift_d = models.BooleanField(default=False)
    use = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True)
    digits = models.CharField(max_length=13, null=True)

