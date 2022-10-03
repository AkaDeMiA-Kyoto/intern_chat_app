from atexit import register
from django import template
from ..models import ChatContent
from django.db.models import Q
register = template.Library()

@register.filter
def get_latest_message(id1, id2):
    messages = ChatContent.objects.filter((Q(send_from__id=id1) & Q(send_to__id=id2)) | (Q(send_from__id=id2) & Q(send_to__id=id1))).order_by('-pub_date')
    if len(messages) != 0:
        return messages[0]
    else:
        return ""