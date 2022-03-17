from flask import current_app
from flask_mail import Message


class EmailService:
    @staticmethod
    async def send_async(subject: str, content: str, **recipients):
        """
        Sending message in asynchronous mode.
        """

        message = Message(
            subject=subject,
            html=content,
            recipients=[*recipients],
        )

        from src import mail
        await mail.send(message)
