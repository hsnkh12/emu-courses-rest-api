from django.db import models
from ..utils.models import UUIDModel, SlugModel
from django.conf import settings
USER = settings.AUTH_USER_MODEL
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

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

    @property
    def difficulty_rate(self):
        
        rates = self.rates_related

        if not rates.exists():
            return None
            
        difficulty_sum = rates.aggregate(Sum('difficulty'))['difficulty__sum']
        count = rates.count()
        return {'avg':round(difficulty_sum/count, 2),'count':count}
        
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
        related_name= 'rates_related',
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

    likes_count = models.IntegerField(
        default=0
    )

    # @property
    # def likes_count(self):
    #     all_likes = self.likes_related
    #     return all_likes.filter(is_liked=True).count() - all_likes.filter(is_liked=False).count()

    class Meta:
        verbose_name_plural = 'Resources'
        ordering = ('-date_added',)

    def __str__(self):
        return self.id


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



@receiver(post_save, sender=Like)
def update_like_count_on_create(sender, instance=None, created=False, **kwargs):
    if created:
        resource = Resource.objects.get(id = instance.resource_id)

        if instance.is_liked:
            resource.likes_count +=1
        else:
            resource.likes_count -=1

        resource.save()

@receiver(post_delete, sender=Like)
def update_like_count_on_delete(sender, instance=None, **kwargs):
    
    resource = Resource.objects.get(id = instance.resource_id)

    if instance.is_liked:
        resource.likes_count -=1
    else:
        resource.likes_count +=1

    resource.save()