from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.core.exceptions import ImproperlyConfigured
from slack_bolt import App

from django_slack_tools.app_settings import AppSettings
from django_slack_tools.slack_messages.backends import BaseBackend

if TYPE_CHECKING:
    from pytest_django.fixtures import SettingsWrapper

    from django_slack_tools.app_settings import ConfigDict


# Config fixtures to run in parametrize (map of test id to config dictionary)
config_fixtures: dict[str, ConfigDict] = {
    "dummy backend": {
        "SLACK_APP": "tests.test_app_settings.get_slack_app",
        "BACKEND": {
            "NAME": "django_slack_tools.slack_messages.backends.DummyBackend",
            "OPTIONS": {},
        },
    },
    "logging backend": {
        "SLACK_APP": "tests.test_app_settings.get_slack_app",
        "BACKEND": {
            "NAME": "django_slack_tools.slack_messages.backends.LoggingBackend",
            "OPTIONS": {},
        },
    },
    "slack backend": {
        "SLACK_APP": "tests.test_app_settings.get_slack_app",
        "BACKEND": {
            "NAME": "django_slack_tools.slack_messages.backends.SlackBackend",
            "OPTIONS": {
                "slack_app": "tests.test_app_settings.get_slack_app",
            },
        },
    },
    "slack redirect backend": {
        "SLACK_APP": "tests.test_app_settings.get_slack_app",
        "BACKEND": {
            "NAME": "django_slack_tools.slack_messages.backends.SlackRedirectBackend",
            "OPTIONS": {
                "slack_app": "tests.test_app_settings.get_slack_app",
                "redirect_channel": "some-redirect-channel",
            },
        },
    },
}

# Save decorator for reuse, as not all test in suite requires this
settings_dict_parametrizer = pytest.mark.parametrize(
    argnames="settings_dict",
    argvalues=config_fixtures.values(),
    ids=config_fixtures.keys(),
)


class TestAppSettings:
    def _assert_app_settings(self, app_settings: AppSettings) -> None:
        assert issubclass(app_settings.backend.__class__, BaseBackend)

    @settings_dict_parametrizer
    def test_dict_config(self, settings_dict: ConfigDict) -> None:
        app_settings = AppSettings(settings_dict)
        self._assert_app_settings(app_settings)

    @settings_dict_parametrizer
    def test_django_config(self, settings: SettingsWrapper, settings_dict: ConfigDict) -> None:
        settings.DJANGO_SLACK_TOOLS = None
        with pytest.raises(ImproperlyConfigured, match=r"^Neither `.+` provided or `.+` settings found"):
            AppSettings()

        settings.DJANGO_SLACK_TOOLS = settings_dict
        app_settings = AppSettings()
        self._assert_app_settings(app_settings)

    def test_raises_if_backend_is_not_subclass_of_base_class(self) -> None:
        with pytest.raises(
            ImproperlyConfigured,
            match="Provided backend is not a subclass of `django_slack_tools.slack_messages.backends.base.BaseBackend` class.",  # noqa: E501
        ):
            AppSettings(
                {
                    "SLACK_APP": "tests.test_app_settings.get_slack_app",
                    "BACKEND": {"NAME": "tests.test_app_settings.ImproperBackend", "OPTIONS": {}},
                },
            )

    def test_bad_config_not_slack_app(self) -> None:
        def not_slack_app() -> str:
            return "I'm not a slack app"

        with pytest.raises(ImproperlyConfigured, match="Couldn't resolve provided app spec into Slack app instance."):
            AppSettings(
                {
                    "SLACK_APP": "tests.test_app_settings.get_slack_app",
                    "BACKEND": {
                        "NAME": "django_slack_tools.slack_messages.backends.SlackBackend",
                        "OPTIONS": {
                            "slack_app": not_slack_app,
                        },
                    },
                },
            )

        with pytest.raises(ImproperlyConfigured, match="Provided `SLACK_APP` config is not Slack app."):
            AppSettings(
                {
                    "SLACK_APP": not_slack_app,  # type: ignore[typeddict-item]
                    "BACKEND": {
                        "NAME": "django_slack_tools.slack_messages.backends.SlackBackend",
                        "OPTIONS": {
                            "slack_app": "tests.test_app_settings.get_slack_app",
                        },
                    },
                },
            )


def get_slack_app() -> App:
    return App(token="i-am-a-cookie", token_verification_enabled=False)  # noqa: S106


class ImproperBackend:
    pass
