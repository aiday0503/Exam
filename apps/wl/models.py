from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime, timedelta


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile("^[^0-9]+$")
PASSWORD_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if postData['name'] == '':
            errors['name'] = 'Name can not be blank.'
        else:
            if not NAME_REGEX.match(postData['name']):
                errors['name'] = 'Please input valid name. No numbers.'

        if postData['alias'] == '':
            errors['alias'] = 'Alias can not be blank.'
        else:
            if len(self.filter(alias=postData['alias'])) > 0:
                    errors['alias'] = 'Alias already in use.'

        if postData['email'] == '':
            errors['email'] = 'Email can not be blank.'
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = 'Please input valid email.'
            else:
                if len(self.filter(email=postData['email'])) > 0:
                    errors['email'] = 'email already in use.'

        if postData['password'] == '':
            errors['password'] = 'Password can not be blank.'
        else:
            if len(postData['password']) < 2:
                errors['password'] = 'Password can not be less than 8 characters.'
            else:
                # if not PASSWORD_REGEX.match(postData['password']):
                #     errors['password'] = 'Please input valid password.'
                if postData['password'] != postData['cpassword']:
                    errors['password'] = 'Password does not match.'

        if len(errors) == 0:
            hashpw = bcrypt.hashpw(
                postData['password'].encode(), bcrypt.gensalt())
            user = self.create(name=postData['name'], alias=postData['alias'],
                               email=postData['email'], password=hashpw)
            return (True, user)

        return (False, errors)
        # return dictionary

    def login_validator(self, postData):
        errors = {}

        try:
            user = self.get(email=postData['email'])
        except:
            errors['email'] = "Email and password input are invalid."


        if len(errors) == 0:
    
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = "Password input is invalid."
            else:
                return (True, user)
                
        return (False, errors)

class TravelManager(models.Manager):
    def travel_validator(self, postData, id):
        errors = {}

        #if postData['destination'] == '':
        #    errors['destination'] = 'Name can not be blank.'

        #if len(postData['destination']) < 3 :
        #    errors['destination'] = 'Name need to be longer than 3 characters.'
        test = 10
        if test == 10:
            uploader = User.objects.get(id=id)
            print postData
            travel = self.create(destination=postData['destination'],
            travelStart=postData['travelStart'],
            travelEnd=postData['travelStart'],
            plan=postData['description'],
             uploader=uploader)
            return (True, travel)
                
        return (False, {})

    def add_travel(self,id,travel_id):
        user = User.objects.get(id=id)
        travel = Travel.objects.get(id=travel_id)
        GroupTravel.objects.create(traveler = user,joiner = travel)

   

   
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    def __repr__(self):
        return "User: {}".format(self.name)

class Travel(models.Model):
    uploader = models.ForeignKey(User, related_name='uploaded_travel')
    destination = models.CharField(max_length=255)
    plan = models.CharField(max_length=255)
    travelStart = models.DateTimeField(auto_now_add=False)
    travelEnd = models.DateTimeField(auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = TravelManager()
    def __repr__(self):
        return "Travel: {}".format(self.name)

class GroupTravel(models.Model):
    traveler = models.ForeignKey(User, related_name='wished_travel')
    joiner = models.ForeignKey(Travel, related_name = 'on_list')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __repr__(self):
        return "GroupTravel: {}-{}".format(self.joiner.name, self.joiner.id )
