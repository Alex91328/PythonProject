from __future__ import unicode_literals 
from django.db import models
import string
# Create your models here.
import re
class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors= {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"

        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 Characters"
        
        if post_data['first_name'].isalpha() == False:
            errors['first_name'] = "First Name Field must use Letters"
        
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 Characters"
        
        if post_data['last_name'].isalpha() == False:
            errors['last_name'] = "Last Name Field must use Letters" 
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        
        
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 Characters"
        
        elif post_data['password']!= post_data['confirm_pw']:
            errors['password_cw'] = 'Password fields do not match' 
        return errors
        
    
    def login_validator(self, post_data):
        errors = {}
        user = User.objects.filter(email=post_data)
        if len(user) != 1:
            errors['email'] = 'No User with this email'
        return errors 
    
    def author_validator(self, post_data):
        errors={}
        author = Author.objects.filter(author=post_data)
        quote = Author.objects.filter(quote=post_data)
        if len(author) < 3:
            errors['author']="Authors names must have more than 3 Characters"
        if len(quote) < 10:
            errors['quote']="Quotes must have more than 10 Characters" 
        return errors
    
    def edit_account_validator(self, post_data):
        errors={}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters"

        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last Name must be filled with at least 2 characters"

        #if len(post_data['email']) < 0:
        #    errors['email'] = "Email must be filled"
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        return errors

    # def text_area(self, post_data):
    #     errors = {}
    #     message = Message.objects.filter(message_text=post_data)
    #     if len(message) !=1:
    #         errors['message_text'] = "No Characters in post"
    #     return errors
        
        #if not bcrypt.confirm_pw(post_data)['password'].encode(), user[0].password.encode()):
          #  errors['password'] = "Email and Password do not match"

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    confirm_pw = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 
    objects = UserManager()

class Message(models.Model):
    message_text = models.TextField()
    user = models.ForeignKey(User, related_name="user_messages", on_delete = models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

class Comment(models.Model):
    comment_text = models.TextField()
    message = models.ForeignKey(Message, related_name="message_comments", on_delete= models.CASCADE)
    user = models.ForeignKey(User, related_name="user_comments", on_delete = models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add = True)

class Author(models.Model):
    author = models.CharField(max_length = 255)
    user = models.ForeignKey(User, related_name="author_comments", on_delete = models.CASCADE)
    quote = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

