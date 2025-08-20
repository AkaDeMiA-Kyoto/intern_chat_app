import os
import random

import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings")
django.setup()

from myapp.models import User, Talk

fakegen = Faker(["ja_JP"])

def create_users(n):
    users = [User(
        username=fakegen.user_name(),
        email=fakegen.ascii_safe_email(),
    ) for _ in range(n)]

    User.objects.bulk_create(users, ignore_conflicts=True)

    my_id = User.objects.get(username="admin").pk

    user_ids = User.objects.exclude(id=my_id).values_list('id', flat=True)
    talks = []
    for _ in range(len(user_ids)):
        sent_talk = Talk(talk_from=User.objects.get(pk=my_id), talk_to=User.objects.get(pk=random.choice(user_ids)), talk= fakegen.text())        
        received_talk = Talk(talk_from=User.objects.get(pk=random.choice(user_ids)), talk_to=User.objects.get(pk=my_id), talk=fakegen.text())
        talks.extend([sent_talk, received_talk])

    Talk.objects.bulk_create(talks, ignore_conflicts=True)

    talks = Talk.objects.order_by("-time")[:2 * len(user_ids)]
    for talk in talks:
        talk.time = fakegen.date_time_this_decade(tzinfo=tz.gettz("Asia/Tokyo"))
    Talk.objects.bulk_update(talks, ['time'])

if __name__ == "__main__":
    print("Creating users...", end="")
    create_users(1000)
    print("Done.")