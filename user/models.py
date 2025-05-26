from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):  # 🔥 로그인 필드가 email이므로 여기 맞춰야 함
        return self.get(email=email)

class User(AbstractBaseUser, PermissionsMixin):  # 🔥 관리자 권한 위한 믹스인 추가
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    user_id = models.CharField(max_length=30, blank=True, null=True)
    thumbnail = models.CharField(max_length=256, default='default_profile.jpg', blank=True, null=True)

    is_staff = models.BooleanField(default=False)      # 관리자 페이지 접근 여부
    is_active = models.BooleanField(default=True)      # 계정 활성화 여부
    is_superuser = models.BooleanField(default=False)  # 모든 권한 여부

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'           # 🔥 이메일을 로그인 필드로 설정
    REQUIRED_FIELDS = ['name']         # createsuperuser 시 받을 추가 필드

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'

class UserPreference(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='preference')
    genres = models.JSONField(default=list)
    goals = models.JSONField(default=list)
    reading_time = models.CharField(max_length=50, blank=True)
    reading_duration = models.CharField(max_length=50, blank=True)
    reading_complexity = models.CharField(max_length=50, blank=True)
    favorite_books = models.JSONField(default=list)
    mood = models.JSONField(default=list)
    onboarding_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)