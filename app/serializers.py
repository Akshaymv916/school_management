from rest_framework import serializers
from .models import FeeHistory, Student, User,LibraryHistory

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'class_name']

class UserSerializer(serializers.ModelSerializer):
    student = StudentSerializer(required=False)  

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'password', 'date_joined', 'student']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extract student data if available
        student_data = validated_data.pop('student', None)

        # Create user instance
        user = User.objects.create_user(**validated_data)

        # If user is a student, associate a student record
        if user.user_type == 'student' and student_data:
            Student.objects.create(user=user, **student_data)

        return user

    

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryHistory
        fields = '__all__'

class FeeHistorySerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source="student.username") 

    class Meta:
        model = FeeHistory
        fields = [
            "id", "student", "student_name", "fee_type", "amount",
            "payment_date", "remarks",  "created_at", "updated_at"
        ]
        read_only_fields = [ "created_at", "updated_at"]
