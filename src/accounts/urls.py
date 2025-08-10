from django.urls import path
from .views import ( UserCreateAPIView, UserListAPIView, UserRetrieveUpdateDestroyAPIView,LogoutAPIView)

urlpatterns = [
    path('create/',UserCreateAPIView.as_view(),name='user-create'),
    path('',UserListAPIView.as_view(), name='user-list'),
    path('<int:pk>/',UserRetrieveUpdateDestroyAPIView.as_view(),name='user-detail'),
    path('logout/',LogoutAPIView.as_view(),name='user-logout')
]