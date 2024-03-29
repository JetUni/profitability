'''Views for the Profit app'''
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from profit.forms import JobForm
from profit.models import Job


@login_required
def add_job(request):
    '''View for adding a job'''
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = JobForm(user=request.user)

    return render(request, 'profit/add_job.html', {'form': form})


@login_required
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
        form = JobForm(instance=job, user=request.user)

    return render(request, 'profit/add_job.html', {'form': form})


@login_required
def delete_jobs(request):
    '''View for deleting jobs'''
    if request.method == 'POST' and request.is_ajax():
        body = request.body.decode()
        ids = body.split(',')
        for pk in ids:
            Job.objects.get(pk=pk).delete()
        return HttpResponse('success')
    return HttpResponse(status_code=400)


def autocomplete_jobs(request):
    '''View for completing jquery automcomplete requests'''
    if request.method == 'GET' and request.is_ajax():
        name = request.GET['name']
        if name == '':
            return JsonResponse([], safe=False)
        data = Job.objects.filter(
            Q(name__icontains=name) | Q(name__istartswith=name),
        ).values_list('name', flat=True)
        json = []
        for name in data:
            if name not in json:
                json.append(name)
        return JsonResponse(json, safe=False)
    return HttpResponse(status_code=400)


def index(request):
    '''View for displaying a table of jobs'''
    user = request.user
    if user.is_authenticated:
        companies = user.profile.companies.values_list('id', flat=True)
        jobs = Job.objects.filter(company__pk__in=list(companies))
    else:
        jobs = Job.objects.all()
    return render(request, 'profit/index.html', {'jobs': jobs})
