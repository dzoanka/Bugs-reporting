from django.urls import path
from . import views

urlpatterns = [
    path('', views.BugListView.as_view(), name='bugs'),
    path('<str:project>', views.BugListView.as_view(), name='bugs'),
    path('bugs/', views.BugListView.as_view(), name='bugs'),
    path('bugs/<str:project>/', views.BugListView.as_view(), name='bugs'),
    path('bug/<int:pk>/', views.BugDetailView.as_view(), name='bug-detail'),
    path('bug/<int:pk>/<str:project>/', views.BugDetailView.as_view(), name='bug-detail'),
    path('bug/create/', views.BugCreate.as_view(), name='bug-create'),
    path('bug/create/<str:project>/', views.BugCreate.as_view(), name='bug-create'),
    path('bug/<str:uuid>/update/', views.BugUpdate.as_view(), name='bug-update'),
    path('bug/<str:uuid>/<str:project>/update/', views.BugUpdate.as_view(), name='bug-update'),
    path('bug/track/', views.track_ticket, name='bug-track-ticket'),
    path('bug/track/<str:project>/', views.track_ticket, name='bug-track-ticket'),
]
