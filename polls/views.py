from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView
from django.utils import timezone

from polls.models import Poll, Choice


class PollMixin(object):
    queryset = Poll.objects.filter(pub_date__lte=timezone.now())
    model = Poll


class Index(PollMixin, ListView):

    def get_queryset(self):
        return self.queryset.order_by('-pub_date')[:5]


class Detail(PollMixin, DetailView):
    pass


class Results(PollMixin, DetailView):
    template_name = 'polls/results.html'


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/poll_detail.html', {'poll': p, 'error_message': "You didn't select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect(reverse('polls:results', args=(p.pk,)))