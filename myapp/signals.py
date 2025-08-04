from django.core.mail import send_mail


def custom_send_mail(email, code):
    subject = "チャットアプリ二段階認証"
    message = "二段階認証"
    message += f"\n認証コード  {code}"
    from_email = "test@test.co.jp"
    if subject and message:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[email],
        )
