from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import AddJobForm
from .models import Job


def add_job(request):
    if request.method == 'POST':
        form = AddJobForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = AddJobForm()

    return render(request, 'profit/add_job.html', {'form': form})


def index(request):
    jobs = Job.objects.all()
    return render(request, 'profit/index.html', {'jobs': jobs})
