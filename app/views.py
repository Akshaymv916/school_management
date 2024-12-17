from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import  FeeHistory, LibraryHistory, Student, User
from rest_framework.exceptions import NotFound,PermissionDenied
from .serializers import FeeHistorySerializer, StudentSerializer, UserSerializer,LibrarySerializer
from rest_framework import status


class ManageUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication credentials were not provided'}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.user_type != 'admin':
            return Response({'error': 'only admin can get the details of users'}, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all()
        user_data = [
            {
                'id': user.id,
                'full_name': user.username,
                'email': user.email,
                'user_type': user.user_type
            }
            for user in users
        ]
        return Response({'users': user_data}, status=status.HTTP_200_OK)


    def post(self, request):
        if request.user.user_type != 'admin':
            return Response({'error': 'only admin can add users'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if request.user.user_type != 'admin':
            return Response({'error': 'only admin can edit users'}, status=status.HTTP_403_FORBIDDEN)
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.user_type != 'admin':
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        user = User.objects.get(pk=pk)

        confirm = request.query_params.get('confirm', 'false').lower()
        if confirm != 'true':
            return Response(
                {
                    'message': f'Are you sure you want to delete the user "{user.username}"?',
                    'confirm_url': f'{request.build_absolute_uri()}?confirm=true'
                },
                status=status.HTTP_200_OK
            )
        user.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ManageStudents(APIView):
    permission_classes = [IsAuthenticated]  
    
    def get(self, request, pk=None):
        if request.user.user_type not in ['office_staff', 'librarian', 'admin']:
            raise PermissionDenied("You do not have permission to view student details.")

        if pk:
            try:
                student = Student.objects.get(pk=pk)  
                serializer = StudentSerializer(student)  
                return Response(serializer.data, status=200)
            except Student.DoesNotExist:
                raise NotFound("Student not found.")
        else:
            students = Student.objects.all()  
            serializer = StudentSerializer(students, many=True) 
            return Response(serializer.data, status=200)
    
    def post(self, request):
        if request.user.user_type != 'admin':
            return Response({"detail": "Only admins can add student details."}, status=403)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        if request.user.user_type != 'admin':
            return Response({"detail": "Only admins can update student details."}, status=403)
        
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found")

        serializer = UserSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        if request.user.user_type != 'admin':
            return Response({"detail": "Only admins can delete student details."}, status=403)
        
        try:
            student = Student.objects.get(pk=pk)
            confirm = request.query_params.get('confirm', 'false').lower()
            if confirm != 'true':
                confirm_url = request.build_absolute_uri(reverse('manage_student_detail', kwargs={'pk': pk})) + '?confirm=true'
                return Response(
                {
                    'message': f'Are you sure you want to delete the student "{student.user.username}"?',
                    'confirm_url': confirm_url
                },
                status=status.HTTP_200_OK
            )
            user = student.user
            student.delete() 
            user.delete()  
            return Response({"detail": "Student deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found")
        




class ManageLibrary(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    
    def get(self, request, pk=None):
        if request.user.user_type not in ['student', 'office_staff', 'librarian', 'admin']:
            raise PermissionDenied("You do not have permission to view library records.")
        
        if pk:
            try:
                record = LibraryHistory.objects.get(pk=pk)
                if request.user.user_type == 'student' and record.student.user != request.user:
                    raise PermissionDenied("You can only view your own library records.")
                serializer = LibrarySerializer(record)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except LibraryHistory.DoesNotExist:
                raise NotFound("Library record not found.")
        else:
            if request.user.user_type == 'student':
                records = LibraryHistory.objects.filter(student__user=request.user)
            else:
                records = LibraryHistory.objects.all()
            serializer = LibrarySerializer(records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if request.user.user_type not in ['student', 'admin']:
            raise PermissionDenied("You do not have permission to add library records.")

        if request.user.user_type == 'student':
            try:
                student = Student.objects.get(user=request.user)
                request.data['student'] = student.id
            except Student.DoesNotExist:
                raise NotFound("Student profile not found for the current user.")
        
        serializer = LibrarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, pk=None):
        if request.user.user_type not in ['student', 'admin']:
            raise PermissionDenied("You do not have permission to edit library records.")

        try:
            record = LibraryHistory.objects.get(pk=pk)
        except LibraryHistory.DoesNotExist:
            raise NotFound("Library record not found.")

        if request.user.user_type == 'student' and record.student.user != request.user:
            raise PermissionDenied("You can only edit your own library records.")

        serializer = LibrarySerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        if request.user.user_type not in ['student', 'admin']:
            raise PermissionDenied("You do not have permission to delete library records.")

        try:
            record = LibraryHistory.objects.get(pk=pk)
            confirm = request.query_params.get('confirm', 'false').lower()

            if confirm != 'true':
                confirm_url = request.build_absolute_uri(reverse('manage_library_details', kwargs={'pk': pk})) + '?confirm=true'
                return Response(
                    {
                        'message': f'Are you sure you want to delete the library record for "{record.book_name}"?',
                        'confirm_url': confirm_url
                    },
                    status=status.HTTP_200_OK
                )

            if request.user.user_type == 'student' and record.student.user != request.user:
                raise PermissionDenied("You can only delete your own library records.")

            record.delete()

            return Response({"detail": "Library record deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except LibraryHistory.DoesNotExist:
            raise NotFound("Library record not found.")
    



class ManageFees(APIView):
    permission_classes = [IsAuthenticated]  
    
    def get(self, request, pk=None):
        if request.user.user_type not in ['student', 'office_staff',  'admin']:
            raise PermissionDenied("You do not have permission to view fee records.")
        
        if pk:
            try:
                record = FeeHistory.objects.get(pk=pk)
                if request.user.user_type == 'student' and record.student.user != request.user:
                    raise PermissionDenied("You can only view your own fees records.")
                serializer = FeeHistorySerializer(record)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except FeeHistory.DoesNotExist:
                raise NotFound("fee record not found.")
        else:
            if request.user.user_type == 'student':
                records = FeeHistory.objects.filter(student__user=request.user)
            else:
                records = FeeHistory.objects.all()
            serializer = FeeHistorySerializer(records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if request.user.user_type not in ['student', 'office_staff',  'admin']:
            raise PermissionDenied("You do not have permission to add fee records.")

        if request.user.user_type == 'student':
            try:
                student = Student.objects.get(user=request.user)
                request.data['student'] = student.id
            except Student.DoesNotExist:
                raise NotFound("Student profile not found for the current user.")
        
        serializer = FeeHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, pk=None):
        if request.user.user_type not in ['student', 'office_staff',  'admin']:
            raise PermissionDenied("You do not have permission to edit fee records.")

        try:
            record = FeeHistory.objects.get(pk=pk)
        except FeeHistory.DoesNotExist:
            raise NotFound("fee record not found.")

        if request.user.user_type == 'student' and record.student.user != request.user:
            raise PermissionDenied("You can only edit your own fee records.")

        serializer = FeeHistorySerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        if request.user.user_type not in ['student', 'office_staff', 'admin']:
            raise PermissionDenied("You do not have permission to delete fee records.")

        try:
            record = FeeHistory.objects.get(pk=pk)
            confirm = request.query_params.get('confirm', 'false').lower()

            if confirm != 'true':
                confirm_url = request.build_absolute_uri(reverse('manage_fees_details', kwargs={'pk': pk})) + '?confirm=true'
                return Response(
                    {
                        'message': f'Are you sure you want to delete the fee record for student "{record.student.user.username}"?',
                        'confirm_url': confirm_url
                    },
                    status=status.HTTP_200_OK
                )

            if request.user.user_type == 'student' and record.student.user != request.user:
                raise PermissionDenied("You can only delete your own fee records.")

            record.delete()

            return Response({"detail": "Fee record deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except FeeHistory.DoesNotExist:
            raise NotFound("Fee record not found.")
        
