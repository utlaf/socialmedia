from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import login as django_login
from django.contrib.auth import login as django_logout
from django.contrib.auth.decorators import login_required
from .models import Post,Profile
from django.utils.datastructures import MultiValueDictKeyError
from .forms import PostForm,ProfileForm
from django.shortcuts import get_object_or_404
from django.db.models import F,Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Profile as UserProfile
from django.views.generic import UpdateView  
from .forms import ProfileForm,StoryForm
from django.urls import reverse_lazy
from .forms import CommentForm,CustomPasswordResetForm
from .models import Comment
from .models import Message,Notification
from django.views.generic import TemplateView
import requests
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.exceptions import PermissionDenied
import json
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Story
from datetime import datetime
from django.core.cache import cache
from django.db import transaction
import datetime
from django.shortcuts import render, redirect
from .forms import PostForm, StoryForm
from .models import Post, Story
from django.contrib.auth.decorators import login_required
import datetime
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Post, Message, Notification, Story
from django.template.defaultfilters import timesince

# HOME
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import F, Count
from django.views import View
from .models import Post, Message, Notification, Story  # Import your models
from .forms import PostForm  # Import your form for creating posts
from datetime import timedelta


@login_required
def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Send a notification to the receiver
            receiver_username = 'receiver_username'  # Replace with actual username
            try:
                receiver = User.objects.get(username=receiver_username)
                # Create a message associated with the post
                message = Message.objects.create(sender=request.user, receiver=receiver, content='onii sama message')
                Notification.objects.create(recipient=receiver, message=message)
            except User.DoesNotExist:
                # Handle the case where the receiver does not exist
                receiver = None  # Set receiver to None or handle it according to your needs

            return redirect('home')
    else:
        form = PostForm()

    # Fetch both posts and stories and order them by the created date
    posts = Post.objects.order_by(F('created').desc())

    # Fetch notifications for the logged-in user with sender names and message counts
    notifications = Notification.objects.filter(recipient=request.user, is_read=False) \
                    .values('message__sender__username', 'message__sender__id', 'id') \
                    .annotate(message_count=Count('message'))

    # Get the currently logged-in user's profile
    user_profile = request.user.profile

    # Get the stories of users the current user is following, excluding their own stories
    following_users = user_profile.follows.all()
    following_stories = Story.objects.filter(user__profile__in=following_users).exclude(user=request.user)

    unique_users = set()  # Create a set to track unique user IDs
    unique_stories = []

    for story in following_stories:
        if story.user.id not in unique_users:
            unique_users.add(story.user.id)
            unique_stories.append(story)

    context = {
        'posts': posts,
        'form': form,
        'notifications': notifications,
        'following_stories': unique_stories,  # Pass the unique stories to the template
    }

    return render(request, 'home.html', context)


# <--------------------------------------------------------------------------------------->



@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.delete()
    return JsonResponse({'message': 'Notification deleted successfully'})




def base(request):
    return render(request,'base.html')


