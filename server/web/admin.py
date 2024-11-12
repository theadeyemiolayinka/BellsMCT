import uuid
from django.contrib import admin
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.utils.text import slugify

from unfold.admin import ModelAdmin
from django_ckeditor_5.fields import CKEditor5Field

from .models import Blog


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

admin.site.index_title = 'Welcome to Bells MCT Nexus Admin'

class BlogAdminForm(forms.ModelForm):
    content = CKEditor5Field(config_name='extends')
    
    class Meta:
        model = Blog
        fields = '__all__'

class BlogAdmin(ModelAdmin):
    form = BlogAdminForm

    def is_active(self, obj):
        return obj.deleted_at is None
    is_active.boolean = True
    is_active.short_description = 'Visible'
    
    list_display = ('title', 'author', 'created_at', 'is_active')
    actions = ['hide_blog', 'unhide_blog']
    prepopulated_fields = {"slug": ("title",)}

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields.pop('slug', None)
        form.base_fields.pop('id', None)
        form.base_fields.pop('deleted_at', None)
        return form
    
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.id = uuid.uuid4()
        if not obj.slug:
            def generate_unique_slug(base_slug, num=1):
                slug = f"{base_slug}-{num}" if num > 1 else base_slug
                if Blog.objects.filter(slug=slug).exists():
                    return generate_unique_slug(base_slug, num + 1)
                return slug
            obj.slug = generate_unique_slug(slugify(obj.title))
        super().save_model(request, obj, form, change)

    def hide_blog(self, request, queryset):
        queryset.update(deleted_at=timezone.now())
    hide_blog.short_description = 'Hide selected blogposts'

    def unhide_blog(self, request, queryset):
        queryset.update(deleted_at=None)
    unhide_blog.short_description = 'Unhide selected blogposts'

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(Blog, BlogAdmin)