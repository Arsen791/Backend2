
from django.contrib import admin
from django.urls import path, include
from den.views import  asu, create_problem, view_problems, user_action, user_poblem_details
urlpatterns = [
	path('', create_problem),
	path('problems/', view_problems),
	path('problems/details_problems/<int:pk>/', user_poblem_details , name='user_poblem_details'),
	path('problems/details_problems/<int:pk>/user_action-create/', user_action, name='user_action'),
	path('ad/', asu),

]