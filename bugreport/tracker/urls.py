from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bugs/', views.BugListView.as_view(), name='bugs'),
    path('bugs/<str:project>/', views.displayBugsForProject, name='bugs-project'),
    path('bug/<int:pk>', views.BugDetailView.as_view(), name='bug-detail'),
]

urlpatterns += [
    path('bug/create/', views.BugCreate.as_view(), name='bug-create'),
    path('bug/<str:uuid>/update/', views.BugUpdate.as_view(), name='bug-update'),
    path('bug/<int:pk>/delete/', views.BugDelete.as_view(), name='bug-delete'),
    path('bug/track/', views.track_ticket, name='bug-track-ticket'),
    path('bug/create/<str:project>/', views.ProjectBugCreate.as_view(), name='bug-create-project'),
    path('bug/track/<str:project>/', views.track_ticket, name='bug-track-ticket-project'),
]

urlpatterns += [
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]
