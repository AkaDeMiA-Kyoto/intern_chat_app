import os
import random

import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings")
django.setup()
from myapp.models import TalkContent, CustomUser

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

    my_id = CustomUser.objects.get(username="shumpei128").id

    # values_list メソッドを使うと、User オブジェクトから特定のフィールドのみ取り出すことができます。
    # 返り値はユーザー id のリストになります。
    user_ids = CustomUser.objects.exclude(id=my_id).values_list("id", flat=True)

    talks = []
    for _ in range(len(user_ids)):
        sent_talk = TalkContent(
            send_id=my_id,
            receive_id=random.choice(user_ids),
            sentence=fakegen.text(),
        )
        received_talk = TalkContent(
            send_id=random.choice(user_ids),
            receive_id=my_id,
            sentence=fakegen.text(),)
        talks.extend([sent_talk, received_talk])
    TalkContent.objects.bulk_create(talks, ignore_conflicts=True)
    # Talk の time フィールドは auto_now_add が指定されているため、 bulk_create をするときに
    # time フィールドが自動的に現在の時刻に設定されてしまいます。
    # 最新の 2 * len(user_ids) 個分は先ほど作成した Talk なので、これらを改めて取得し、
    # time フィールドを明示的に更新します。
    talks = TalkContent.objects.order_by("-date")[: 2 * len(user_ids)]
    for talk in talks:
        talk.date = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    TalkContent.objects.bulk_update(talks, fields=["date"])


if __name__ == "__main__":
    print("creating users ...", end="")
    create_users(1000)
    print("done")
