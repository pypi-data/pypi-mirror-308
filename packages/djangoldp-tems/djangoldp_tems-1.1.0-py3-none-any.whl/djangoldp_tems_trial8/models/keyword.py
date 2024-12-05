from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_named_model import baseTEMSNamedModel


class Trial8Keyword(baseTEMSNamedModel):
    class Meta(baseTEMSNamedModel.Meta):
        container_path = "/objects/keywords/trial8/"
        verbose_name = _("TEMS Keyword")
        verbose_name_plural = _("TEMS Keywords")
        rdf_type = "tems:Keyword"
