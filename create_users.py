import os
import random

import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings")
django.setup()

from myapp.models import Talk_content, CustomUser

fakegen = Faker(["ja_JP"])

def create_users(n):
    """
    ダミーのユーザーとチャットの文章を作る。
    n: 作成するユーザーの人数
    """

    users = [
        CustomUser(username=fakegen.user_name(), email=fakegen.ascii_safe_email())
        for _ in range(n)
    ]

    CustomUser.objects.bulk_create(users, ignore_conflicts=True)

    my_id = CustomUser.objects.get(username="admin").id

    # values_list メソッドを使うと、CustomUser オブジェクトから特定のフィールドのみ取り出すことができます。
    # 返り値はユーザー id のリストになります。
    user_ids = CustomUser.objects.exclude(id=my_id).values_list("id", flat=True)

    talks = []
    for _ in range(len(user_ids)):
        sent_talk = Talk_content(
            user_from=CustomUser.objects.get(id=my_id),
            user_to=CustomUser.objects.get(id=random.choice(user_ids)),
            chat_content=fakegen.text(),
        )
        received_talk = Talk_content(
            user_from=CustomUser.objects.get(id=random.choice(user_ids)),
            user_to=CustomUser.objects.get(id=my_id),
            chat_content=fakegen.text(),
        )
        talks.extend([sent_talk, received_talk])
    Talk_content.objects.bulk_create(talks, ignore_conflicts=True)

    # Talk_content の time フィールドは auto_now_add が指定されているため、 bulk_create をするときに
    # time フィールドが自動的に現在の時刻に設定されてしまいます。
    # 最新の 2 * len(user_ids) 個分は先ほど作成した Talk_content なので、これらを改めて取得し、
    # time フィールドを明示的に更新します。
    talks = Talk_content.objects.order_by("-time")[: 2 * len(user_ids)]
    for talk in talks:
        talk.time = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    Talk_content.objects.bulk_update(talks, fields=["time"])


if __name__ == "__main__":
    print("creating users ...", end="")
    create_users(1000)
    print("done")
