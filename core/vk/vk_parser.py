from datetime import datetime

import vk
from decouple import config
from core.models import VKGroup, VKPost, VKSource
import logging

from django.db import IntegrityError

logger = logging.getLogger(__name__)


class VKParser:
    def __init__(self):
        self.session = vk.Session()
        self.api = vk.API(self.session)
        self.ACCESS_TOKEN = config('ACCESS_TOKEN')

    def parse_group(self, vk_id):
        response = self.api.groups.getById(access_token=self.ACCESS_TOKEN, v='5.81',
                                           lang='ru', group_ids=vk_id,
                                           fields='description,members_count,verified,site,cover')
        response = response[0]
        try:
            group = VKGroup.objects.get(vk_id=response['id'])
            group.name = response['name']
            group.vk_id = response['id']
            group.description = response['description']
            group.members_count = response['members_count']
            group.verified = response['verified']
            group.site = response['site']
            group.photo_100 = response['photo_100']
        except VKGroup.DoesNotExist:
            group = VKGroup.objects.create(name=response['name'],
                                           vk_id=response['id'],
                                           description=response['description'],
                                           members_count=response['members_count'],
                                           verified=response['verified'],
                                           site=response['site'],
                                           photo_100=response['photo_100'])
        group.save()
        logger.info(f'Info about {group.name} has been updated successfully')
        return group

    def parse_posts(self, source_id):
        response = self.api.wall.get(access_token=self.ACCESS_TOKEN, v='5.81', filter='owner', extended='1',
                                     lang='ru', owner_id=f'-{source_id}', count=50)

        posts = response['items']
        for post in posts:
            try:
                post = VKPost.objects.get(id=post['id'])
            except VKPost.DoesNotExist:
                try:
                    new_post = VKPost(
                        id=post['id'],
                        owner=VKGroup.objects.get(vk_id=abs(post['owner_id'])),
                        pub_date=datetime.fromtimestamp(post['date']),
                        text=post['text'],
                        comments=post['comments']['count'],
                        likes=post['likes']['count'],
                        reposts=post['reposts']['count'],
                        checked=False
                    )
                    new_post.save()
                    logger.info(f'VK post by {new_post.owner} from {post["date"]} has been saved')
                except IntegrityError:
                    pass

    def parse_groups(self):
        groups = VKSource.objects.values('vk_id').all()
        # iterating sources
        for group in groups:
            # updating group info
            updated = self.parse_group(group['vk_id'])
            # updating posts
            self.parse_posts(updated.vk_id)