def registration(request):
    if request.method == 'POST':
        
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['username']
        
        if User.objects.filter(username=username).exists():
            error_message = 'Username already exists.'
            return render(request, 'registration.html', {'error_message': error_message})

        myuser = User.objects.create_user(username,email,password)

        myuser.save()
        return redirect('login')
 
    return render(request,'registration.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        if user is not None:
            django_login(request, user)
            messages.success(request,"you are loged in succesfully")
            return redirect("/")
        else:
            messages.error(request,"Invalid username & pass") 
            return redirect("login") 
            

    return render(request,'login.html')

def handlelogout(request):
    logout(request)
    messages.success(request,"you are logged out succesfully")
    return redirect("login")




@login_required
def add_post(request):
  if request.method == 'POST':
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user 
      post.save()
      return redirect('home')
  
  form = PostForm()
  return render(request, 'add_post.html', {'form': form})

@login_required
def Profile(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user_id=pk)
        posts = Post.objects.filter(author=profile.user)

        # Update user's last online time
        profile.set_online()

        if request.method == 'POST':
            current_user_profile = request.user.profile
            action = request.POST.get('follow', None)
            print(f"Action: {action}")  # Print the action for debugging
            if action == 'Unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        # Rest of your view logic

        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # If it's an AJAX request, return JSON response for real-time updates
            data = {
                'is_online': profile.is_online,
                'last_updated': profile.last_updated.isoformat(),
                # Add other profile data as needed
            }
            return JsonResponse(data)

        # If it's not an AJAX request, render the regular template
        return render(request, 'profile.html', {"profile": profile, 'posts': posts})
    else:
        return redirect("home")
    



@login_required
def update_profile_status(request, pk):
    try:
        # Retrieve the user profile
        profile = get_object_or_404(UserProfile, user__id=pk)  # Update this line if user_id is stored in a different field

        # Update the user's online status
        profile.set_online()

        # Return a JSON response with relevant information
        data = {
            'is_online': profile.is_online,
            'last_updated': profile.last_updated.isoformat(),
        }
        return JsonResponse(data)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found'}, status=404)
    except Exception as e:
        # Print or log the exception for debugging
        print(e)
        return JsonResponse({'error': 'Internal Server Error'}, status=500)




# @login_required
# def edit_profile(request, pk):
#     profile = Profile.objects.get(pk=pk)
#     if profile.user != request.user:
#         return HttpResponseForbidden()

#     form = ProfileForm(instance=profile)
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile', pk=pk)

#     context = {'form': form}
#     return render(request, 'edit_profile.html', context)

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'social/profile_form.html'

    def get_object(self, queryset=None):
        # Retrieve the user's profile
        profile = self.request.user.profile
        return profile

    def form_valid(self, form):
        # Save the form with the user's profile data
        response = super(ProfileUpdateView, self).form_valid(form)
        # Redirect to the 'edit_profile' URL with the user's ID as a parameter
        return HttpResponseRedirect(reverse_lazy('profile', kwargs={'pk': self.request.user.id}))


def profile_image_view(request, filename):
    # Logic to serve profile images, return appropriate HttpResponse
    pass

  





def profile_image_view(request, filename):
    # view to serve profile images
    return HttpResponse()

def post_like(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)

        # Check if the user has already liked the post
        user_has_liked = post.likes.filter(id=request.user.id).exists()

        if user_has_liked:
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        # Return JSON response with updated like status and count
        likes_count = post.likes.count()
        data = {
            'liked': liked,
            'likes_count': likes_count,
        }
        return JsonResponse(data)
    else:
        # If user is not authenticated, return a 403 Forbidden status
        return JsonResponse({'error': 'User not authenticated'}, status=403)




def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_comment_id = request.POST.get('parent_comment_id')
            parent_comment = None
            if parent_comment_id:
                parent_comment = get_object_or_404(Comment, id=parent_comment_id)
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.parent_comment = parent_comment
            comment.save()

            # Assuming you have a function to serialize comment data
            serialized_comment = serialize_comment(comment)

            # Redirect to the post detail page for the comment
            return redirect('post_detail', post_id=post_id)
        else:
            # If form is not valid, return form errors
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CommentForm()

    context = {
        'form': form,
        'post': post
    }

    return render(request, 'add_comment.html', context)


# Assuming you have a function to serialize comment data
def serialize_comment(comment):
    return {
        'id': comment.id,
        'text': comment.text,
        'user': comment.user.username,
        # Add other fields you need
    }



def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post, parent_comment=None)
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

def search_users(request):
    query = request.GET.get('query')
    
    if query:
        # Search users where username or full name contains the query
       users = User.objects.filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
)
    else:
        users = User.objects.none()
    
    context = {
        'users': users,
        'query': query
    }
    
    return render(request, 'search_results.html', context)


def add_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        new_reply = Comment.objects.create(
            text=text,
            user=request.user,
            parent_comment=parent_comment,
            post=parent_comment.post  # Set the post field here
        )

        # Assuming you have a function to serialize reply data
        serialized_reply = serialize_comment(new_reply)

        return JsonResponse({'success': True, 'reply': serialized_reply})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    

                                                            # Story
