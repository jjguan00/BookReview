# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

# Create your views here.
from .models import User, Author, Book, Review
from django.contrib import messages
import bcrypt

def index(request):
	return render(request, "index.html")

def signups(request):
	if request.method == "POST":
		errors = User.objects.sign_up_validator(request.POST)
		if len(errors):
			for tag,value in errors.iteritems():
				messages.error(request, value,extra_tags=tag)
				print(tag,value)
			return redirect('/')
		else:
			hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			User.objects.create(username = request.POST['username'],  email = request.POST['email'], password= hash1)
			print("Created User.")
			return redirect('/')
	else:
		return redirect("/")
	return redirect('/')

def logins(request):
	if request.method == "POST":
		errors = User.objects.log_in_validator(request.POST)
		if len(errors):
			for tag, value in errors.iteritems():
				messages.error(request, value, extra_tags = tag)
				print(tag, value)
			return redirect('/')
		else:
			user = User.objects.get(username = request.POST['username'])
			request.session['user'] = user.id
			return redirect('/main')
	else:
		return redirect('/')

def main(request):
	if request.session['user']:
		user = User.objects.get(id = request.session['user'])
		reviews = Review.objects.filter(user = user).order_by("-created_at")
		books = Book.objects.all().order_by("-created_at")
		context = {
			'user' : user,
			'reviews': reviews,
			'books':books
		}
		return render(request, "main.html", context)
	else:
		return redirect("/")

def addReview(request):
	if request.session['user']:
		user = User.objects.get(id = request.session['user'])
		authors = Author.objects.all().order_by("-created_at")
		context = {
			'user': user,
			'authors': authors
		}
		return render(request, "add.html", context)
	else:
		return redirect("/")

def addReviews(request):
	if request.session['user']:
		errors = Author.objects.author_validator(request.POST)
		errors.update(Book.objects.book_validator(request.POST))
		errors.update(Review.objects.review_validator(request.POST))
		print(errors)
		if len(errors):
			for tag,value in errors.iteritems():
				messages.error(request, value,extra_tags=tag)
				print(tag,value)
			return redirect('/addReview')
		else:
			try:
				author = Author.objects.get(name = request.POST['author'])
			except:
				author = Author.objects.create(name = request.POST['author'])
			# if not Author.objects.get(name = request.POST['author']):
			# 	author = Author.objects.create(name = request.POST['author'])
			# else:
			# 	author = Author.objects.get(name = request.POST['author'])
			try:
			    book = Book.objects.get(title = request.POST['title'] )
			except:
			    book = Book.objects.create(title = request.POST['title'], author = author)
			# if Book.objects.get(title = request.POST['title']) is None:
			# 	book = Book.objects.create(title = request.POST['title'], author = author)
			# else:
			# 	book = Book.objects.get(title = request.POST['title'] )
			user = User.objects.get(id = request.session['user'])
			review = Review.objects.create(content = request.POST['content'], rating = request.POST['rating'], book= book, user=user)
			print("Successfully created reviews and books.")
			return redirect("/books/"+ str(book.id))
	else:
		return redirect("/")

def addReviewByBook(request, number):
	if request.session['user']:
		errors = Review.objects.review_validator(request.POST)
		if len(errors):
			for tag,value in errors.iteritems():
				messages.error(request, value,extra_tags=tag)
				print(tag,value)
			return redirect('/books/'+ number)
		else:
			user = User.objects.get(id = request.session['user'])
			book = Book.objects.get(id = number)
			review = Review.objects.create(content = request.POST['content'], rating = request.POST['rating'], book= book, user=user)
			print("Successfully created reviews and books.")
			return redirect("/books/"+ str(book.id))

	else:
		return redirect("/")

def books(request, number):
	if request.session['user']:
		book = Book.objects.get(id = number)
		reviews = Review.objects.filter(book = book).order_by("-created_at")
		context = {
			'book': book,
			'reviews': reviews
		}
		return render(request, "book.html", context)
	else:
		return redirect("/")

def users(request, number):
	if request.session['user']:
		user = User.objects.get(id = number)
		reviews = Review.objects.filter(user = user).order_by("-created_at")
		context = {
			'user': user,
			'reviews': reviews
		}
		return render(request, "user.html", context)
	else:
		return redirect("/")

def logOut(request):
	request.session['user'] = None
	return redirect("/")
