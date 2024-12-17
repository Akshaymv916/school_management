from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views  

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('add-users/', views.ManageUsers.as_view(), name='manage_users'),
    path('delete-users/<int:pk>/', views.ManageUsers.as_view(), name='manage_users'),
    path('students/', views.ManageStudents.as_view(), name='manage_students'),
    path('students/<int:pk>/', views.ManageStudents.as_view(), name='manage_student_detail'),
    path('library/', views.ManageLibrary.as_view(), name='manage_library'),
    path('library/<int:pk>/', views.ManageLibrary.as_view(), name='manage_library_details'),
    path('fees/', views.ManageFees.as_view(), name='manage_fees'),
    path('fees/<int:pk>/', views.ManageFees.as_view(), name='manage_fees_details'),

]
