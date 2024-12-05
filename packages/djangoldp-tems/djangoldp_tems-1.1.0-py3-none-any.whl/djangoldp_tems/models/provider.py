from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_model import baseTEMSModel
from djangoldp_tems.models.provider_category import TEMSProviderCategory


class TEMSProvider(baseTEMSModel):
    name = models.CharField(max_length=255, blank=True, null=True, default="")
    description = models.TextField(blank=True, null=True, default="")
    category = models.ForeignKey(
        TEMSProviderCategory, blank=True, null=True, on_delete=models.SET_NULL
    )

    @property
    def catalogs(self):
        """
        List of catalogs associated with a provider.

        The list is computed by inspecting the fields of the model that start
        with "catalog_".

        Each item of the list is a dictionary with two keys:

        - "container": the name of the field (e.g. "catalog_tems1")
        - "@type": the rdf_type of the model associated with the field

        :return: a list of dictionaries
        """
        return [
            {
                "container": field,
                "@type": getattr(self, field).model._meta.rdf_type,
            }
            for field in (
                f.name for f in self._meta.get_fields() if f.name.startswith("catalog_")
            )
        ]

    def __str__(self):
        return self.name or self.url or self.urlid

    class Meta(baseTEMSModel.Meta):
        container_path = "/providers/"
        verbose_name = _("TEMS Provider")
        verbose_name_plural = _("TEMS Providers")

        serializer_fields = [
            "@id",
            "creation_date",
            "update_date",
            "name",
            "description",
            "category",
            "catalogs",
        ]
        nested_fields = ["category"]
        rdf_type = "tems:Provider"


def register_catalog(catalog):
    """
    Registers a new catalog for the TEMSProvider model.

    :param str catalog: The name of the catalog field to register
    """
    TEMSProvider._meta.serializer_fields += [catalog]
    TEMSProvider._meta.nested_fields += [catalog]
