from django.urls import path

from .views import PostView, PostListView

urlpatterns = [
    path('', PostView.as_view()),
    path('/<int:post_id>', PostView.as_view()),
    path('/list', PostListView.as_view())
    ]