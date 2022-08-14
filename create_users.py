import os
import random
from venv import create
import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE","intern.settings.dev")
django.setup()

from myapp.models import CustomMessage, CustomUser

fakegen=Faker(["ja_JP"])

def create_users(n):
    users = [
        CustomUser(username=fakegen.user_name(),email=fakegen.ascii_safe_email())
        for _ in range(n)
    ]
    
    CustomUser.objects.bulk_create(users,ignore_conflicts=True)

    my_id = CustomUser.objects.get(username="admin").id

    user_ids = CustomUser.objects.exclude(id=my_id).values_list("id",flat=True)

    talks = []
    for _ in range(len(user_ids)):
        sent_talk = CustomMessage(
            sender=my_id,
            receiver=random.choice(user_ids),
            message=fakegen.text(),
        )
        received_talk=CustomMessage(
            sender=random.choice(user_ids),
            receiver=my_id,
            message=fakegen.text(),
        )
        talks.extend([sent_talk,received_talk])
    CustomMessage.objects.bulk_create(talks,ignore_conflicts=True)

if __name__ == "__main__":
    print("creating users ...",end="")
    create_users(5)
    print("done")
