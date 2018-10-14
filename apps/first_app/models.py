# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import re
import bcrypt

class UserManager(models.Manager):
	def sign_up_validator(self, postData):
		errors = {}
		if len(postData['username']) < 2:
			errors["username"] = "user name should be at least 2 characters"
		elif not re.match('[A-Za-z]+', postData['username']):
			errors['username'] = "user name may only contain letters."
		if len(postData['username']) < 2:
			errors["username"] = "user name should be at least 2 characters"
		elif not re.match('[A-Za-z]+', postData['username']):
			errors['username'] = "user name may only contain letters."
		if len(postData['password']) < 1:
			errors['email'] = "Please enter your email."
		elif User.objects.filter(email=postData['email']):
			errors['email'] = "Email is already taken."
		elif not re.match('[A-Za-z0-9-_]+(.[A-Za-z0-9-_]+)*@[A-Za-z0-9-]+(.[A-Za-z0-9]+)*(.[A-Za-z]{2,})',postData['email']):
			errors['email'] = "Incorrect Email Format."
		if len(postData['password']) < 4:
			errors['password']= "Password must be longer than 4 characters"
		elif postData['pw_confirm'] != postData['password'] :
			errors['password']= "Password is not match"
		return errors
	def log_in_validator(self, postData):
		errors = {}
		if len(postData['username']) < 1:
			errors['username'] = "Please Enter Your username"
		elif not User.objects.filter(username = postData['username']):
			errors['username_not_found'] = "Your username and password does not match."
		if len(postData['password']) < 1:
			errors['password'] = "Please enter your password"
		elif not bcrypt.checkpw(postData['password'].encode(), User.objects.get(username=postData['username']).password.encode()):
			errors['password'] = "Please enter the correct email or password."
		return errors

class ReviewManager(models.Manager):
	def review_validator(self, postData):
		errors = {}
		if len(postData['content']) < 5:
			errors['content'] = "Please write a review longer than 5 characters."
		if postData['rating'] < 1 :
			errors['rating'] = "You cannot rate a book below one."
		# if postData['rating'] > 5:
		# 	errors['rating'] = "You cannot rate a book above five"
		return errors

class AuthorManager(models.Manager):
	def author_validator(self, postData):
		errors = {}
		if len(postData['author']) < 1:
			errors['author'] = "You must enter an author name."
		return errors

class BookManager(models.Manager):
	def book_validator(self, postData):
		errors = {}
		if len(postData['title']) < 1:
			errors['title'] = "You must enter a proper title."
		return errors

class User(models.Model):
	username = models.CharField(max_length = 36 , unique = True)
	email = models.CharField(max_length = 100, unique = True)
	password = models.CharField(max_length = 36)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Author(models.Model):
	name = models.TextField(max_length = 50, unique = True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = AuthorManager()

class Book(models.Model):
	title = models.TextField(max_length = 50, unique = True)
	author = models.ForeignKey(Author, related_name="books")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = BookManager()

class Review(models.Model):
	content = models.TextField(max_length = 500)
	rating = models.IntegerField()
	user = models.ForeignKey(User, related_name = "reviews")
	book = models.ForeignKey(Book, related_name = "reviews")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = ReviewManager()

