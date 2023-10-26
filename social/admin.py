from django.contrib import admin
from .models import Post,Profile,Comment,Story,Message,Notification
from django.contrib.auth.models import User, Group
# Register your models here.
admin.site.unregister(Group)
admin.site.register(Post)
admin.site.register(Story)
admin.site.register(Message)
admin.site.register(Notification)



# admin.site.register(Profile)
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User,UserAdmin)


class CommentInline(admin.StackedInline):
  model = Comment
  
class PostAdmin(admin.ModelAdmin):
  inlines = [CommentInline]

admin.site.unregister(Post)
admin.site.register(Post, PostAdmin)










