## Installation

**django-slack-tools** supports Python 3.8+ and Django 3.2+. Supports for each deps will be dropped as soon as the ends of security updates.

Install the package:

```bash
$ pip install django-slack-tools
```

Add the app to the your Django settings:

```python
INSTALLED_APPS = [
    ...
    "django.contrib.messages", # Used in admin
    "django_slack_tools.slack_messages",
    ...
]
```

Add configuration for application:

```python
DJANGO_SLACK_TOOLS = {
    # Module path to Slack Bolt application or callable returns the app
    "SLACK_APP": "path.to.your.slack.app",

    # Messaging backend configuration
    "BACKEND": {
        "NAME": "django_slack_tools.slack_messages.backends.SlackBackend",
        "OPTIONS": {
            "slack_app": "path.to.your.slack.app",
        }
    }
}
```

Then, run the database migration (`python manage.py migrate`) and send messages:

```python
from django_slack_tools.slack_messages.message import slack_message

message = slack_message(
    "I like threading",
    channel="id-of-channel",
    header={"reply_broadcast": True},
)
```

Check [examples](https://github.com/lasuillard/django-slack-tools/tree/main/examples) for about more detailed usage examples.
