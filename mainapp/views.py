import json
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from api.producer_user_created import ProducerUserCreated
from api.serializers import TaskSerializer
from api.models import Task
from django.contrib.auth.models import User
from .helpers import activity_feed
from .models import ActivityFeed

# Create your views here.
class IndexView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            all_task = Task.objects.filter(user=request.user)
            return render(request, 'dashboard.html', context={'tasks':all_task})
        return redirect("login")        

class LoginView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        return redirect("home")   
        
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    user = user
            except User.DoesNotExist:
                user = None
            if user is not None:
                login(request=request, user=user)
                print("You are logged in successfully.")
                messages.success(request, "You are logged in successfully." )
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials." )
                return redirect("login")
        else:
            messages.error(request, "Invalid credentials." )
            return redirect("login")
        
class RegisterView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'signup.html')
        return redirect("home")        
        
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, "Registration successful. You can login now." )
            ProducerUserCreated().publish("user_created_method", json.dumps(serializer.data))
            return redirect("login")
        messages.error(request, "Please fill form correctly.")
        return render(request, 'signup.html')
    
class AddTaskView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'addtask.html')
        return redirect("login")   
    def post(self, request):
        my_data = request.data.copy()
        my_data["user"] = request.user.pk
        serializer = TaskSerializer(data=my_data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Task Added successful." )
            activity_feed(serializer.data, "CREATE")
            return redirect("home")
        messages.error(request, "Task with this name already exists.")
        return redirect("add_task")

class MyActivityView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            activities = ActivityFeed.objects.filter(user=request.user).order_by('-created_at')[:10]
            return render(request, 'activity.html', context={"activities":activities})
        return redirect("login")   

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have successfully logged out.") 

    return redirect("login")

class LogoutView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.info(request, "You have successfully logged out.")
            return redirect("login")