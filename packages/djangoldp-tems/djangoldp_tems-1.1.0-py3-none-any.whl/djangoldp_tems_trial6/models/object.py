from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_object import baseTEMSObject
from djangoldp_tems.models.provider import TEMSProvider, register_catalog

register_catalog("catalog_trial6")


class Trial6Object(baseTEMSObject):
    providers = models.ManyToManyField(
        TEMSProvider, blank=True, related_name="catalog_trial6"
    )
    subtitle = models.CharField(max_length=255, blank=True, null=True, default="")
    editor = models.CharField(max_length=255, blank=True, null=True, default="")
    contributors = models.TextField(blank=True, null=True, default="")
    author = models.CharField(max_length=254, blank=True, null=True, default="")
    platform = models.CharField(max_length=254, blank=True, null=True, default="")

    def __str__(self):
        return self.title or self.urlid

    class Meta(baseTEMSObject.Meta):
        container_path = "/objects/trial6/"
        verbose_name = _("TEMS Trial 6 Object")
        verbose_name_plural = _("TEMS Trial 6 Objects")

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
            "subtitle",
            "editor",
            "contributors",
            "author",
            "platform",
            "assets",
            "providers",
        ]
        nested_fields = [
            "licences",
            "assets",
            "images",
            "providers",
        ]
        rdf_type = ["tems:Object", "tems:ContentObject"]
