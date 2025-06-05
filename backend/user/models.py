from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,email,name,roll_number,department,programme,role, password=None):
        if not email:
            raise ValueError("Email required")
        
        user=self.model(
            email=email,
            name=name,
            roll_number=roll_number,
            department=department,
            programme=programme,
            role=role
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user
    def create_superuser(self, email, name, roll_number, department, programme, role,password):
        user = self.create_user(email, name, roll_number, department, programme, role,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, email):
        return self.get(email=email)




class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    backup_email = models.EmailField(blank=True, null=True)
    name= models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    programme=models.CharField(max_length=100)
    role= models.CharField(max_length=20, choices=[
        ('student', 'student'),
        ('spoc', 'spoc'),
        ('pr','pr'),
        ('admin', 'admin')
    ])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'roll_number', 'department', 'programme', 'role']

    objects = UserManager()

    def __str__(self):
        return f"{self.name} ({self.roll_number}) - {self.role}"
    