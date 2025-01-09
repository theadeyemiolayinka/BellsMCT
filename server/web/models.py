from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

class Blog(models.Model):
    id = models.UUIDField(primary_key=True)
    slug = models.SlugField(unique=True, blank=False, null=False)
    title = models.CharField(max_length=100)
    content = CKEditor5Field(config_name='extends')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/')
    description = models.TextField(blank=True, null=True, max_length=2048)
    tags = models.TextField(blank=True, null=True)
    # tags = models.JSONField(blank=True, null=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hidden_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            def generate_unique_slug(base_slug, num=1):
                slug = f"{base_slug}-{num}" if num > 1 else base_slug
                if Blog.objects.filter(slug=slug).exists():
                    return generate_unique_slug(base_slug, num + 1)
                return slug
            self.slug = generate_unique_slug(slugify(self.title))
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_active_blogs(cls):
        return cls.objects.filter(hidden_at__isnull=True)
    
    @classmethod
    def get_hidden_blogs(cls):
        return cls.objects.filter(hidden_at__isnull=False)
    
    @classmethod
    def get_blog_by_slug(cls, slug):
        return cls.objects.get(slug=slug)
    
    @classmethod
    def get_blog_by_id(cls, id):
        return cls.objects.get(id=id)
    
    @classmethod
    def hide_blog(cls, id):
        blog = cls.get_blog_by_id(id)
        blog.hidden_at = timezone.now()
        blog.save()
        return blog
    
    @classmethod
    def restore_blog(cls, id):
        blog = cls.get_blog_by_id(id)
        blog.hidden_at = None
        blog.save()
        return blog
    

class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.TextField(max_length=100)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Enquiry from {self.name} - {self.subject}"


class Event(models.Model):
    id = models.UUIDField(primary_key=True)
    slug = models.SlugField(unique=True, blank=False, null=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', null=False)
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            def generate_unique_slug(base_slug, num=1):
                slug = f"{base_slug}-{num}" if num > 1 else base_slug
                if Blog.objects.filter(slug=slug).exists():
                    return generate_unique_slug(base_slug, num + 1)
                return slug
            self.slug = generate_unique_slug(slugify(self.title))
        return super().save(*args, **kwargs)