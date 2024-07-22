from django import template

register = template.Library()

@register.filter(name='is_video')
def is_video(url):
    return url.lower().endswith('.mp4')

@register.filter(name='is_audio')
def is_audio(url):
    return url.lower().endswith('.mp3')
