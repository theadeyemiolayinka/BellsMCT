from django.http import HttpResponse
from django.shortcuts import render
from django_bunny.storage import BunnyStorage

def index(request):
    def list_files_in_bunnycdn():
        files = BunnyStorage().listdir('/')
        return files

    files = list_files_in_bunnycdn()
    return HttpResponse(files.__str__())
    # return render(request, 'web/index.html')
