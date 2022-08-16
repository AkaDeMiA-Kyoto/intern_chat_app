import os
import random
#from venv import create
import django
from dateutil import tz
from faker import Faker
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE","intern.settings")
django.setup()

from myapp.models import CustomMessage, CustomUser

fakegen=Faker(["ja_JP"])

def create_users(n):
    users = [
        CustomUser(username=fakegen.user_name(),email=fakegen.ascii_safe_email())
        for _ in range(n)
    ]
    
    CustomUser.objects.bulk_create(users,ignore_conflicts=True)

    my_id = CustomUser.objects.get(username="Asmil1024").id
    mainUser=CustomUser.objects.get(id=my_id)

    user_ids = CustomUser.objects.exclude(id=my_id).values_list("id",flat=True)

    talks = []
    for _ in range(len(user_ids)):
        #送信
        anotherUser=CustomUser.objects.get(id=random.choice(user_ids))
        msg=fakegen.text()
        msgTime=fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
        sent_talk = CustomMessage(
            primeUser=mainUser,
            subUser=anotherUser,
            isReceipt=False,
            content=msg,
            createdTime=msgTime
        )
        received_talk=CustomMessage(
            primeUser=anotherUser,
            subUser=mainUser,
            isReceipt=True,
            content=msg,
            createdTime=msgTime
        )
        talks.extend([sent_talk,received_talk])

        #受信
        msg=fakegen.text()
        msgTime=fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
        sent_talk = CustomMessage(
            primeUser=mainUser,
            subUser=anotherUser,
            isReceipt=True,
            content=msg,
            createdTime=msgTime
        )
        received_talk=CustomMessage(
            primeUser=anotherUser,
            subUser=mainUser,
            isReceipt=False,
            content=msg,
            createdTime=msgTime
        )
        talks.extend([sent_talk,received_talk])
    CustomMessage.objects.bulk_create(talks,ignore_conflicts=True)

if __name__ == "__main__":
    print("creating users ...",end="")
    create_users(1000)
    print("done")
