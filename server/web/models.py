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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title + ' - ' + self.author.username
    
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
        return cls.objects.filter(deleted_at__isnull=True)
    
    @classmethod
    def get_deleted_blogs(cls):
        return cls.objects.filter(deleted_at__isnull=False)
    
    @classmethod
    def get_blog_by_slug(cls, slug):
        return cls.objects.get(slug=slug)
    
    @classmethod
    def get_blog_by_id(cls, id):
        return cls.objects.get(id=id)
    
    @classmethod
    def delete_blog(cls, id):
        blog = cls.get_blog_by_id(id)
        blog.deleted_at = timezone.now()
        blog.save()
        return blog
    
    @classmethod
    def restore_blog(cls, id):
        blog = cls.get_blog_by_id(id)
        blog.deleted_at = None
        blog.save()
        return blog