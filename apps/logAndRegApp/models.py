# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z0-9]\w+$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        users = self.filter(email=post_data['email'])
        if users:
            user = users[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')
        if errors:
            return errors
        return user 

    def validate_registration(self, post_data):
        errors = []
        # check all fields for emptyness
        if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2:
            errors.append("name fields must be at least 3 characters")
        # check name fields for letter characters            
        elif not re.match(NAME_REGEX, post_data['first_name']) or not re.match(NAME_REGEX, post_data['last_name']):
            errors.append('name fields must be letter characters only')

        # check length of name password
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")
         # check password == password_confirm
        elif post_data['password'] != post_data['confpassword']:
            errors.append("passwords do not match")

        # check emailness of email
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")
       
        if not errors:
            # check uniqueness of email
            if len(User.objects.filter(email=post_data['email'])) > 0:
                errors.append("email already in use")
            else:
                hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

                new_user = self.create(
                    first_name=post_data['first_name'],
                    last_name=post_data['last_name'],
                    email = post_data['email'],
                    password = hashed
                )
                return new_user
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()
    def __str__(self):
        return "<User: {}>".format(self.email)