from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('elections/', views.election_list, name='election_list'),
    path('elections/<int:election_id>/', views.election_list, name='election_list'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),  # Add this line
    path('create/', views.create_candidate_and_election, name='create_election'),
    path('', views.index, name='index'),
    path('vote/<int:election_id>/', views.vote, name='vote'),
    path('voting_success/', views.voting_success_view, name='voting_success'),
    path('check_candidate_name/', views.check_candidate_name, name='check_candidate_name'),
    path('election/<int:election_id>/results/', views.election_results, name='election_results'),
    path('close_election/<int:election_id>/', views.close_election, name='close_election'),
    path('election/<int:election_id>/delete/', views.delete_election, name='delete_election'),

]
