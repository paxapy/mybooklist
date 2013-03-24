from django.shortcuts import render, get_object_or_404

from polls.models import Poll


def index(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'latest_poll_list': latest_poll_list})


def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/detail.html', {'poll': poll})


def results(request):
    return render(request)


def vote(request):
    return render(request)