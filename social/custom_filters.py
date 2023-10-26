# custom_filters.py
from django import template

register = template.Library()

@register.filter
def unique_usernames(stories):
    usernames = set()
    unique_stories = []
    for story in stories:
        if story.user.username not in usernames:
            unique_stories.append(story)
            usernames.add(story.user.username)
    return unique_stories
