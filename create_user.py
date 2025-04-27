import os
import random

import django
from dateutil import tz
from faker import Faker
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings.base")
django.setup()

from myapp.models import Talk, User
from django.db import connection

fakegen = Faker(["ja_JP"])

def create_users(n):
    """
    ダミーのユーザーとチャットの文章を作る。
    n: 作成するユーザーの人数
    """
    
    print("DB接続先:", connection.settings_dict)
    print("BASE_DIR:", Path(__file__).resolve().parent.parent)
    print("ENV file exists?:", os.path.exists(os.path.join(Path(__file__).resolve().parent.parent, ".env")))

    users = [
        User(username=fakegen.user_name(), email=fakegen.ascii_safe_email())
        for _ in range(n)
    ]

    print(users,"+++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    try:
        User.objects.bulk_create(users, ignore_conflicts=True)
    except Exception as e:
        print(f"Error occurred while bulk creating users: {e}")

    my_id = User.objects.get(username="admin").id
    print(my_id,"#################################################################################")
    # values_list メソッドを使うと、User オブジェクトから特定のフィールドのみ取り出すことができます。
    # 返り値はユーザー id のリストになります。
    user_ids = User.objects.exclude(id=my_id).values_list("id", flat=True)
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
    create_users(1000)
    print("done")