import json
import logging
import requests
from pydantic import Field, BaseSettings
from dotenv import load_dotenv
from requests import Response


SLACK_POST_MESSAGE_API = "https://slack.com/api/chat.postMessage"


class SlackNotifierConfig(BaseSettings):
    token: str = Field(None, env="slack_token")
    channel_id: str = Field(None, env="slack_channel_id")


class SlackNotifier:
    def __init__(self) -> None:
        self.config: SlackNotifierConfig = SlackNotifierConfig()  # type: ignore

    def is_ready(self):
        return self.config.token and self.config.channel_id

    def send_message(self, msg: str) -> Response:
        if not self.is_ready():
            raise ValueError("Slack token and channel id missing")

        return requests.post(
            url=SLACK_POST_MESSAGE_API,
            headers={
                "Content-type": "application/json",
                "Authorization": f"Bearer {self.config.token}"
            },
            data=json.dumps({
                "channel": self.config.channel_id,
                "text": msg,
            })
        )


class SlackHandler(logging.Handler):
    """
    Custom Slack logging handler.
    Sends a Slack message for each log message to the specified channel via SlackNotifierConfig.

    Requires SlackNotifierConfig to be set.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slack_notifier = SlackNotifier()

    def emit(self, record):
        log_entry = self.format(record)

        try:
            response = self.slack_notifier.send_message(log_entry)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to send log message to Slack: {e}")


class ClassWithSlackLogger:
    """
    Base class that provides 2 attributes for Slack logging:
    - logger: a dynamic logging.Logger with 2 Handlers for stream and Slack chat logging if Slack credentials are provided.
    - tqdm: a dynamic tqdm to log to a Slack chat if Slack credentials are provided.
    """
    def __init__(self):
        """Init logger with SlackHandler if available"""
        load_dotenv()
        # Console logger
        stream_handler = logging.StreamHandler()
        handlers = [stream_handler, ]

        # Slack logger (requires setting the slack credentials in the env, check utils/slack_notifier.py)
        slack_handler = SlackHandler()
        if slack_handler.slack_notifier.is_ready():
            handlers.append(slack_handler)  # type: ignore
            print("Using slack logger!")

        logging.basicConfig(
            level=logging.INFO,
            format="[%(levelname)s] %(asctime)s | %(name)s |  %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            handlers=handlers,
        )
        self.logger = logging.getLogger(self.__class__.__name__)

        # Mute all loggers except the self.logger
        logging.getLogger().setLevel(logging.CRITICAL + 10)
        self.logger.setLevel(logging.INFO)

        # Init tqdm
        try:
            from tqdm import tqdm
            from tqdm.contrib.slack import tqdm as slack_tqdm
        except ImportError:
            print("Please, install tqdm to use Slack tqdm")
        else:
            self.tqdm = (
                lambda *args, **kwargs: slack_tqdm(
                    token=slack_handler.slack_notifier.config.token,
                    channel=slack_handler.slack_notifier.config.channel_id,  # type: ignore
                    *args,
                    **kwargs,
                )
            ) if slack_handler.slack_notifier.is_ready() else tqdm


if __name__ == "__main__":
    # This is to test the notifier and the handler
    import os

    SLACK_TOKEN = "xoxb-4605774589-4545908363351-3eSBVHocmLaP0MxsGHQqzTj6"
    SLACK_CHANNEL_ID = "C04G9QHK2EA"
    os.environ = {
        "SLACK_TOKEN": SLACK_TOKEN,
        "SLACK_CHANNEL_ID": SLACK_CHANNEL_ID,
    }

    # Simple Slack messages
    sn = SlackNotifier()
    res = sn.send_message("This is a simple slack message sent with SlackNotifier")

    # Slack as a log handler
    test = ClassWithSlackLogger()
    test.logger.info("Test using ClassWithSlackLogger")
