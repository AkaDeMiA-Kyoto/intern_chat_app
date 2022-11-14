import os
import random

import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings.dev_settings")
django.setup()

from myapp.models import Talk, User

fakegen = Faker(["ja_JP"])

def create_users(n):
    """
    ダミーのユーザーとチャットの文章を作る。
    n: 作成するユーザーの人数
    """

    users = [
        User(username=fakegen.user_name(), email=fakegen.ascii_safe_email())
        for _ in range(n)
    ]

    User.objects.bulk_create(users, ignore_conflicts=True)

    my_instance = User.objects.get(username="Admin")

    # values_list メソッドを使うと、User オブジェクトから特定のフィールドのみ取り出すことができます。
    # 返り値はユーザー id のリストになります。
    user_instances = User.objects.exclude(id=my_instance.id)

    talks = []
    for _ in range(len(user_instances)):
        sent_talk = Talk(
            talk_from=my_instance,
            talk_to=random.choice(user_instances),
            talk=fakegen.text(),
        )
        received_talk = Talk(
            talk_from=random.choice(user_instances),
            talk_to=my_instance,
            talk=fakegen.text(),
        )
        talks.extend([sent_talk, received_talk])
    Talk.objects.bulk_create(talks, ignore_conflicts=True)

    # Talk の time フィールドは auto_now_add が指定されているため、 bulk_create をするときに
    # time フィールドが自動的に現在の時刻に設定されてしまいます。
    # 最新の 2 * len(user_ids) 個分は先ほど作成した Talk なので、これらを改めて取得し、
    # time フィールドを明示的に更新します。
    talks = Talk.objects.order_by("-time")[: 2 * len(user_instances)]
    for talk in talks:
        talk.time = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    Talk.objects.bulk_update(talks, fields=["time"])


if __name__ == "__main__":
    print("creating users ...", end="")
    create_users(5)
    print("done")