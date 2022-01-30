import email
from http import client
import imp
from time import time
from django.test import TestCase
from .models import Client, Barber, Skills, User, Visit

class ModelsTests(TestCase):
    def setUp(self):
        Client.objects.create(username = "clientTest", email = "clientTest@wp.pl", staff = False)
        Barber.objects.create(username = "barberTest", email = "barberTest@wp.pl", staff = True)
        Skills.objects.create(skills_name = "wlosyTest")
        User.objects.create(username = "userTest", email = "userTest@wp.pl", staff = False)

    def testDeleteUser(self):
        user = User.objects.filter(username = "userTest").first()
        user.delete()

    def testDeleteClient(self):
        client = Client.objects.filter(username = "clientTest").first()
        client.delete()

    def testDeleteBarber(self):
        barber = Barber.objects.filter(username = "barberTest").first()
        barber.delete()

    def testSkillSetToBarber(self):
        barber = Barber.objects.filter(username = "barberTest").first()
        skill = Skills.objects.filter(skills_name = "wlosyTest").first()
        barber.skills.add(skill.id)
        self.assertEqual(barber.skills.values().first()["skills_name"], skill.skills_name)

    def testDelteSkill(self):
        skill = Skills.objects.filter(skills_name = "wlosyTest")
        skill.delete()

    def testCreateVisit(self):
        clientTest = Client.objects.filter(username = "clientTest").first()
        skill = Skills.objects.filter(skills_name = "wlosyTest").first()
        Visit.objects.create(client = clientTest, skills = skill, date = "2022-02-02", time = "13:00")

    def testDeleteVisit(self):
        clientTest = Client.objects.filter(username = "clientTest").first()
        skill = Skills.objects.filter(skills_name = "wlosyTest").first()
        visit = Visit.objects.create(client = clientTest, skills = skill, date = "2022-02-02", time = "13:00")
        visit.delete()

    

    

    
        
    

    


