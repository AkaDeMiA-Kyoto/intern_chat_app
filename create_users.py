import os
import random

import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings")
django.setup()

from myapp.models import Talk
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
User = get_user_model()

fakegen = Faker(["ja_JP"])

def create_users(n):
    """
    ダミーのユーザーとチャットの文章を作る。
    n: 作成するユーザーの人数
    """

    fakegen.unique.clear()

    uname_field = User.USERNAME_FIELD  # 'username' or 'email'
    admin_identifier = "admin@example.com" if uname_field == "email" else "admin"

    defaults = {
        "is_staff": True,
        "is_superuser": True,
        "password": make_password("admin1234"),
    }
    if uname_field != "email":
        defaults.setdefault("email", "admin@example.com")

    admin, _ = User._default_manager.get_or_create(
        **{uname_field: admin_identifier},
        defaults=defaults,
    )
    my_id = admin.id
    user_ids = list(User.objects.exclude(id=my_id).values_list("id", flat=True))

    seen = {getattr(admin, uname_field)}

    new_users = []
    for _ in range(n):
        if uname_field == "email":
            identifier = fakegen.unique.ascii_safe_email()
            user_kwargs = {"email": identifier}
        else:
            identifier = fakegen.unique.user_name()
            user_kwargs = {"username": identifier, "email": fakegen.ascii_safe_email()}

        seen.add(identifier)
        user_kwargs["password"] = make_password("pass1234")
        new_users.append(User(**user_kwargs))

    User.objects.bulk_create(new_users, ignore_conflicts=True)

    talks = []
    for _ in range(len(user_ids)):
        sent_talk = Talk(
            talk_from_id=my_id,
            talk_to_id=random.choice(user_ids),
            talk=fakegen.text(),
        )
        received_talk = Talk(
            talk_from_id=random.choice(user_ids),
            talk_to_id=my_id,
            talk=fakegen.text(),
        )
        talks.extend([sent_talk, received_talk])
    Talk.objects.bulk_create(talks, ignore_conflicts=True)

    # Talk の time フィールドは auto_now_add が指定されているため、 bulk_create をするときに
    # time フィールドが自動的に現在の時刻に設定されてしまいます。
    # 最新の 2 * len(user_ids) 個分は先ほど作成した Talk なので、これらを改めて取得し、
    # time フィールドを明示的に更新します。
    talks = Talk.objects.order_by("-time")[: 2 * len(user_ids)]
    for talk in talks:
        talk.time = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    Talk.objects.bulk_update(talks, fields=["time"])


if __name__ == "__main__":
    print("creating users ...", end="")
    create_users(400)
    print("done")