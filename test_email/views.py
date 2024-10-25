from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, EmailSerializer
from rest_framework import status
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
import os
from .utils import create_pdf
from .tasks import send_email

# Create your views here.

class UserView(APIView):
    def get(self,request, id):
        # user = User.objects.all()
        user = User.objects.filter(id=id).first()
        print(user.password,'------------------')
        serializer = UserSerializer(user)
        return Response(serializer.data)
    

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        email = request.data.get("email")
        password = request.data.get("password")
        if serializer.is_valid():
            pdf_file_path = create_pdf(password, email)
            print(pdf_file_path,'--------------------')
            serializer.save()
            subject = "Welcome! Your Protected PDF"
            body = "Hello! Please find the attached PDF. Use your registered password to open it."
            email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [email])
            email.attach_file(pdf_file_path)
            email.send(fail_silently=False)
            os.remove(pdf_file_path)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class SendingEmailView(APIView):
    def post(self,request):
        data = request.data
        lst = data.get("email_list",None)
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            for i in lst:
                pdf_file_path = create_pdf("test@123456", i)
                send_email.delay(pdf_file_path,i)
            return Response({'data':"Email has been sent"})
        else:
            return Response({'Error':serializer.errors})
