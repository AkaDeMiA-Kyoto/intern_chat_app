import os

import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings")
django.setup()

from myapp.models import Talk, User

fakegen = Faker(["ja_JP"])

def create_users(n):
    users = [
        User(username=fakegen.user_name(), email=fakegen.ascii_safe_email())
        for _ in range(n)
    ]

    User.objects.bulk_create(users, ignore_conflicts=True)

    users_all = list(User.objects.all().order_by("id"))
    users = users_all[len(users_all)-n:]
    me = User.objects.get(username="denden")

    talks = []

    for user in users:
        sent_talk = Talk(
            sender=me,
            receiver=user,
            message=fakegen.text(max_nb_chars=35)
        )
        receiver_talk = Talk(
            sender=user,
            receiver=me,
            message=fakegen.text(max_nb_chars=35)
        )
        talks.extend([sent_talk, receiver_talk])

    Talk.objects.bulk_create(talks, ignore_conflicts=True)

    talks = Talk.objects.order_by("-sent_time")[: 2 * len(users)]
    for talk in talks:
        talk.sent_time = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    Talk.objects.bulk_update(talks, fields=["sent_time"])

if __name__ == "__main__":
    print("creating users ...", end="")
    create_users(10)
    print("done")


