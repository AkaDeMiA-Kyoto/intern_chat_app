import os
import random

import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE","myapp.settings.dev")
django.setup()

from myapp.models import Message, Signup

fakegen = Faker(["ja_JP"])

def create_users(n):
    users=[
        Signup(username=fakegen.user_name(),email=fakegen.ascii_safe_email())
        for _ in range(n)
    ]

    Signup.objects.bulk_create(users, ignore_conflicts=True)

    my_id = Signup.objects.get(username="ka-ryo-ta").id

    user_ids = Signup.objects.exclude(id=my_id).values_list("id",flat=True)

    messages = []
    for _ in range(len(user_ids)):
        sent_message = Message(
            sender_id=my_id,
            recipient_id=random.choice(user_ids),
            message=fakegen.text(),
        )
        received_message = Message(
            sender_id=random.choice(user_ids),
            recipient_id=my_id,
            message=fakegen.text(),
        )
        messages.extend([sent_message,received_message])
    Message.objects.bulk_create(messages,ignore_conflicts=True)

    messages = Message.objects.order_by("-sended_at")[:2*len(user_ids)]
    for message in messages:
        message.sended_at = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    Message.objects.bulk_update(messages,fields=["sended_at"])

if __name__=="__main__":
    print("creating users ...", end="")
    create_users(1000)
    print("done")