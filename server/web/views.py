import json
import random
from django.http import HttpResponse, JsonResponse

# from django.shortcuts import render
from django_bunny.storage import BunnyStorage

from django.contrib.auth.models import User
from .models import Event


def index(request):
    def list_files_in_bunnycdn():
        files = BunnyStorage().listdir("/")
        return files

    files = list_files_in_bunnycdn()
    return HttpResponse(files.__str__())
    # return render(request, 'web/index.html')


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


def events_json(request):
    events = Event.objects.filter(deleted_at__isnull=True)
    data = [
        {
            "id": str(event.id),
            "title": event.title,
            "start": event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end": None if event.start_time.strftime("%Y-%m-%d %H:%M:%S") == event.end_time.strftime("%Y-%m-%d %H:%M:%S") else event.end_time.strftime("%Y-%m-%d %H:%M:%S"), 
            "url": f"/admin/web/event/{event.id}/change/",
        }
        for event in events
    ]
    return JsonResponse(data, safe=False)
