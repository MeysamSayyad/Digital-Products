from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Package(models.Model):
    title = models.CharField(_("title"), max_length=50)
    sku = models.CharField(
        _("stock keeping unit"), max_length=20, validators=[], db_index=True
    )
    description = models.TextField(_("description"))
