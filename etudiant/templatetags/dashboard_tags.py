from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def is_due_soon(due_date):
    return due_date <= timezone.now() + timezone.timedelta(days=3)

@register.filter
def days_until(due_date):
    delta = due_date - timezone.now().date()
    return delta.days