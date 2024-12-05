from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model

from djangoldp_tems.models.__base_model import baseTEMSModel
from djangoldp_tems.models.images import TEMSImages
from djangoldp_tems.models.licence import TEMSLicence
from djangoldp_tems.models.provider import TEMSProvider


class baseTEMSObject(baseTEMSModel):
    title = models.CharField(max_length=254, blank=True, null=True, default="")
    description = models.TextField(blank=True, null=True, default="")
    copyright = models.CharField(max_length=254, blank=True, null=True, default="")
    website = models.CharField(max_length=2000, blank=True, null=True, default="")
    licences = models.ManyToManyField(TEMSLicence, blank=True)
    images = models.ManyToManyField(TEMSImages, blank=True)
    providers = models.ManyToManyField(TEMSProvider, blank=True)

    class Meta(Model.Meta):
        abstract = True
        serializer_fields = [
            "@id",
            "creation_date",
            "update_date",
            "title",
            "description",
            "copyright",
            "website",
            "licences",
            "images",
            "providers",
        ]
        nested_fields = [
            "licences",
            "images",
            "providers",
        ]
        rdf_type = "tems:Object"
