from django.db.models import Q, Count
from django.utils import timezone
from django.core.paginator import Paginator


# Create your views here.


def participated_projects(user):
    return user.annotate(participated_projects=Count('participants'))


def interested_users(project):
    return project.annotate(interested_users=Count('favorites'))


def page_paginator(request, list):
    paginator = Paginator(list, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
