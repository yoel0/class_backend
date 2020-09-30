from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import viewsets, status
from .serializers import UserSerializer, UsersSerializer, TeacherSerializer, StudentSerializer, ClassroomSerializer, ClassroomsSerializer
from .models import User, Teacher, Student, Classroom
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from django.http import JsonResponse
from rest_framework import mixins, generics

# Create your views here.

class TeacherRecordView(APIView):

    # A class based view for creating and fetching teacher records

    def get(self, format=None):

        # Get all the teacher records
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request):

        # Create a teacher

        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

class StudentRecordView(APIView):

    # A class based view for creating and fetching student records

    def get(self, format=None):

        # Get all the teacher records
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):

        # Create a teacher

        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

class UserRecordView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        if not user:
            return JsonResponse({'status': 0, 'message': 'User with this id not found'})
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UsersSerializer(user, data=request.data)
        if serializer.is_valid():

            email = request.data.get("email", None)
            first_name = request.data.get('first_name', None)
            last_name = request.data.get('last_name', None)
            username = request.data.get('username', None)
            password = request.data.get('password', None)

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.password = password
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class UsersRecordView(APIView):

    # A class based view for creating and fetching teacher records

    def get(self, format=None):
        # Get all the teacher records
        users = User.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        # Create a teacher
        serializer = UsersSerializer(data=request.data)
        # print(serializer)
        if serializer.is_valid(raise_exception=ValueError):
            # print(serializer)
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

class ClassroomRecordView(APIView):

    def get_object(self, pk):
        try:
            return Classroom.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk, format=None):
        classroom = self.get_object(pk)
        if not classroom:
            return JsonResponse({'status': 0, 'message': 'Classroom with this id not found'})
        serializer = ClassroomSerializer(classroom)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, pk, format=None):
        classroom = self.get_object(pk)
        serializer = ClassroomsSerializer(classroom, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserDefault():
    # """
    # May be applied as a `default=...` value on a serializer field.
    # Returns the current user.
    # """
    requires_context = True

    def __call__(self, serializer_field):
        print(serializer_field.context['request'].user)
        return serializer_field.context['request'].user

            
class ClassroomsRecordView(APIView):

    def get_queryset(self):
        user = User.objects.all()
        return user

    def get_object(self, pk):
        teacher = Teacher.objects.get(pk=pk)
        return teacher

    def get(self, format=None):
        print('🥁')
        # Get all the teacher records
        classrooms = Classroom.objects.all()
        serializer = ClassroomsSerializer(classrooms, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user_id = self.request.user.id
        teacher = self.get_object(pk=user_id)
        print(self.request.user.id, "Blah")
        print(request.data)
        request.data['teacher'] = teacher
        # Create a classroom
        # request.data['teacher'] = self.request.user
        print("We have made it")
        print(request)
        serializer = ClassroomsSerializer(data=request.data)
        # print(serializer)
        if serializer.is_valid(raise_exception=ValueError):
            # print(serializer)
            serializer.create(validated_data=request.data)
            print(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)