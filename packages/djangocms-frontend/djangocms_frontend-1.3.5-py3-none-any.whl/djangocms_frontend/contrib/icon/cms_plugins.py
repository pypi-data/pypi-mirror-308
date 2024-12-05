from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from ... import settings
from ...cms_plugins import CMSUIPlugin
from ...common.attributes import AttributesMixin
from ...common.background import BackgroundMixin
from ...common.responsive import ResponsiveMixin
from ...common.spacing import SpacingMixin
from .. import icon
from . import forms, models

mixin_factory = settings.get_renderer(icon)


class IconPlugin(
    mixin_factory("Icon"),
    AttributesMixin,
    ResponsiveMixin,
    SpacingMixin,
    BackgroundMixin,
    CMSUIPlugin,
):
    """
    Universal icon picker
    https://github.com/migliori/universal-icon-picker
    """

    name = _("Icon")
    module = _("Frontend")
    model = models.Icon
    form = forms.IconForm
    text_enabled = True
    text_icon = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" '
        'class="bi bi-emoji-sunglasses" viewBox="0 0 16 16"><path d="M4.968 9.75a.5.5 0 1 0-.866.5A4.5 4.5 '
        "0 0 0 8 12.5a4.5 4.5 0 0 0 3.898-2.25.5.5 0 1 0-.866-.5A3.5 3.5 0 0 1 8 11.5a3.5 3.5 0 0 1-3.032-1.75M7 "
        "5.116V5a1 1 0 0 0-1-1H3.28a1 1 0 0 0-.97 1.243l.311 1.242A2 2 0 0 0 4.561 8H5a2 2 0 0 0 1.994-1.839A3 "
        "3 0 0 1 8 6c.393 0 .74.064 1.006.161A2 2 0 0 0 11 8h.438a2 2 0 0 0 1.94-1.515l.311-1.242A1 1 0 0 0 "
        '12.72 4H10a1 1 0 0 0-1 1v.116A4.2 4.2 0 0 0 8 5c-.35 0-.69.04-1 .116"/><path d="M16 8A8 8 0 1 1 0 8a8 8 '
        '0 0 1 16 0m-1 0A7 7 0 1 0 1 8a7 7 0 0 0 14 0"/></svg>'
    )
    fieldsets = [
        (
            None,
            {
                "fields": (
                    (
                        "icon",
                        "icon_size",
                    ),
                    "icon_foreground",
                    "icon_rounded",
                )
            },
        ),
    ]


if "IconPlugin" in plugin_pool.plugins:
    #  Unregister already installed IconPlugin
    del plugin_pool.plugins["IconPlugin"]

plugin_pool.register_plugin(IconPlugin)
