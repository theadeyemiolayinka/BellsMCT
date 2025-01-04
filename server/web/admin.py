import uuid
import json
from django.contrib import admin
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.utils.text import slugify
from django.utils.html import format_html

from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget
from django_ckeditor_5.fields import CKEditor5Field

from .models import Blog
from .models import Enquiry
from .models import Event

from django.core.mail import send_mail
from django.conf import settings


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


admin.site.index_title = "Welcome to Bells MCT Nexus Admin"


class BlogAdminForm(forms.ModelForm):
    content = CKEditor5Field(config_name="extends")

    class Meta:
        model = Blog
        fields = "__all__"


class BlogAdmin(ModelAdmin):

    search_fields = ("title", "author", "tags", "content")

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "tags":
            kwargs["widget"] = ArrayWidget(
                attrs={"add_item_text": "Add new tag"},
            )
        return super().formfield_for_dbfield(db_field, **kwargs)

    def is_active(self, obj):
        return obj.hidden_at is None

    is_active.boolean = True
    is_active.short_description = "Visible"

    def get_tags(self, obj):
        return obj.tags.replace(",", ', ') if obj.tags else ''

    get_tags.short_description = "Tags"

    list_filter = ("hidden_at",)

    list_display = ("title", "author", "created_at", "get_tags", "is_active")
    actions = ["hide_blog", "unhide_blog"]
    prepopulated_fields = {"slug": ("title",)}

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields.pop("slug", None)
        form.base_fields.pop("id", None)
        form.base_fields.pop("hidden_at", None)
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
        if obj.tags:
            try:
                obj.tags = ",".join(json.loads(obj.tags.replace("'", '"')))
            except json.JSONDecodeError:
                pass
        super().save_model(request, obj, form, change)

    def hide_blog(self, request, queryset):
        queryset.update(hidden_at=timezone.now())

    hide_blog.short_description = "Hide selected blogposts"

    def unhide_blog(self, request, queryset):
        queryset.update(hidden_at=None)

    unhide_blog.short_description = "Unhide selected blogposts"

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions


class EnquiryAdminForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = "__all__"

class EnquiryAdmin(ModelAdmin):
    form = EnquiryAdminForm

    list_filter = ("status",)
    search_fields = ("name", "email", "subject", "message")

    def get_status(self, obj):
        status_display = dict(Enquiry.STATUS_CHOICES).get(obj.status, "Unknown")
        theme = getattr(settings, 'ADMIN_THEME', 'dark')

        if obj.status == 'resolved':
            color = "green"
            bg_color = "#155724" if theme == 'dark' else "#d4edda"
        elif obj.status == 'in_progress':
            color = "orange"
            bg_color = "#856404" if theme == 'dark' else "#ffeeba"
        elif obj.status == 'closed':
            color = "gray"
            bg_color = "#383d41" if theme == 'dark' else "#e2e3e5"
        else:
            color = "red"
            bg_color = "#721c24" if theme == 'dark' else "#f8d7da"
        return format_html('<span style="color: {}; background-color: {}; padding: 0.25rem 0.5rem; border-radius: 0.5rem; border: 1px solid {};">{}</span>', color, bg_color, color, status_display)


    get_status.short_description = "Status"

    list_display = ("name", "email", "subject", "created_at", "get_status")

    actions = ["mark_as_resolved", "send_email"]

    def mark_as_resolved(self, request, queryset):
        queryset.update(resolved_at=timezone.now())

    mark_as_resolved.short_description = "Mark selected enquiries as resolved"

    def send_email(self, request, queryset):
        for enquiry in queryset:
            send_mail(
                subject=f"Response to your enquiry: {enquiry.subject}",
                message="Thank you for your enquiry. We will get back to you shortly.",
                from_email="admin@bellsmct.com",
                recipient_list=[enquiry.email],
            )

    send_email.short_description = "Send email to selected enquiries"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields.pop("id", None)
        return form

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.id = uuid.uuid4()
        super().save_model(request, obj, form, change)


class EventAdminForm(forms.ModelForm):
    description = CKEditor5Field(config_name="extends")

    class Meta:
        model = Event
        fields = "__all__"

class EventAdmin(ModelAdmin):
    form = EventAdminForm

    search_fields = ("title", "location", "category", "description")
    list_filter = ("category", "start_time", "end_time", "deleted_at")

    def is_active(self, obj):
        return obj.deleted_at is None

    is_active.boolean = True
    is_active.short_description = "Active"

    list_display = ("title", "location", "start_time", "end_time", "category", "is_active")
    actions = ["delete_event", "restore_event"]
    # prepopulated_fields = {"slug": ("title",)}

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields.pop("slug", None)
        form.base_fields.pop("id", None)
        form.base_fields.pop("deleted_at", None)
        return form

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.id = uuid.uuid4()
        super().save_model(request, obj, form, change)

    def delete_event(self, request, queryset):
        queryset.update(deleted_at=timezone.now())

    delete_event.short_description = "Hide selected events"

    def restore_event(self, request, queryset):
        queryset.update(deleted_at=None)

    restore_event.short_description = "Restore selected events"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions



admin.site.register(Event, EventAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Enquiry, EnquiryAdmin)
