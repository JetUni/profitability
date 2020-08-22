'''Views for the Profit app'''
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import AddJobForm
from .models import Job


def add_job(request):
    '''View for adding a job'''
    if request.method == 'POST':
        form = AddJobForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = AddJobForm()

    return render(request, 'profit/add_job.html', {'form': form})


def edit_job(request, pk):
    '''View for editing a job'''
    if request.method == 'POST':
        form = AddJobForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        job = Job.objects.get(pk=pk)
        form = AddJobForm(instance=job)

    return render(request, 'profit/add_job.html', {'form': form})


def index(request):
    '''View for displaying a table of jobs'''
    jobs = Job.objects.all()
    return render(request, 'profit/index.html', {'jobs': jobs})
