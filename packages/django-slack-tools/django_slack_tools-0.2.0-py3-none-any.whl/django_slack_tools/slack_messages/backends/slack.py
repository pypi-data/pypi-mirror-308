"""Slack backends actually interact with Slack API to do something."""

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any, Callable

from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from slack_bolt import App
from slack_sdk.errors import SlackApiError

from .base import BaseBackend

if TYPE_CHECKING:
    from slack_sdk.web import SlackResponse

    from django_slack_tools.slack_messages.models import SlackMessage
    from django_slack_tools.utils.slack import MessageBody


logger = getLogger(__name__)


class SlackBackend(BaseBackend):
    """Backend actually sending the messages."""

    def __init__(
        self,
        *,
        slack_app: App | Callable[[], App] | str,
    ) -> None:
        """Initialize backend.

        Args:
            slack_app: Slack app instance or import string.
        """
        if isinstance(slack_app, str):
            slack_app = import_string(slack_app)

        if callable(slack_app):
            slack_app = slack_app()

        if not isinstance(slack_app, App):
            msg = "Couldn't resolve provided app spec into Slack app instance."
            raise ImproperlyConfigured(msg)

        self._slack_app = slack_app

    def _send_message(self, message: SlackMessage) -> SlackResponse:
        header = message.header or {}
        body = message.body or {}
        return self._slack_app.client.chat_postMessage(channel=message.channel, **header, **body)

    def _get_permalink(self, *, message: SlackMessage, raise_exception: bool = False) -> str:
        """Get a permalink for given message identifier."""
        if not message.ts:
            msg = "Message timestamp is not set, can't retrieve permalink."
            raise ValueError(msg)

        try:
            _permalink_resp = self._slack_app.client.chat_getPermalink(
                channel=message.channel,
                message_ts=message.ts,
            )
        except SlackApiError:
            if raise_exception:
                raise

            logger.exception(
                "Error occurred while sending retrieving message's permalink,"
                " but ignored as `raise_exception` not set.",
            )
            return ""

        return _permalink_resp.get("permalink", default="")

    def _record_request(self, response: SlackResponse) -> dict[str, Any]:
        # Remove auth header (token) from request before recording
        response.req_args.get("headers", {}).pop("Authorization", None)

        return response.req_args

    def _record_response(self, response: SlackResponse) -> dict[str, Any]:
        return {
            "http_verb": response.http_verb,
            "api_url": response.api_url,
            "status_code": response.status_code,
            "headers": response.headers,
            "data": response.data,
        }


class SlackRedirectBackend(SlackBackend):
    """Inherited Slack backend with redirection to specific channels."""

    def __init__(self, *, slack_app: App | str, redirect_channel: str, inform_redirect: bool = True) -> None:
        """Initialize backend.

        Args:
            slack_app: Slack app instance or import string.
            redirect_channel: Slack channel to redirect.
            inform_redirect: Whether to append an attachment informing that the message has been redirected.
                Defaults to `True`.
        """
        self.redirect_channel = redirect_channel
        self.inform_redirect = inform_redirect

        super().__init__(slack_app=slack_app)

    def prepare_message(self, *args: Any, channel: str, body: MessageBody, **kwargs: Any) -> SlackMessage:
        """Prepare message to send, with modified for redirection.

        Args:
            args: Positional arguments to pass to super method.
            channel: Original channel to send message.
            body: Message content.
            kwargs: Keyword arguments to pass to super method.

        Returns:
            Prepared message instance.
        """
        # Modify channel to force messages always sent to specific channel
        # Add an attachment that informing message has been redirected
        if self.inform_redirect:
            body.attachments = [
                self._make_inform_attachment(original_channel=channel),
                *(body.attachments or []),
            ]

        return super().prepare_message(*args, channel=self.redirect_channel, body=body, **kwargs)

    def _make_inform_attachment(self, *, original_channel: str) -> dict[str, Any]:
        msg_redirect_inform = _(
            ":warning:  This message was originally sent to channel *{channel}* but redirected here.",
        )

        return {
            "color": "#eb4034",
            "text": msg_redirect_inform.format(channel=original_channel),
        }
