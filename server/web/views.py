from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render
from django_bunny.storage import BunnyStorage

from .models import Event

def index(request):
    def list_files_in_bunnycdn():
        files = BunnyStorage().listdir('/')
        return files

    files = list_files_in_bunnycdn()
    return HttpResponse(files.__str__())
    # return render(request, 'web/index.html')


def dashboard_callback(request, context):
    context.update(
        {
            "chart": {
                "headers": ["col 1", "col 2"],
                "rows": [
                    ["a", "b"],
                    ["c", "d"],
                ],
            }
        }
    )
    return context


def events_json(request):
    events = Event.objects.filter(deleted_at__isnull=True)
    data = [
        {
            "id": str(event.id),
            "title": event.title,
            "start": event.start_time.strftime("%Y-%m-%d"),
            "end": event.end_time.strftime("%Y-%m-%d"),
            "url": f"/admin/web/event/{event.id}/change/"
        }
        for event in events
    ]
    return JsonResponse(data, safe=False)