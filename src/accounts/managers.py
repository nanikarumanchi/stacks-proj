from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_details):
        if not email:
            raise ValueError('User must provide Email address')
        if not username:
            raise ValueError('User must provide User name')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        password = user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staff(self, email, name, password=None):
        user = self.create_user(email=email, username=name)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, username=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
