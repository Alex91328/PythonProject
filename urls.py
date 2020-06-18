from django.urls import path 
from . import views
urlpatterns = [
    path('', views.index),
    path('users/create', views.create),
    path('users/login', views.login),
    path('quotes', views.quotes),
    path('logout', views.logout),
    path('myaccount/<int:user_id>', views.edit),
    path('post_message', views.post_message),
    path('account/<int:user_id>/update', views.update),
    path('user/<int:author_id>', views.user),
    path('message/<int:author_id>/delete', views.delete),
    ]
    #path('post_comment/<int:message_id>', views.post_comment), 
