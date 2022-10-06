from .models import Talk, CustomUser
from django.db.models import Q
import operator

def create_latest_talk(user):
    
    friends = CustomUser.objects.exclude(id=user.id)

    info = []
    message = []
    no_message = []

    for friend in friends:
        latest_talk = Talk.objects.select_related('CustomUser').filter( Q(talk_from=user, talk_to=friend) | Q(talk_from=friend, talk_to=user) ).order_by('talk_at').last()
        
        if latest_talk:
            message.append([friend, latest_talk.content, latest_talk.talk_at])
        else:
            no_message.append([friend, None, None])
        
    info_have_message = sorted(message, key=operator.itemgetter(2), reverse=True)
    
    info.extend(message)
    info.extend(no_message)

    return info