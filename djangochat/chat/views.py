from .serializers import UserSerializer
from .models import Thread
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import ThreadListSerializer, ThreadSerializer
from django.db.models import Q
from django.shortcuts import redirect, reverse


@api_view(['POST'])
def start_convo(request, ):
    data = request.data
    # print(myusername:=data['username'])
    # username = data.pop('username')
    # print(username)
    username = data.get('username', None)
    try:
        participant = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'message': 'You cannot chat with a non existent user'})

    conversation = Thread.objects.filter(participants__in=[request.user, participant])
    if conversation.exists():
        return redirect(reverse('get_conversation', args=(conversation[0].id,)))
    else:
        conversation = Thread.objects.create()
        conversation.participants.set([request.user.id, participant.id])
        return Response(ThreadSerializer(instance=conversation).data)


@api_view(['GET'])
def get_conversation(request, convo_id):
    conversation = Thread.objects.filter(id=convo_id)
    if not conversation.exists():
        return Response({'message': 'Thread does not exist'})
    else:
        serializer = ThreadSerializer(instance=conversation[0])
        return Response(serializer.data)


@api_view(['GET'])
def conversations(request):
    conversation_list = Thread.objects.filter(participants__in=[request.user])
    # print(conversation_list[0].participants.all())
    serializer = ThreadListSerializer(instance=conversation_list, many=True)
    return Response(serializer.data)
    # return Response({'gppd'})


@api_view(['GET'])
def user_list(request):
    users = User.objects.all().order_by('username')
    serializer = UserSerializer(instance=users, many=True)
    return Response(serializer.data)
