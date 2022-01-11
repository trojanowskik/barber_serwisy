import jwt
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, email, type, password=None):
        user = None
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        if type == 'client':
            user = Client.objects.create(username=username, email=self.normalize_email(email))
        elif type == 'barber':
            user = Barber.objects.create(username=username, email=self.normalize_email(email), staff=True)

        if user:
            user.set_password(password)
            user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.staff = True
        user.save()

        return user

class User(AbstractUser):
    name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    phone_number = models.CharField(max_length=11, default='')
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    password = models.CharField(max_length=255)

    staff = models.BooleanField(default='False')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=30)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

class Skills(models.Model):
    skills_name = models.CharField(max_length=50, default='')

    class Meta:
        ordering = ['skills_name']

    def __str__(self):
        return self.skills_name

class Barber(User):
    skills = models.ManyToManyField(Skills)

class Client(User):
    pass