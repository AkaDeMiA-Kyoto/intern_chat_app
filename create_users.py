import os
import random

import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings")
django.setup()

from myapp.models import Chat, CustomUser
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

    me = CustomUser.objects.get(username="admin")

    # values_list メソッドを使うと、User オブジェクトから特定のフィールドのみ取り出すことができます。
    # 返り値はユーザー id のリストになります。
    users = CustomUser.objects.exclude(id=me.id)

    talks = []
    for _ in range(len(users)):
        talk1 = Chat(
            chat_to=me,
            chat_from=random.choice(users),
            chat=fakegen.text(),
        )
        talk2 = Chat(
            chat_to=random.choice(users),
            chat_from=me,
            chat=fakegen.text(),
        )
        talks.extend([talk1,talk2])
    Chat.objects.bulk_create(talks, ignore_conflicts=True)

    # Talk の time フィールドは auto_now_add が指定されているため、 bulk_create をするときに
    # time フィールドが自動的に現在の時刻に設定されてしまいます。
    # 最新の 2 * len(user_ids) 個分は先ほど作成した Talk なので、これらを改めて取得し、
    # time フィールドを明示的に更新します。
    '''talks = Chat.objects.order_by("-time")[: 2 * len(users)]
    for talk in talks:
        talk.time = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    Talk.objects.bulk_update(talks, fields=["time"])
    '''


if __name__ == "__main__":
    print("creating users ...", end="")
    create_users(5)
    print("done")