from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image

from itology.config import ACCOUNT_TYPE, USER_TYPE


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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        ordering = ['title']


class Subsection(models.Model, AbstractMixin):
    title = models.CharField(max_length=128, unique=True, help_text='Name of IT specialization')
    section = models.ForeignKey('Section', verbose_name='section', on_delete=models.CASCADE,
                                related_name='subsection', help_text='Name of type of IT specialization')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Subsection {self.title} from section {self.section.title}'

    class Meta:
        verbose_name = 'Subsection'
        verbose_name_plural = 'Subsections'
        ordering = ['title']


class Comment(models.Model, AbstractMixin):
    comment = models.CharField(max_length=128, unique=True, help_text='Comment text')
    parent = models.ForeignKey(
        'self', verbose_name='parent', on_delete=models.CASCADE, null=True, related_name='children'
    )
    creator = models.ForeignKey('Client', verbose_name='user', on_delete=models.CASCADE,
                                related_name='comment', help_text='The user who left the comment')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment "{self.comment}" from user {self.creator.username}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_at']


class Client(models.Model, AbstractMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user', related_name='client')
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE, help_text='User account type')
    user_type = models.CharField(max_length=10, choices=USER_TYPE, help_text='User type in the system')
    avatar = models.ImageField(default='images/default_avatar.png', upload_to='profile_images')

    role = models.ManyToManyField('Role', verbose_name='role', related_name='client',
                                  help_text='The role of an expert in a project')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['user']


class Team(models.Model):
    role = models.ForeignKey('Role', verbose_name='role', on_delete=models.CASCADE,
                             related_name='team', help_text='The role of an expert in a project')
    advert = models.ForeignKey('Advert', verbose_name='advert', on_delete=models.CASCADE,
                               related_name='team', help_text='Advert of the desired IT product')
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
    classify = models.BooleanField(help_text='Flag of expert evaluation of the division of the team into roles')
    sole_execution = models.BooleanField(help_text='Single project flag')

    creator = models.ForeignKey('Client', verbose_name='user', on_delete=models.CASCADE,
                                related_name='advert', help_text='Advert author')
    comment = models.ManyToManyField('Comment', verbose_name='comment', related_name='advert',
                                     help_text='Advert comment')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Advert'
        verbose_name_plural = 'Adverts'
        ordering = ['created_at']
