import os
import random

import django
from dateutil import tz
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intern.settings.dev')
django.setup()

from myapp.models import ChatContent, MyUser
fakegen = Faker(['Ja-jp'])

def create_users(n):
    # n人データを作る
    users = [MyUser(username=fakegen.user_name(), email=fakegen.ascii_safe_email()) for _ in range(n)]
    MyUser.objects.bulk_create(users, ignore_conflicts=True)
    me = MyUser.objects.get(username='admin')
    my_id = me.id

    # values_listメソッドを使い、MyUserオブジェクトから特定のフィールドのみ取り出す
    # 返り値はユーザーidのリスト
    user_ids = MyUser.objects.exclude(id=my_id).values_list('id', flat=True)
    talks = []
    for _ in range(len(user_ids)):
        sent_talk = ChatContent(
            send_from = me,
            send_to = MyUser.objects.get(id=random.choice(user_ids)),
            chat_content = fakegen.text(),
        )
        received_talk = ChatContent(
            send_from = MyUser.objects.get(id=random.choice(user_ids)),
            send_to = me,
            chat_content = fakegen.text(),
        )
        talks.extend([sent_talk, received_talk])
    ChatContent.objects.bulk_create(talks, ignore_conflicts=True)

    # ChatContentのpub_dateが自動で入っているので、これを明示的に書き換える
    talks = ChatContent.objects.order_by('-pub_date')[: 2 * len(user_ids)]
    for talk in talks:
        talk.pub_date = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    ChatContent.objects.bulk_update(talks, fields=["pub_date"])

if __name__ == '__main__':
    print('creating users ...', end='')
    create_users(995)
    print('done')