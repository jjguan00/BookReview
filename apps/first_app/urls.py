from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$', views.index),
	url(r'^signups$', views.signups),
	url(r'^logins$', views.logins),
	url(r'^main$', views.main),
	url(r'^addReview$', views.addReview),
	url(r'^logOut$', views.logOut),
	url(r'^addReviews$', views.addReviews),
	url(r'^books/(?P<number>\d+)$', views.books),
	url(r'^users/(?P<number>\d+)$', views.users),
	url(r'^addReviewByBook/(?P<number>\d+)$', views.addReviewByBook)
]