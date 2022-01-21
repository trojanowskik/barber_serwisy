from re import A
from urllib import response
from django.shortcuts import render
from .serializers import BarberSerializer, ClientSerializer, LoginSerializer, RegistrationSerializer, UserSerializer, SkillSerializers, VisitSerializers
from rest_framework import viewsets
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Barber, Client,  Skills, Visit
from .backends import IsStaffForReadOnly, IsStaff, IsClient
from .tasks import send_email

def skill_id_to_name(skills):
    table = []
    for i in skills:
        table.append(i["skills_name"])
    return table
    
class BarberViewSet(viewsets.ModelViewSet):
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})

        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),

            'barber': {
                'skill': user_data.get('skill', request.barber.skills),
            }
        }

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        if request.user.staff:
            user = Barber.objects.filter(email = request.user.email).first()
            serializer = BarberSerializer(user)
        else:
            user = Client.objects.filter(email = request.user.email).first()
            serializer = ClientSerializer(user)
        skills = skill_id_to_name(user.skills.values())
        #serializer.data["skills"] = {}
        return Response((serializer.data, skills), status=status.HTTP_200_OK)

class MakeSkills(APIView):
    permission_classes = (IsAuthenticated, IsStaffForReadOnly)
    serializer_class = SkillSerializers

    def post(self, request):
        serializer = SkillSerializers(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        skills = Skills.objects.all()
        s = [SkillSerializers(skill).data for skill in skills]
        return Response(s)
    
    def delete(self, request):
        skill = Skills.objects.filter(skills_name = request.data["skills_name"])
        skill.delete()
        return Response({"message": "usunięto"})

class SetSkills(APIView):
    permission_classes = (IsAuthenticated, IsStaff)

    def post(self, request):
        skill = Skills.objects.get_or_create(skills_name = request.data["skills_name"])
        request.user.skills.add(skill[0])
        request.user.save()

        return  Response({"message": "dodano"})
    
    def delete(self, request):
        spec_name = request.data['skills_name']
        s = Skills.objects.filter(skills_name = spec_name).first()
        skill_list = request.user.skills.values()
        if not {"id":s.id, "skills_name":s.skills_name} in skill_list.values():
            response.data = {'message':  skill_list.values()} 
            return Response(response.data)
        request.user.skills.remove(s)
        request.user.save()
        response.data = {'message': 'Delete success'}
        return Response(response.data)

class SetVisit(APIView):
    permission_classes = (IsAuthenticated, IsClient)

    def post(self, request):
        request.data["client"] = request.user.id
        date = request.data["date"]
        time = request.data["time"]
        time = time + ":00.000"
        request.data["date"] = date + "T" + time
        visit = VisitSerializers(data = request.data)
        visit.is_valid(raise_exception = True)
        visit.save()
        send_email(request.user, visit.data)
        return Response(visit.data)

    def delete(self, request):
        id = request.data['id']
        visit = Visit.objects.filter(id = id).first()
        visit.delete()
        return Response({"message": "Wizyta usunięta"})

