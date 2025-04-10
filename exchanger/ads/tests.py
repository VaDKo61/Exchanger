from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APITestCase

from ads.models import Ad, ExchangeProposal
from ads.serializers import AdSerializer, ProposalSerializer


def create_superuser(username: str, password: str):
    return User.objects.create_superuser(username=username, password=password)


def create_user(username: str, password: str):
    return User.objects.create_user(username=username, password=password)


def create_ad(data: tuple):
    return Ad.objects.create(title=data[0],
                             description=data[1],
                             category=data[2],
                             condition=data[3],
                             user=data[4])


def create_proposal(data: tuple):
    return ExchangeProposal.objects.create(ad_sender=data[0], ad_receiver=data[1], comment=data[2])


class AdApiTestCase(APITestCase):
    def setUp(self):
        self.admin_user = create_superuser('admin', 'admin')
        self.user_1 = create_user('user_1', 'user')
        self.user_2 = create_user('user_2', 'user')
        self.ad_1 = create_ad(('Test ad 1', 'Test ad 1', '1', 'N', self.admin_user))
        self.ad_2 = create_ad(('Test ad 2', 'Test ad 2', '1', 'N', self.user_1))
        self.ad_3 = create_ad(('Test ad 3', 'Test ad 3', '2', 'U', self.admin_user))
        self.url_list = reverse('ad-list')

    def test_get(self):
        response = self.client.get(self.url_list)
        serialize_data = AdSerializer([self.ad_1, self.ad_2, self.ad_3], many=True).data
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.client.force_login(user=self.user_1)
        response = self.client.get(self.url_list)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialize_data, response.data['results'])

    def test_filter_search(self):
        self.client.force_login(user=self.user_1)
        serialize_data = AdSerializer([self.ad_1, self.ad_2], many=True).data
        response = self.client.get(self.url_list, query_params={'category': '1', 'condition': 'N'})
        self.assertEqual(serialize_data, response.data['results'])

        response = self.client.get(self.url_list, query_params={'search': 'Test ad 3'})
        serialize_data = [AdSerializer(self.ad_3).data]
        self.assertEqual(serialize_data, response.data['results'])

    def test_post_put(self):
        self.client.force_login(user=self.user_2)
        data = {'title': 'Test ad 3',
                'description': 'Test ad 3',
                'category': '3',
                'condition': 'U'}

        response = self.client.post(self.url_list, data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user_2.username, response.data['user_name'])

        data['condition'] = 'N'
        response = self.client.put(self.url_list + str(response.data['id']) + '/', data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data['condition'], response.data['condition'])

        response = self.client.put(self.url_list + str(self.ad_1.id) + '/', data=data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        response = self.client.put(self.url_list + '100/', data=data)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete(self):
        self.client.force_login(user=self.user_1)
        response = self.client.delete(self.url_list + str(self.ad_3.id) + '/')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.delete(self.url_list + str(self.ad_3.id) + '/')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class ProposalApiTestCase(APITestCase):
    def setUp(self):
        self.admin_user = create_superuser('admin', 'admin')
        self.user_1 = create_user('user_1', 'user')
        self.ad_1 = create_ad(('Test ad 1', 'Test ad 1', '1', 'N', self.admin_user))
        self.ad_2 = create_ad(('Test ad 2', 'Test ad 2', '1', 'N', self.user_1))
        self.ad_3 = create_ad(('Test ad 3', 'Test ad 3', '2', 'U', self.admin_user))
        self.proposal_1 = create_proposal((self.ad_1, self.ad_2, 'comment'))
        self.proposal_2 = create_proposal((self.ad_2, self.ad_3, 'comment'))
        self.url_list = reverse('exchangeproposal-list')

    def test_get(self):
        serialize_data = ProposalSerializer([self.proposal_1, self.proposal_2], many=True).data
        response = self.client.get(self.url_list)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialize_data, response.data)

    def test_filter_search(self):
        serialize_data = [ProposalSerializer(self.proposal_1).data]
        response = self.client.get(self.url_list, query_params={'ad_sender': self.proposal_1.ad_sender})
        self.assertEqual(serialize_data, response.data)

        serialize_data = ProposalSerializer([self.proposal_1, self.proposal_2], many=True).data
        response = self.client.get(self.url_list, query_params={'status': 'W'})
        self.assertEqual(serialize_data, response.data)

    def test_post_put(self):
        data = {'ad_sender': self.ad_1,
                'ad_receiver': self.ad_3,
                'comment': 'comment'}

        response = self.client.post(self.url_list, data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.ad_3.id, response.data['ad_receiver'])

        data = {'status': 'A'}
        response = self.client.put(self.url_list + str(response.data['id']) + '/', data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data['status'], response.data['status'])
