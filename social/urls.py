from django.urls import path,include
from. import views
from .views import send_message, get_messages


urlpatterns = [
    path('base/',views.base,name='base'),
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('registration/',views.registration,name='registration'),
    path('handlelogout/',views.handlelogout,name='handlelogout'),
    path('new_post/', views.add_post, name='add_post'),
    path('profile/<int:pk>/', views.Profile, name='profile'),
    path('edit_profile/<int:pk>/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('images/<str:filename>/', views.profile_image_view, name='profile_image'),
    path('post/<int:pk>/like/', views.post_like, name='post_like'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('search/', views.search_users, name='search_users'),
    path('add_reply/<int:comment_id>/', views.add_reply, name='add_reply'),
    # path('stories/view_stats/<int:story_id>/', views.view_story_stats, name='view_story_stats'),
    path('stories/', views.StoryListView.as_view(), name='story-list'),
    path('story/', views.story_view, name='story_view'),
    path('add_story/', views.add_story, name='add_story'),
    path('stories1/', views.view_stories, name='view_stories'),
    path('view_status/<str:username>/', views.view_status, name='view_status'),
    path('send_message/<int:receiver_id>/', send_message, name='send_message'),
    path('get_messages/<int:receiver_id>/', get_messages, name='get_messages'),
    path('direct/',views.direct,name='direct'),
    path('personal_chat/<int:receiver_id>/',views. personal_chat, name='personal_chat'),
    path('send_personal_message/<int:receiver_id>/', views.send_personal_message, name='send_personal_message'),
    path('get_personal_messages/<int:receiver_id>/', views.get_personal_messages, name='get_personal_messages'),
    path('profile/<int:pk>/update/', views.update_profile_status, name='update_profile_status'),
    path('send_message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('get_messages/<int:receiver_id>/', views.get_messages, name='get_messages'),
    path('delete_notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('api/user/<int:user_id>/data/', views.get_user_data, name='user-data-api'),
    path('api/user/<int:user_id>/stories/', views.get_user_stories, name='user-stories-api'),
  



]
