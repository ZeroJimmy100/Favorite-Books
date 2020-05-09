from django.db import models
from datetime import datetime, date
import re


class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(post_data["type_first_name"]) < 3:
            errors["first_name"] = 'First name should be at least 3 characters or more'
        if len(post_data["type_last_name"]) < 1:
            errors["last_name"] = 'Last name should be at least 1 characters or more'
        if not EMAIL_REGEX.match(post_data['type_email']):    # test whether a field matches the pattern      
            errors['email'] = "Invalid email address!"
        if len(post_data["type_email"]) < 10:
            errors["email"] = 'Email should be at least 10 characters or more'
        if len(post_data["type_password"]) < 5:
            errors["password"] = 'Password should be at least 5 characters or more'
        if post_data["type_confirm"] != post_data["type_password"]:
            errors["password"] = "Confirm password must match your password you've created"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #authors
