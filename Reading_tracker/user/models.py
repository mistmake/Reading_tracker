from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from book.models import Book


class Reader(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email adress'), unique=True)
    password = models.CharField(max_length=40)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    books = models.ManyToManyField(Book, through='ReadingList')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class ReadingList(models.Model):
    reader_id = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True)
    finish_date = models.DateTimeField(null=True)
    overall_reading_time = models.FloatField(null=True)
    reread = models.BooleanField(default=False)

