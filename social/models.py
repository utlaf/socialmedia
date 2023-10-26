from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.core.files.images import get_image_dimensions
from django.core.validators import FileExtensionValidator
import PIL
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Q
import datetime
from django.utils import timezone
from datetime import timedelta


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    profile_image = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    last_online = models.DateTimeField(default=timezone.now)
    date_modified = models.DateField(User, auto_now=True)


    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
       return reverse('profile', kwargs={'pk': self.pk})
    def get_num_posts(self):
        return self.user.post_set.count()

    def get_num_followers(self):
        return self.followed_by.count()

    def get_num_following(self):
        return self.follows.count()
    
    def set_online(self):
        self.is_online = True
        self.last_updated = timezone.now()
        self.save()
    

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

        # Allow the user to follow themselves
        user_profile.follows.add(user_profile)
        user_profile.save()

post_save.connect(create_profile, sender=User)

        

class Post(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='post_images', blank=True) 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_like',blank=True)

    def num_of_likes(self):
        return self.likes.count()
    
    
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_like', blank=True)
    

    def __str__(self):
        return self.text


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stories', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField()
    viewers = models.ManyToManyField(User, related_name='viewed_stories', blank=True)
    views_count = models.IntegerField(default=0)
    unique_views_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.expiration_time:
            # Set the expiration time to 24 hours from the current time
            self.expiration_time = timezone.now() + timedelta(hours=24)
        super(Story, self).save(*args, **kwargs)

    def is_expired(self):
        now = timezone.now()
        return self.expiration_time <= now

    def view_story(self, user):
        if user not in self.viewers.all():
            self.viewers.add(user)
            self.views_count += 1
            self.unique_views_count = self.viewers.count()

    def __str__(self):
        return f"{self.user.username}'s Story"
    
  
    

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_messages', null=True, blank=True)
    receiver_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver} at {self.timestamp}'

    def save(self, *args, **kwargs):
        # Set sender and receiver profiles
        self.sender_profile = self.sender.profile
        self.receiver_profile = self.receiver.profile
        super(Message, self).save(*args, **kwargs)


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.recipient} at {self.timestamp}'
    
    
    def is_expired(self):
        expiration_time = timezone.now() - timezone.timedelta(hours=1)  # Adjust as needed
        return self.timestamp < expiration_time

    
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(recipient=instance.receiver, message=instance)
   
