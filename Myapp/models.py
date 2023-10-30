from django.db import models
from django.urls import reverse
import datetime
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericRelation
from autoslug import AutoSlugField
from django_countries.fields import CountryField


from django.db.models import Avg

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=20)
    

    def __str__(self) -> str:
        return str(self.name)

class Category(models.Model):

    choice = models.CharField(max_length = 15)
    slug = models.SlugField(max_length=200, unique=True)
    def __str__(self):
        return str(self.choice)
    def get_absolut_url(self):
        return reverse('Myapp:category_filter', args={self.slug})
    

class Product(models.Model):
    class StatusChoices(models.TextChoices):
        Available = "Available"
        SoldOut = "SoldOut"
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25) 
    image = models.ImageField(upload_to='products/') 
    description = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from = 'name', unique=True)
    price = models.FloatField()
    choice = models.ForeignKey(Category,on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=StatusChoices.choices)
    quantity = models.PositiveIntegerField(default=1)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.name)
    
    def get_absolut_url(self):
        return reverse('Myapp:product_detail', args={self.slug, })
    

class History(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    price = models.FloatField()
    category = models.CharField(max_length=20) 
    date_sold = models.DateField(auto_now=True)
    

class Feedback(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE )
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    # slug = AutoSlugField(populate_from = 'product.name', unique=True)
    chat_with_seller  = models.TextField(max_length=500)
    date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.username} + {self.chat_with_seller}'


class Reply(models.Model):
    sender= models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    # slug = AutoSlugField(populate_from = 'product.name', unique=True)
    reply  = models.TextField(max_length=500)
    date = models.DateField(auto_now=True)
    timer = models.TimeField(auto_now=True)



class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=11)
    subject = models.CharField(max_length=30)
    comment = models.CharField(max_length=1000)


    def __str__(self) -> str:
        return f'{self.name}'
    

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar =  models.ImageField(upload_to='profilePic/photos')
    phone = models.CharField(max_length=11)
    bio = models.CharField(max_length=1000)
    store_name = models.CharField(max_length=25)
    state = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    country = CountryField()

    def __str__(self) -> str:
        return f'{self.username}'
    

class Notification(models.Model):
    class StatusChoices(models.TextChoices):
        Read = "Read"
        Unread = "Unread"
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=25)
    notify = models.CharField(max_length=100)
    ids = models.IntegerField()
    isread = models.CharField(max_length=10, choices=StatusChoices.choices, default="Unread")
    
    def __str__(self) -> str:
        return f'notification for {self.username}'
    

class Alert(models.Model):
    class StatusChoices(models.TextChoices):
        Read = "Read"
        Unread = "Unread"
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=25)
    notify = models.CharField(max_length=100)
    ids = models.IntegerField()
    isread = models.CharField(max_length=10, choices=StatusChoices.choices, default="Unread")
    
    def __str__(self) -> str:
        return f'notification for {self.username}'