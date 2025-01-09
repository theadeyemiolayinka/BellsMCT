import json
import random
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from .models import Blog, Event, News
from .forms import EnquiryFormSetFactory, EnquiryForm
from django.conf import settings


def index(request):
    latest_events = Event.objects.filter(deleted_at__isnull=True).order_by(
        "-start_time"
    )[:3]
    latest_events = [
        {
            "id": event.id,
            "title": event.title,
            "start_time": event.start_time,
            "end_time": event.end_time,
            "category": event.category,
            "description": event.description[:150] + "...",
            "image_url": f"{settings.MEDIA_URL}uploads/{event.image}",
            "url": f"/events/{event.slug}",
        }
        for event in latest_events
    ]

    latest_news = News.objects.filter(deleted_at__isnull=True)[:5]
    latest_news = [
        {
            "id": news.id,
            "title": news.title,
            "category": news.category,
            "description": news.description[:150] + "...",
            "image_url": f"{settings.MEDIA_URL}uploads/{news.image}",
            "url": f"/news/{news.slug}",
        }
        for news in latest_news
    ]
    context = {
        "events": latest_events,
        "news": latest_news
    }
    return render(request, "web/index.html", context)


def blog(request):
    posts = Blog.objects.filter(hidden_at__isnull=True)
    posts = [
        {
            "id": str(post.id),
            "title": post.title,
            "author": post.author.username,
            "created_at": post.created_at.strftime("%B %d, %Y"),
            "updated_at": post.updated_at.strftime("%B %d, %Y"),
            "tags": post.tags,
            "description": post.description[:150] + "..." if post.description else "",
            "image_url": f"{settings.MEDIA_URL}uploads/{post.image}",
            "url": f"/blog/{post.slug}",
        }
        for post in posts
    ]
    context = {
        "posts": posts,
    }
    return render(request, "web/blog.html", context)


def blog_read(request, slug):
    post = get_object_or_404(Blog, slug=slug, hidden_at__isnull=True)

    context = {
        "post": post,
        "author": post.author.username,
        "author_profile": "https://placehold.co/600x400?text="
        + post.author.username[0].upper(),
        "tags": post.tags,
        "content": post.content,
        "description": post.description[:150] + "..." if post.description else "",
        "created_at": post.created_at.strftime("%B %d, %Y"),
        "updated_at": post.updated_at.strftime("%B %d, %Y"),
        "image_url": f"{settings.MEDIA_URL}uploads/{post.image}",
    }

    return render(request, "web/blog_read.html", context)


def dashboard_callback(request, context):
    WEEKDAYS = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    positive = [[1, random.randrange(8, 30)] for i in range(1, 30)]
    negative = [[-1, -random.randrange(8, 30)] for i in range(1, 30)]
    average = [r[1] - random.randint(3, 5) for r in positive]
    # performance_positive = [[1, random.randrange(8, 30)] for i in range(1, 30)]
    # performance_negative = [[-1, -random.randrange(8, 30)] for i in range(1, 30)]

    context.update(
        {
            "stats": [
                {"title": "Total Events", "value": Event.objects.count()},
                {"title": "Total Users", "value": User.objects.count()},
            ],
            "chart": json.dumps(
                {
                    "labels": [WEEKDAYS[day % 7] for day in range(1, 30)],
                    "datasets": [
                        {
                            "label": "Analysis",
                            "type": "line",
                            "data": average,
                            "backgroundColor": "#f0abfc",
                            "borderColor": "#f0abfc",
                        },
                        {
                            "label": "This Month",
                            "data": positive,
                            "backgroundColor": "#9333ea",
                        },
                        {
                            "label": "Last Month",
                            "data": negative,
                            "backgroundColor": "#f43f5e",
                        },
                    ],
                }
            ),
        }
    )
    return context


def news(request):
    latest_news = News.objects.filter(deleted_at__isnull=True)

    latest_news = [
        {
            "id": news.id,
            "title": news.title,
            "category": news.category,
            "description": news.description[:150] + "...",
            "image_url": f"{settings.MEDIA_URL}uploads/{news.image}",
            "url": f"/news/{news.slug}",
        }
        for news in latest_news
    ]
    context = {
        "news": latest_news,
    }
    return render(request, "web/news.html", context)


def news_details(request, slug):
    news = get_object_or_404(News, slug=slug, deleted_at__isnull=True)

    context = {
        "news": news,
        "image_url": f"{settings.MEDIA_URL}uploads/{news.image}",
    }

    return render(request, "web/news_details.html", context)


def events(request):
    latest_events = Event.objects.filter(deleted_at__isnull=True).order_by(
        "-start_time"
    )
    latest_events = [
        {
            "id": event.id,
            "title": event.title,
            "start_time": event.start_time,
            "end_time": event.end_time,
            "category": event.category,
            "description": event.description[:150] + "...",
            "image_url": f"{settings.MEDIA_URL}uploads/{event.image}",
            "url": f"/events/{event.slug}",
        }
        for event in latest_events
    ]
    context = {
        "events": latest_events,
    }
    return render(request, "web/events.html", context)


def events_details(request, slug):
    event = get_object_or_404(Event, slug=slug, deleted_at__isnull=True)

    context = {
        "event": event,
        "image_url": f"{settings.MEDIA_URL}uploads/{event.image}",
    }

    return render(request, "web/events_details.html", context)


def events_json(request):
    events = Event.objects.filter(deleted_at__isnull=True)
    data = [
        {
            "id": str(event.id),
            "title": event.title,
            "start": event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end": (
                None
                if event.start_time.strftime("%Y-%m-%d %H:%M:%S")
                == event.end_time.strftime("%Y-%m-%d %H:%M:%S")
                else event.end_time.strftime("%Y-%m-%d %H:%M:%S")
            ),
            "url": f"/admin/web/event/{event.id}/change/",
        }
        for event in events
    ]
    return JsonResponse(data, safe=False)


def enquiry(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            form.clean()
            return render(
                request,
                "web/enquiry.html",
                {
                    "form": EnquiryForm(),
                    "messages": [
                        {
                            "message": "Enquiry submitted successfully.",
                            "tags": "alert-success",
                        }
                    ],
                },
                status=201,
            )
        else:
            return render(
                request,
                "web/enquiry.html",
                {"form": form, "errors": form.errors},
                status=400,
            )
    pass

    form = EnquiryForm
    context = {"form": form}

    return render(request, "web/enquiry.html", context)
