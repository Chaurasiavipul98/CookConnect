from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to='profiles/', default='profiles/default.jpg')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True, default='')
    website = models.URLField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, default='N')
    
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    joined_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

    def total_followers(self):
        return self.followers.count()

    def total_following(self):
        return self.following.count()

    def profile_completion(self):
        fields = [self.bio, self.profile_pic, self.location, self.website, self.dob, self.gender]
        filled = sum(bool(f) for f in fields)
        return int((filled / len(fields)) * 100)
    

class Recipe(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    description = models.TextField()
    ingredients = models.TextField()
    steps = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_recipes', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} on {self.recipe.title}"
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject[:20]}"