import functools
import inspect
import logging
from time import time


default_logger = logging.getLogger("default-logger")


def log_decorator(log_msg: str = "", log_level: int = logging.INFO, logger: logging.Logger = default_logger):
    """
    Adds console logs before and after the method execution.

    :param log_msg: The message to be printed out.
    :param log_level: Log level used for the console log.
    :param logger: logging.Logger object. By default, it will use "default-logger".
    :return:
    """
    def inner(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if log_level == logging.DEBUG:
                log = logger.debug
            elif log_level == logging.WARNING:
                log = logger.warning
            elif log_level == logging.ERROR:
                log = logger.error
            elif log_level == logging.CRITICAL:
                log = logger.critical
            else:
                log = logger.info

            log("%s...", log_msg)
            result = func(*args, **kwargs)
            log("%s...OK", log_msg)
            return result
        return wrapper
    return inner


def ntfy(
    url: str = "http://ntfy.george-sandbox.es",
    topic: str = "zimmer",
    username: str = "reportal",
    password: str = "reportal",
    ok_msg: str = "OK",
    nok_msg: str = "NOK",
    notify_if_ok: bool = True,
    notify_if_nok: bool = True,
):
    """Run the script and send a message once it finishes.

    I set up a tool in a private server that is accessible to all in
    http://ntfy.george-sandbox.es

    If you use a browser like Firefox, Chrome,... it won't send you updates
    because that functionality requires HTTPS, BUT if you install the NTFY app
    in your PC or smartphone and start listening to the `zimmer` topic the tool
    will notify you whenever a new message is sent.

    So, if this script fails, it will send the exception to the `zimmer` topic.
    If it doesn't fail, it will send a message to let you know the reports are ready.

    I chose `zimmer` as the topic because that's the server supposedly running this script.

    You can read more about this tool in https://ntfy.sh

    :param url: NTFY server. Defaults to my custom server http://ntfy.george-sandbox.es
    :param topic: NTFY topic. Defaults to zimmer.
    :param ok_msg: what to print in case the script finishes without error.
    :param nok_msg: what to print in case the script finishes with error.
    :param notify_if_ok: whether to send a message if function did not raise an error
    :param notify_if_nok: whether to send a message if function raised an error
    """

    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import os
            import requests
            import traceback as tb

            script_name = os.path.abspath(inspect.getfile(func))
            session = requests.Session()

            req = requests.Request(
                method="POST",
                url=(url.replace("://", f"://{username}:{password}@").removesuffix("/") + "/" + topic),
                headers={
                    "Title": f"`{script_name}:{func.__name__}`",
                },
            )

            msg = f"\n- *args: {args}\n- **kwargs: {kwargs}\n---\n"
            is_ok = False
            total_time_secs = None
            result = None

            try:
                start = time()
                result = func(*args, **kwargs)
                end = time()
                total_time_secs = end - start
                is_ok = True
            finally:
                if not is_ok and notify_if_nok:
                    exception_msg = tb.format_exc()
                    if "KeyboardInterrupt" in exception_msg:
                        req.headers["Tags"] = "orange_circle,no_mouth"
                    else:
                        # only add nok_msg when not intentionally interrupted
                        if nok_msg:
                            msg += f"{nok_msg}\n"

                        req.headers["Tags"] = "red_circle,rotating_light"
                        req.headers["Priority"] = "5"

                    msg += f"Exception: {exception_msg}\n"

                    req.data = msg.encode()
                    session.send(req.prepare())

                if is_ok and notify_if_ok:
                    if ok_msg:
                        msg += f"{ok_msg}\n"

                    msg += f"- Time taken: {total_time_secs} seconds\n"
                    msg += f"- Result: {result}\n"

                    req.data = msg.encode()
                    req.headers["Tags"] = "green_circle,partying_face"
                    session.send(req.prepare())
            return result
        return wrapper
    return inner
