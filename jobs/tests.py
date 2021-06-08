import datetime

from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.utils import timezone

from jobs.models import Job


class JobModelTests(TestCase):

    def test_was_finished_recently_with_future_job(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_job = Job(finish_date=time)
        self.assertIs(future_job.was_finished_recently(), False)

    def test_was_finished_recently_with_old_job(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_job = Job(finish_date=time)
        self.assertIs(old_job.was_finished_recently(), False)

    def test_was_finished_recently_with_recent_job(self):
        time = timezone.now() - datetime.timedelta(hours=23,minutes=59, seconds=59)
        recent_job = Job(finish_date=time)
        self.assertIs(recent_job.was_finished_recently(), True)


def create_job(job_name, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Job.objects.create(name=job_name, finish_date=time)


class JobIndexViewTests(TestCase):
    EMPTY_TEXT = "No jobs are available"

    def test_no_jobs(self):
        response = self.client.get(reverse('jobs:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.EMPTY_TEXT)
        self.assertQuerysetEqual(response.context['latest_job_list'], [])

    def test_past_job(self):
        job = create_job('old_job', days=-30)
        response = self.client.get(reverse('jobs:index'))

        self.assertQuerysetEqual(
            response.context['latest_job_list'],
            [job]
        )

    def test_future_job(self):
        job = create_job('future_job', days=30)
        response = self.client.get(reverse('jobs:index'))

        self.assertContains(response, self.EMPTY_TEXT)
        self.assertQuerysetEqual(
            response.context['latest_job_list'],
            []
        )

    def test_future_and_old_job(self):
        future_job = create_job('future_job', days=30)
        old_job = create_job('old_job', days=-30)
        response = self.client.get(reverse('jobs:index'))

        self.assertQuerysetEqual(
            response.context['latest_job_list'],
            [old_job]
        )

    def test_two_old_job(self):
        old_job_1 = create_job('old_job_1', days=-30)
        old_job_2 = create_job('old_job_2', days=-5)
        response = self.client.get(reverse('jobs:index'))

        self.assertQuerysetEqual(
            response.context['latest_job_list'],
            [old_job_2, old_job_1]  # 顺序是后创建的在前
        )


class JobDetailViewTests(TestCase):

    def test_future_job(self):
        job = create_job('future_job', days=30)
        response = self.client.get(reverse('jobs:detail', args=(job.id,)))

        self.assertEqual(response.status_code, 404)

    def test_past_job(self):
        job = create_job('old_job', days=-30)
        response = self.client.get(reverse('jobs:detail', args=(job.id,)))

        self.assertContains(
            response,
            job.name
        )