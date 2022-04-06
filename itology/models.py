from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image

from itology.config import ACCOUNT_TYPE, SIZE_IMAGE, USER_TYPE


class AbstractMixin:
    @classmethod
    def get_all(cls):
        return cls.objects.all()


class Role(models.Model, AbstractMixin):
    title = models.CharField(max_length=128, unique=True, help_text='The role of an expert in a project')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['title']


class Section(models.Model, AbstractMixin):
    title = models.CharField(max_length=128, unique=True, help_text='Name of IT specialization')
    parent = models.ForeignKey('self', verbose_name='parent', on_delete=models.CASCADE, related_name='children',
                               null=True, help_text='Name of type of IT specialization')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_adverts_amount(self):
        return sum(len(set(ch.adverts.filter(in_developing=False))) for ch in self.children.all())

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        ordering = ['title']


class Comment(models.Model, AbstractMixin):
    content = models.CharField(max_length=128, unique=True, help_text='Comment text')
    author = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE,
                               related_name='comments', help_text='The user who left the comment')
    advert = models.ForeignKey('Advert', verbose_name='advert', on_delete=models.CASCADE, related_name='comments',
                               help_text='Advert to which the comment was written')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment "{self.content}" from user {self.author.username}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_at']


class Client(models.Model, AbstractMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user', related_name='client')
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE, help_text='User account type')
    user_type = models.CharField(max_length=10, choices=USER_TYPE, help_text='User type in the system')
    avatar = models.ImageField(default='images/avatar.jpg', upload_to='profile_images')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > SIZE_IMAGE or img.width > SIZE_IMAGE:
            img.thumbnail((SIZE_IMAGE, SIZE_IMAGE))
            img.save(self.avatar.path)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['user']


class Team(models.Model, AbstractMixin):
    role = models.ForeignKey('Role', verbose_name='role', on_delete=models.CASCADE,
                             related_name='team', help_text='The role of an expert in a project')
    advert = models.ForeignKey('Advert', verbose_name='advert', on_delete=models.CASCADE,
                               related_name='teams', help_text='Advert of the desired IT product')
    members = models.ManyToManyField(User, verbose_name='members', related_name='team', help_text='Team members')
    amount = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)],
                                 help_text='Number of people in this role on the project')

    def __str__(self):
        return f'Team of {self.advert.title}'

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['amount']


class Advert(models.Model, AbstractMixin):
    title = models.CharField(max_length=128, help_text='Advert of the desired IT product')
    description = models.TextField(help_text='Description of the desired IT product')
    classify = models.BooleanField(default=False, null=True, blank=True,
                                   help_text='Flag of expert evaluation of the division of the team into roles')
    sole_execution = models.BooleanField(default=False, null=True, blank=True, help_text='Single project flag')
    in_developing = models.BooleanField(default=False, null=True, blank=True, help_text='Project stage flag')

    creator = models.ForeignKey(User, verbose_name='creator', on_delete=models.CASCADE,
                                related_name='adverts', help_text='Advert author')
    sections = models.ManyToManyField('Section', verbose_name='sections', related_name='adverts',
                                      help_text='Advert sections')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Advert'
        verbose_name_plural = 'Adverts'
        ordering = ['created_at']
