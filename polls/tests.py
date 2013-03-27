import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

from polls.models import Poll


class PollMethodTests(TestCase):

    def test_was_published_recently_with_future_poll(self):
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=30))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)

def create_poll(question, days):
    return Poll.objects.create(question=question,
                               pub_date=timezone.now() + datetime.timedelta(days=days))

class PollViewTests(TestCase):
    def test_index_view_with_no_polls(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['poll_list'], [])

    def test_index_view_with_a_past_poll(self):
        poll = create_poll(question="Past poll.", days=-30)
        response = self.client.get(reverse('polls:index'))
        print(response.context['poll_list'][0])
        self.assertEqual(response.context['poll_list'][0], poll)

    def test_index_view_with_a_future_poll(self):
        create_poll(question="Future poll.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.", status_code=200)
        self.assertQuerysetEqual(response.context['poll_list'], [])

    def test_index_view_with_future_poll_and_past_poll(self):
        past_poll = create_poll(question="Past poll.", days=-30)
        future_poll = create_poll(question="Future poll.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.context['poll_list'][0], past_poll)

    def test_index_view_with_two_past_polls(self):
        poll1 = create_poll(question="Past poll 1.", days=-30)
        poll2 = create_poll(question="Past poll 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(list(response.context['poll_list']), [poll2, poll1])