from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('office_staff', 'Office Staff'),
        ('librarian', 'Librarian'),
        ('student', 'Student'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPES)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)  # Optional, for students
    name = models.CharField(max_length=255,null=True, blank=True)
    roll_number = models.CharField(max_length=20,null=True, blank=True)
    class_name = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.roll_number}"
    

class LibraryHistory(models.Model):
    STATUS_CHOICES = (
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
    )

    student = models.ForeignKey(Student, related_name="library_history", on_delete=models.CASCADE)
    book_name = models.CharField(max_length=255)
    borrow_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')


    def __str__(self):
        return f"{self.book_name} - {self.student.name} - {self.status}"
    
class FeeHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fee_records")
    fee_type = models.CharField(max_length=100) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.fee_type} - {self.amount}"