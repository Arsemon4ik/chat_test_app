from .serializers import UserSerializer
from .models import Thread, Message
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import ThreadListSerializer, ThreadSerializer, MessageListSerializer, MessageSerializer
from django.db.models import Q
from django.shortcuts import redirect, reverse


@api_view(['POST'])
def create_thread(request, ):
    """Створення (якщо Thread з такими user'ами існує - повертаємо його)"""

    data = request.data
    username = data.get('username', None)
    try:
        participant = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'message': 'You can not chat with a non existent user'})

    thread = Thread.objects.filter(participants__in=[request.user, participant])
    if thread.exists():
        return redirect(reverse('get_thread', args=(thread[0].id,)))
    else:
        new_thread = Thread.objects.create()
        new_thread.participants.set([request.user.id, participant.id])
        return Response(ThreadSerializer(instance=new_thread).data)


@api_view(['DELETE'])
def delete_thread(request, thread_id):
    """Видалення Thread'а для заданого Thread_id, якщо User є в списку participants"""

    thread = Thread.objects.filter(id=thread_id)
    if not thread.exists():
        return Response({'message': 'Thread does not exist'})
    elif not thread.filter(participants__in=[request.user]).exists():
        return Response({'message': 'You are not allowed to delete this Thread'})
    else:
        thread.delete()
        return Response({'message': f'You have successfully deleted thread with id:{thread_id}'})


@api_view(['GET'])
def get_thread(request, thread_id):
    """Одержання списку Thread'ів для будь-якого user'a з останнім повідомленням, якщо таке є)"""

    thread = Thread.objects.filter(id=thread_id)
    if not thread.exists():
        return Response({'message': 'Thread does not exist'})
    else:
        serializer = ThreadSerializer(instance=thread[0])
        return Response(serializer.data)


@api_view(['GET'])
def get_messages_by_thread(request, thread_id):
    """Одержання списку Messages для заданого Thread"""

    thread = Thread.objects.filter(id=thread_id)
    user = request.user
    if not thread.exists():
        return Response({'message': 'Thread does not exist'})
    elif user not in thread[0].participants.all():
        return Response({'message': 'You are not allowed to view messages in this Thread'})
    else:
        messages_list = thread[0].message_set.all()
        serializer = MessageListSerializer(instance=messages_list, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def threads(request):
    """Одержання списку Thread'ів для будь-якого user'a з останнім повідомленням, якщо таке є)"""

    user = request.user
    thread_list = Thread.objects.filter(participants__in=[user])
    if not thread_list.exists():
        return Response({'message': f'Thread with user {user} does not exist'})
    serializer = ThreadListSerializer(instance=thread_list, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def user_list(request):
    """Одержання списку Юзерів для подальшого спілкування (щоб можна було під'єднатися по юзернейму)"""

    users = User.objects.all().order_by('username')
    if len(users) == 0:
        return Response({'message': f'Users table is empty'})
    serializer = UserSerializer(instance=users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def view_message(request, message_id):
    """Позначки що одне Message прочитано(is_read=True). Декілька можу в окремій функції :)"""

    participant = request.user
    message = Message.objects.filter(id=message_id)
    if not message.exists():
        return Response({'message': f'Message with id:{message_id} does not exist'})
    if participant not in message[0].thread.participants.all():
        return Response({'message': f'You are not allowed to read this message'})

    message.update(is_read=True)
    serializer = MessageSerializer(instance=message[0])
    return Response(serializer.data)


@api_view(['GET'])
def count_unread_messages(request, ):
    """Отримання кількості непрочитаних повідомлень для користувача"""

    participant = request.user
    participant_threads = participant.thread_set.all()

    if not participant_threads.exists():
        return Response({'message': f'Participant has not had threads yet'})

    # print(participant_threads[0].message_set.filter(is_read=False).exclude(sender=participant.id))
    unread_messages = sum([thread.message_set.filter(is_read=False).exclude(sender=participant).count() for thread in
                           participant_threads])
    return Response({'message': f'You have {unread_messages} unread messages!'})
