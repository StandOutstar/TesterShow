from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic

from jobs.models import Job


# Create your views here.
# def index(request):
#     # return HttpResponse("Hello world. You're at the task index.")
#     latest_task_list = Job.objects.order_by('-finish_date')[:5]
#     # template = loader.get_template('jobs/index.html')
#     context = {
#         'latest_task_list': latest_task_list,
#     }
#     # output = ',<br>'.join([j.name for j in latest_task_list])
#     # return HttpResponse(template.render(context, request))
#     return render(request, 'jobs/index.html', context)
#
#
# def detail(request, task_id):
#     # try:
#     #     job = Job.objects.get(id=task_id)
#     # except Job.DoesNotExist:
#     #     raise Http404("Job does not exist")
#
#     job = get_object_or_404(Job, id=task_id)
#
#     # response = "You're looking at task %s"
#     # return HttpResponse(response % task_id)
#     return render(request, 'jobs/detail.html', context={'job': job})

# 类视图 通用视图
class IndexView(generic.ListView):
    template_name = 'jobs/index.html'
    context_object_name = 'latest_job_list'

    def get_queryset(self):
        # return Job.objects.order_by('-finish_date')[:5]

        return Job.objects.filter(
            finish_date__lte=timezone.now()
        ).order_by('-finish_date')[:5]


class DetailView(generic.DetailView):
    model = Job
    template_name = 'jobs/detail.html'

    def get_queryset(self):
        return Job.objects.filter(finish_date__lte=timezone.now())