def get_user_data(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        profile = user.profile
        data = {
            'username': user.username,
            'profile_image': profile.profile_image.url,
        }
        return JsonResponse(data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

def get_user_stories(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        stories = Story.objects.filter(user=user)
        data = {
            'stories': [{'image': story.image.url} for story in stories]
        }
        return JsonResponse(data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    




@login_required
def view_story_viewers(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    viewers = story.viewers.all()
    return render(request, 'view_story_viewers.html', {'story': story, 'viewers': viewers})

class StoryListView(LoginRequiredMixin, View):
    template_name = 'list_stories.html'  # Replace with your actual template name

    def get(self, request, *args, **kwargs):
        # Get the currently logged-in user's profile
        user_profile = request.user.profile

        # Get the stories of users the current user is following, excluding their own stories
        following_users = user_profile.follows.all()
        following_stories = Story.objects.filter(user__profile__in=following_users).exclude(user=request.user)

        unique_users = set()  # Create a set to track unique user IDs
        unique_stories = []

        for story in following_stories:
            if story.user.id not in unique_users:
                unique_users.add(story.user.id)
                unique_stories.append(story)

        context = {
            'following_stories': unique_stories,  # Pass the unique stories to the template
        }

        return render(request, self.template_name, context)



# zuck
def story_view(request):
    stories = []

    now = timezone.now()
    expiration_time_limit = now - timedelta(hours=24)  # Calculate the expiration time limit (24 hours ago)

    for story in Story.objects.filter(expiration_time__gt=now):
        items = []

        items.append({
            "id": story.id,
            "length": 3,
            "src": story.image.url,
            "time": timesince(story.created),
            "lastUpdated": timesince(story.created),
        })

        user = story.user

        stories.append({
            "id": user.id,
            "photo": user.profile.profile_image.url,
            "items": items,
            "name": user.username,
            "time": timesince(story.created),
        })

        # Check if the user viewing the story is authenticated
        if request.user.is_authenticated:
            # Call the view_story method to record the view
            story.view_story(request.user)

    context = {'stories': json.dumps(stories)}

    return render(request, 'zuck.html', context)







@login_required
def add_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user  # Use the user directly, not the profile

            # Check if the user has uploaded an image
            if not story.image:
                messages.error(request, 'You must upload an image to create a story.')
                return render(request, 'add_story.html', {'form': form})

            story.save()

            # Redirect to the story section
            return redirect('add_story')

    else:
        form = StoryForm()

    # Fetch stories for the current user and their follows
    active_stories = Story.objects.filter(expiration_time__gt=timezone.now())

    current_user = request.user
    follows = current_user.profile.follows.all()
    stories = Story.objects.filter(user__profile__in=follows).order_by('-created')

    return render(request, 'add_story.html', {'form': form, 'current_user_stories': stories})

@login_required
def view_stories(request):
    # Fetch current user's active stories
    current_user_stories = Story.objects.filter(user=request.user, expiration_time__gt=timezone.now())

    # Fetch followers' active stories
    followers_stories = Story.objects.filter(
        user__profile__in=request.user.profile.follows.all(),
        expiration_time__gt=timezone.now()
    )

    return render(request, 'home.html', {'current_user_stories': current_user_stories, 'followers_stories': followers_stories})




def view_status(request, username):
    user = User.objects.get(username=username)
    profile = user.profile

    # Increment view count and add viewer
    profile.objects.update(view_count=F('view_count') + 1)
    profile.views.add(request.user)
    profile.save()

    return render(request, 'view_status.html', {'user': user})

def view_stories(request):
    # Fetch stories from all users
    all_users = User.objects.all()
    all_stories = Story.objects.filter(user__in=all_users)
    return render(request, 'view_stories.html', {'stories': all_stories})



                                                                # messages

@login_required
@require_POST
def send_message(request, receiver_id):
    # Get the receiver based on the receiver_id parameter
    receiver = get_object_or_404(User, id=receiver_id)

    if request.user.is_authenticated:
        content = request.POST.get('content', '')

        # Check if the content is not empty
        if content:
            # Create a message
            message = Message(sender=request.user, receiver=receiver, content=content)
            message.save()

            return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid message content'})


@login_required
def get_messages(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user))
    ).order_by('timestamp')

    data = [{'content': message.content, 'timestamp': message.timestamp} for message in messages]

    return JsonResponse({'success': True, 'messages': data})

@login_required
def direct(request):

    followers = request.user.profile.followed_by.annotate(
        message_count=Count('user__received_messages')
    )

    # Assuming you want to set the first follower as the receiver
    if followers.exists():
        receiver = followers.first().user
    else:
        receiver = None  # Handle the case where there are no followers

    context = {
        'followers': followers,
        'receiver': receiver
    }

    return render(request, 'direct/message_form.html', context)



@login_required
def personal_chat(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user))
    ).order_by('timestamp')

    context = {
        'receiver': receiver,
        'messages': messages,
    }

    return render(request, 'direct/personal_chat.html', context)

@login_required
def send_personal_message(request, receiver_id):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        receiver = get_object_or_404(User, id=receiver_id)

        # Allow everyone to send messages, regardless of followers
        message = Message(sender=request.user, receiver=receiver, content=content)
        message.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def get_personal_messages(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user))
    ).order_by('timestamp')

    data = [{'content': message.content, 'timestamp': message.timestamp, 'sender': message.sender.username} for message in messages]

    return JsonResponse({'success': True, 'messages': data, 'receiver': receiver.username})