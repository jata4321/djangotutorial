from django.db import models

# Create your models here.

class User(models.Model):

    def __str__(self):
        return self.username

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    date_of_birth = models.DateField

class Profile(models.Model):

    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    bio = models.TextField()
    location = models.CharField(max_length=200)
    birth_date = models.DateField
    profile_picture = models.ImageField(upload_to='profile_pictures')
    followers = models.ManyToManyField(User, related_name='followers')
    following = models.ManyToManyField(User, related_name='following')
    # posts = models.ManyToManyField('Post', related_name='posts')