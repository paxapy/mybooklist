from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView

from polls.models import Poll, Choice


class Index(ListView):
    queryset = Poll.objects.order_by()[:5]


class Detail(DetailView):
    model = Poll


class Results(DetailView):
    model = Poll
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