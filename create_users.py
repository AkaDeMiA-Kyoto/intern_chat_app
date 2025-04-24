import os
import random

import django
from dateutil import tz
from faker import Faker
from django.core.files.base import ContentFile
from PIL import Image
import io
import random


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings")
django.setup()

from myapp.models import TalkLog, CustomUser

fakegen = Faker(["ja_JP"])


def generate_dummy_image():
    img = Image.new(
        "RGB",
        (100, 100),
        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    )

    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    return ContentFile(buf.read(), name="dummy.jpg")


def create_users(n):
    users = [
        CustomUser(
            username=fakegen.user_name(),
            email=fakegen.ascii_safe_email(),
            image=generate_dummy_image(),
        )
        for _ in range(n)
    ]

    CustomUser.objects.bulk_create(users, ignore_conflicts=True)
    my_id = CustomUser.objects.get(username="shu").id
    me = CustomUser.objects.get(username="shu")
    user_ids = CustomUser.objects.exclude(id=my_id).values_list("id", flat=True)

    talks = []

    for _ in range(len(user_ids) * 3):
        talk = TalkLog(
            fromuser=me,
            touser=CustomUser.objects.get(id=random.choice(user_ids)),
            message=fakegen.text(),
        )
        talks.extend([talk])
        talk = TalkLog(
            fromuser=CustomUser.objects.get(id=random.choice(user_ids)),
            touser=me,
            message=fakegen.text(),
        )
        talks.extend([talk])

    TalkLog.objects.bulk_create(talks, ignore_conflicts=True)

    talks = TalkLog.objects.order_by("-timestamp")[: 2 * len(user_ids)]
    for talk in talks:
        talk.timestamp = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    TalkLog.objects.bulk_update(talks, fields=["timestamp"])


if __name__ == "__main__":
    print("creating users ...", end="")
    create_users(10)
    print("done")
