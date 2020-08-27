'''Views for the Profit app'''
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import JobForm
from .models import Job


def add_job(request):
    '''View for adding a job'''
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = JobForm()

    return render(request, 'profit/add_job.html', {'form': form})


def edit_job(request, pk):
    '''View for editing a job'''
    if request.method == 'POST':
        instance = get_object_or_404(Job, pk=pk)
        form = JobForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        job = Job.objects.get(pk=pk)
        form = JobForm(instance=job)

    return render(request, 'profit/add_job.html', {'form': form})


def delete_jobs(request):
    '''View for deleting jobs'''
    if request.method == 'POST' and request.is_ajax():
        body = request.body.decode()
        ids = body.split(',')
        for pk in ids:
            Job.objects.get(pk=pk).delete()
        return HttpResponse('success')
    return HttpResponse(status_code=400)


def index(request):
    '''View for displaying a table of jobs'''
    jobs = Job.objects.all()
    return render(request, 'profit/index.html', {'jobs': jobs})
