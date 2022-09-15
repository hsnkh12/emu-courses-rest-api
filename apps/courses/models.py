from django.db import models
from ..utils.models import UUIDModel, SlugModel
from django.conf import settings
USER = settings.AUTH_USER_MODEL
from django.core.validators import MaxValueValidator, MinValueValidator


class Department(SlugModel):
    
    name = models.CharField(
        max_length= 70,
        unique=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Course(models.Model):

    department = models.ForeignKey(
        'Department',
        related_name='courses_related',
        on_delete = models.CASCADE
    )
    
    code = models.CharField(
        max_length= 10,
        primary_key=True,
        unique=True
    )

    name = models.CharField(
        max_length= 70,
    )

    credit = models.SmallIntegerField(
        default= 0,
    )

    hours = models.SmallIntegerField(
        default= 1,
    )

    lab = models.SmallIntegerField(
        null = True,
    )

    tutorial = models.SmallIntegerField(
        null = True
    )
        
    def __str__(self):
        return f'{self.code} | {self.name}'


class Rate(models.Model):

    course = models.ForeignKey(
        'course',
        related_name= 'rates_related',
        on_delete= models.CASCADE
    )

    user = models.ForeignKey(
        USER,
        on_delete = models.SET_NULL,
        null = True
    )

    difficulty = models.SmallIntegerField(
        default= 1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )


class Resource(UUIDModel):
    
    user = models.ForeignKey(
        USER,
        related_name= 'resources_related',
        on_delete=models.SET_NULL,
        null = True
    )

    course = models.ForeignKey(
        'Course',
        related_name= 'resources_related',
        on_delete= models.CASCADE
    )

    title = models.CharField(
        max_length= 70
    )

    url = models.URLField()

    description = models.TextField(
        null = True
    )
    
    date_added = models.DateField()

    class Meta:
        verbose_name_plural = 'Resources'
        ordering = ('-date_added',)

    def __str__(self):
        return self.url


class Like(models.Model):

    user = models.ForeignKey(
        USER,
        on_delete=models.SET_NULL,
        null = True
    )

    resource = models.ForeignKey(
        'Resource',
        related_name= 'likes_related',
        on_delete=models.CASCADE
    )

    is_liked = models.BooleanField(
        default= True
    )