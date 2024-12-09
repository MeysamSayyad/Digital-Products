from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from utils.validators import validate_phone_number


class Gateway(models.Model):
    title = models.CharField(_("title"), max_length=50)
    avatar = models.ImageField(_("avatar"), blank=True, upload_to="packages/")
    is_enable = models.BooleanField(_("is enable"), default=True)
    description = models.TextField(_("description"), blank=True)

    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(
        _("updated time"),
        auto_now=True,
    )

    class Meta:
        db_table = "gateway"
        verbose_name = _("Gateway")
        verbose_name_plural = _("Gateways")


class Payment(models.Model):
    STATUS_VOID = 0
    STATUS_PAID = 10
    STATUS_ERROR = 20
    STATUS_CANCELED = 30
    STATUS_REFUNDED = 31
    STATUS_CHOICES = (
        (STATUS_VOID, _("void")),
        (STATUS_ERROR, _("error")),
        (STATUS_PAID, _("paid")),
        (STATUS_REFUNDED, _("refunded")),
        (STATUS_CANCELED, _("canceled")),
    )
    user = models.ForeignKey(
        "users.User",
        verbose_name=_("user"),
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )
    package = models.ForeignKey(
        "subscriptions.Package", related_name="%(class)s", on_delete=models.CASCADE
    )
    gateway = models.ForeignKey(
        Gateway,
        related_name="%(class)s",
        verbose_name=_("gateway"),
        on_delete=models.CASCADE,
    )
    price = models.PositiveIntegerField(_("price"), default=0)
    status = models.PositiveIntegerField(
        _("status"), choices=STATUS_CHOICES, default=STATUS_VOID
    )
    token = models.CharField(_("token"), max_length=50)
    device_uuid = models.CharField(_("device uuid"), max_length=40, blank=True)
    phone_number = models.BigIntegerField(
        _("phone number"), validators=[validate_phone_number]
    )
    consumed_code = models.PositiveIntegerField(
        _("consumed refrence code"), null=True, db_index=True
    )
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(
        _("updated time"),
        auto_now=True,
    )

    class Meta:
        db_table = "payment"
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
