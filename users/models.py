import random

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    send_mail,
)
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, username, phone_number, email, password, **extra_fields):
        return self._create_user(
            username, phone_number, email, password, True, True, **extra_fields
        )

    def _create_user(
        self,
        username,
        phone_number,
        email,
        password,
        is_staff,
        is_superuser,
        **extra_fields
    ):
        now = timezone.now()
        if not username:
            raise ValueError("The giver username must be set")
        email = self.normalize_email(email)

        user = self.model(
            phone_number=phone_number,
            username=username,
            is_staff=is_staff,
            email=email,
            is_active=True,
            is_superuser=is_superuser,
            date_joined=now,
            **extra_fields
        )
        if not extra_fields.get("no_password"):
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        username=None,
        phone_number=None,
        email=None,
        password=None,
        is_staff=False,
        is_superuser=False,
        **extra_fields
    ):

        if username is None:
            if email:
                username = email.split("@", 1)[0]
            if phone_number:
                username = (
                    random.choice("abcdefghijklmnopqrstuzwxyz") + str(phone_number)[-7:]
                )

            while User.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))

            return self._create_user(
                username,
                phone_number,
                email,
                password,
                is_staff,
                is_superuser,
                **extra_fields
            )


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _("username"),
        max_length=32,
        unique=True,
        help_text="Required. 30 characters or fewer starting with a letter",
        validators=[
            validators.RegexValidator(
                r"^[a-zA-Z][a-zA-Z0-9_\.]+$",
                _("Enter a valid username starting with a-z"),
            ),
        ],
        error_messages={"unique": _("A user with that username already exists")},
    )
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    email = models.EmailField(
        _("email address"), max_length=254, unique=True, null=True, blank=True
    )
    phone_number = models.BigIntegerField(
        _("mobile number"),
        unique=True,
        null=True,
        blank=True,
        validators=[
            validators.RegexValidator(
                r"^989[0-3,9]\d{8}$",
                _("Enter a valid number"),
            ),
        ],
        error_messages={"unique": _("A user with that phone already exists")},
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user is admin or not"),
    )
    is_active = models.BooleanField(
        _("active"), default=True, help_text=_("Designates whether the user is active")
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_seen = models.DateTimeField(_("last seen date"), null=True)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone_number"]

    @property
    def is_loggenin_user(self):
        return self.phone_number is not None or self.email is None

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == "":
            self.email = None
        super().save(*args, **kwargs)

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(_("nick_name"), max_length=150, blank=True)
    avatar = models.ImageField(_("avatar"), blank=True)
    birthday = models.DateField(_("birthday"), null=True, blank=True)
    gender = models.BooleanField(
        _("gender"),
        null=True,
        blank=True,
        help_text=_("female is False male is True,null is unset"),
    )
    province = models.ForeignKey(
        verbose_name=_("province"), to="Province", null=True, on_delete=models.SET_NULL
    )

    class Meta:
        db_table = "user_profiles"
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")


class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICE_TYPE_CHOICES = ((WEB, "web"), (IOS, "ios"), (ANDROID, "android"))
    user = models.ForeignKey(User, related_name="devices", on_delete=models.CASCADE)
    device_uuid = models.UUIDField(_("Device UUID"), null=True)
    last_login = models.DateTimeField(_("last login date"), null=True)
    device_type = models.PositiveSmallIntegerField(
        _("device type"), choices=DEVICE_TYPE_CHOICES, default=WEB
    )
    device_os = models.CharField(_("device os"), max_length=20, blank=True)
    device_model = models.CharField(_("device model"), max_length=50, blank=True)
    app_version = models.CharField(_("app version"), max_length=20, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user devices"
        verbose_name = _("device")
        verbose_name_plural = _("devices")
        unique_together = ("user", "device_uuid")


class Province(models.Model):
    name = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    modifed_at = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
