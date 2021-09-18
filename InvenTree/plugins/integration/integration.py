# -*- coding: utf-8 -*-

import logging

from django.conf.urls import url, include
from django.conf import settings
import plugins.plugin as plugin


logger = logging.getLogger("inventree")


class SettingsMixin:
    """Mixin that enables settings for the plugin"""
    def __init__(self):
        super().__init__()

        self.add_mixin('settings', 'has_settings')
        self.settings = self.setup_settings()

    def setup_settings(self):
        """
        setup settings for this plugin
        """
        return getattr(self, 'SETTINGS', None)

    @property
    def has_settings(self):
        """
        does this plugin use custom settings
        """
        return bool(self.settings)

    @property
    def settingspatterns(self):
        if self.has_settings:
            return {f'PLUGIN_{self.plugin_name().upper()}_{key}': value for key, value in self.settings.items()}
        return None


class UrlsMixin:
    """Mixin that enables urls for the plugin"""
    def __init__(self):
        super().__init__()

        self.add_mixin('urls', 'has_urls')
        self.urls = self.setup_urls()

    def setup_urls(self):
        """
        setup url endpoints for this plugin
        """
        return getattr(self, 'URLS', None)

    @property
    def base_url(self):
        return f'{settings.PLUGIN_URL}/{self.plugin_name()}/'

    @property
    def urlpatterns(self):
        """
        retruns the urlpatterns for this plugin
        """
        if self.has_urls:
            return url(f'^{self.plugin_name()}/', include(self.urls), name=self.plugin_name())
        return None

    @property
    def has_urls(self):
        """
        does this plugin use custom urls
        """
        return bool(self.urls)


class IntegrationPlugin(plugin.InvenTreePlugin):
    """
    The IntegrationPlugin class is used to integrate with 3rd party software
    """

    def __init__(self):
        self.add_mixin('base')
        super().__init__()

    def add_mixin(self, key: str, fnc_enabled=True):
        if not hasattr(self, 'mixins'):
            self.mixins = {}
        self.mixins[key] = fnc_enabled

    def module(self, key):
        return key in self.mixins

    def module_enabled(self, key):
        if self.module(key):
            fnc_name = self.mixins.get(key)
            return getattr(self, fnc_name, True)
        return False
