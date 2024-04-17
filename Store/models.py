from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TshirtProperty(models.Model):
    title = models.CharField(max_length=50, null=False, default='')
    slug = models.CharField(max_length=50, null=False, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Occasion(TshirtProperty):
    pass 

class IdealFor(TshirtProperty):
    pass

class NeckType(TshirtProperty):
    pass

class Brand(TshirtProperty):
    pass

class Color(TshirtProperty):
    pass

class Sleeve(TshirtProperty):
    pass

class Tshirt(models.Model):
    name =  models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500, null=True)
    discount = models.IntegerField(default=0)
    image = models.ImageField(upload_to='uploads/images', null=False)
    occasion = models.ForeignKey(Occasion, on_delete=models.CASCADE)
    ideal_for = models.ForeignKey(IdealFor, on_delete=models.CASCADE)
    neck_type = models.ForeignKey(NeckType, on_delete=models.CASCADE)
    sleeve = models.ForeignKey(Sleeve, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SizeVariant(models.Model):
    SIZES = (
        ("S","Small"),
        ("M","Medium"),
        ("L","Large"),
        ("XL","Extra Large"),
        ("XXL","Extra Extra Large")
    )
    price = models.FloatField(null=False)
    tshirt = models.ForeignKey(Tshirt, on_delete = models.CASCADE)
    size = models.CharField(max_length=5, choices=SIZES)

    def __str__(self):
        return f'{self.size}'

class Cart(models.Model):
    sizeVariant = models.ForeignKey(SizeVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    orderStatus = (
        ('PENDING','pending'),
        ('PLACED','placed'),
        ('CANCELED','canceled'),
        ('COMPLETED','completed')
    )
    method = (
        ('COD','cod'),
        ('ONLINE','online')
    )
    order_status = models.CharField(max_length=25, choices=orderStatus)
    payment_method = models.CharField(max_length=25, choices=method)
    shippping_address = models.CharField(max_length=100)
    phone = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    tshirt = models.ForeignKey(Tshirt, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=25,default='FAILED')
    payment_id = models.CharField(max_length=100)
    payment_request_id = models.CharField(max_length=100)
