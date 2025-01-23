from enum import _auto_null
from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank= True, on_delete=models.CASCADE)
    username= models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null= True)
    password = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField( default="profile1.png", null=True, blank= True)
    date_created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
     return self.username

class Organizations(models.Model):
   org_name = models.CharField(max_length=200, null= True)
   phone_number= models.CharField(max_length=200, null= True)
   org_email = models.CharField(max_length=200, null= True)
   org_about = models.CharField(max_length=200, null= True)
   org_password = models.CharField(max_length=200, null=True)
   date_created = models.DateTimeField(auto_now_add = True)
   
   def __str__(self):
      return self.org_name
  
class Posts(models.Model):
   org_id = models.CharField(max_length=50, primary_key= True)
   org_post = models.CharField(max_length= 200, null= True)
   media_url = models.CharField(max_length= 200, null= True, blank =True)
   date_created = models.DateTimeField(auto_now_add = True)
 
   organizations = models.ForeignKey(Organizations, null=True, on_delete= models.SET_NULL)

class Tag(models.Model):
      name = models.CharField(max_length=200, null= True)
      
      def __str__(self):
         return self.name

class Products(models.Model):
      CATEGORY =(
         ('Indoor', 'Indoor'),
         ('Out Door', 'Out Door'),
         )
      
      name = models.CharField(max_length = 200, null= True)
      price = models.CharField(max_length = 200, null= True)
      category= models.CharField(max_length = 200, null= True, choices = CATEGORY)
      description = models.CharField(max_length = 200, null= True, blank = True)
      date_created = models.DateTimeField(auto_now_add = True, null= True)
      tags = models.ManyToManyField(Tag)
      
      def __str__(self):
         return self.name

class Orders(models.Model):
   STATUS =(
      ('Pending', 'Pending'),
      ('Out for Delivery', 'Out for Delivery'),
      ('Delivered', 'Delivered')
      )
   customer = models.ForeignKey(Customer, null=True, on_delete = models.SET_NULL)
   product = models.ForeignKey(Products, null=True, on_delete = models.SET_NULL)
   
   date_created = models.DateTimeField(auto_now_add = True, null =True)
   status = models.CharField(max_length = 200, null= True, choices = STATUS)
   note = models.CharField(max_length = 1000, null= True)
   
   def __str__(self):
      return self.product.name