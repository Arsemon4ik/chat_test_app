from django.urls import path, re_path
from . import views

# Валідацію в urls.py через re_path
urlpatterns = [
    re_path(r'^start', views.create_thread, name='create_thread'),
    re_path(r'^(?P<thread_id>\w+)/$', views.get_thread, name='get_thread'),
    re_path(r'^thread_messages/(?P<thread_id>\w+)/$', views.get_messages_by_thread, name='thread_messages'),
    re_path(r'^delete_thread/(?P<thread_id>\w+)/$', views.delete_thread, name='delete_thread'),
    re_path(r'^view_message/(?P<message_id>\w+)/$', views.view_message, name='view_message'),
    re_path(r'^count_unread_messages', views.count_unread_messages, name='count_unread_messages'),
    path('', views.threads, name='threads'),
    re_path(r'^users', views.user_list, name='user_list')
]
