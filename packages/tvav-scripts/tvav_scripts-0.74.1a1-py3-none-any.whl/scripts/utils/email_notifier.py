import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage
from pathlib import Path
from typing import Optional


class EmailNotifier:
    """Aux class to handle email notifications.

    Use it to send email notifications with attachments whenever a script
    is finished.

    Use it to monitor the script by sending POLL emails to your `FROM` email
    address with the information you need to track its progress.

    Use it to be notified whenever an error that needs your attention
    has been raised.

    Bonus: when used as a context manager, 
    """
    def __init__(self) -> None:
        load_dotenv()
        self._subject = os.getenv("SUBJECT")
        self._from = os.getenv("FROM")
        self._to = os.getenv("TO")
        self._cc = os.getenv("CC")
        self._smtp_server = os.getenv("SMTP_SERVER") or "smtp.gmail.com"
        self._smtp_user = os.getenv("SMTP_USER")
        self._smtp_password = os.getenv("SMTP_PASSWORD")

        self._error = False
        self._poll = False

    def __enter__(self) -> "EmailNotifier":
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        error_message = f"{str(exc_type)}: {exc_value} - {traceback}"
        print(error_message)
        self.error(error_message)
        raise RuntimeError("An error was raised. Check your email for more info.")

    def _send_email_message(self, message: EmailMessage):
        with smtplib.SMTP(self._smtp_server) as s:
            s.starttls()
            if self._smtp_user and self._smtp_password:
                s.login(self._smtp_user, self._smtp_password)
            s.send_message(message)

        self._error = False
        self._poll = False

    def poll(self, message: Optional[str] = ""):
        """Use this method to send emails to the `FROM` email address.

        It is useful for devs to monitor scripts to ensure they are alive,
        without spamming the `TO` email address.

        Email subject will appear as `SUBJECT - POLL`
        """
        self._poll = True
        self.send(body=message)

    def error(self, error_message: Optional[str] = ""):
        """Use this method to send emails to the `FROM` email address.

        It is useful for devs to monitor scripts when the script has raised
        an error that needs to be attended.

        Email subject will appear as `SUBJECT - ERROR`
        """
        self._error = True
        self.send(body=error_message)

    def send(self, body: Optional[str] = "", attachment: Optional[Path] = None):
        subject = self._subject

        if self._error:
            subject = f"{subject} - ERROR"
        elif self._poll:
            subject = f"{subject} - POLL"

        message = EmailMessage()

        message.set_content(body)
        message["Subject"] = subject
        message["From"] = self._from
        message["To"] = (
            self._to
            if not (self._poll or self._error)
            else self._from
        )

        if self._cc and not (self._error or self._poll):
            message["CC"] = self._cc

        if attachment:
            with attachment.open(mode="rb") as f:
                message.add_attachment(
                    f.read(),
                    subtype=os.path.splitext(attachment.absolute()),
                    filename=attachment.name,
                )
        self._send_email_message(message)
