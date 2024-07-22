from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import forms
from .models import *


class UserAdmin(BaseUserAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:40px; max-height:40px"/>'.format(obj.user_avatar.url))

    image_tag.short_description = 'user_avatar'
    fieldsets = (
        (None, {'fields': ('email', 'password', 'user_avatar',
                           'last_login', 'username', 'first_name', 'last_name', 'phone'
                           )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'username', 'phone', 'image_tag', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('is_active',)


# Register your models here.
class EduSolutionsAdmin(admin.ModelAdmin):
    def itemnames(self, obj):
        return format_html('<p>{}</p>'.format(obj.itemname))

    itemnames.short_description = 'Programs'
    itemnames.allow_tags = True

    def was_published_recently(self, obj):
        parks = obj.created_on >= timezone.now() - timedelta(days=1)
        return format_html('<p>{}</p>'.format(parks))
        # self.created_on >= timezone.now() - datetime.timedelta(days=1)

    list_display = ['itemnames', 'was_published_recently', 'created_by']
    list_filter = ('itemname', 'created_on')
    search_fields = ('itemname',)
    ordering = ('itemname', 'created_on', 'created_by')


class ICTSolutionsAdmin(admin.ModelAdmin):

    def itemnames(self, obj):
        return format_html('<p>{}</p>'.format(obj.itemname))

    itemnames.short_description = 'Programs'
    itemnames.allow_tags = True

    def was_published_recently(self, obj):
        parks = obj.created_on >= timezone.now() - timedelta(days=1)
        return format_html('<p>{}</p>'.format(parks))
        # self.created_on >= timezone.now() - datetime.timedelta(days=1)

    list_display = ['itemnames', 'was_published_recently', 'created_by']
    list_filter = ('itemname', 'created_on')
    search_fields = ('itemname',)
    ordering = ('itemname', 'created_on', 'created_by')


class MediaSolutionsAdmin(admin.ModelAdmin):

    def itemnames(self, obj):
        return format_html('<p>{}</p>'.format(obj.itemname))

    itemnames.short_description = 'Programs'
    itemnames.allow_tags = True

    def was_published_recently(self, obj):
        parks = obj.created_on >= timezone.now() - timedelta(days=1)
        return format_html('<p>{}</p>'.format(parks))
        # self.created_on >= timezone.now() - datetime.timedelta(days=1)

    list_display = ['itemnames', 'was_published_recently', 'created_by']
    list_filter = ('itemname', 'created_on')
    search_fields = ('itemname',)
    ordering = ('itemname', 'created_on', 'created_by')


class ConsultancyServicesAdmin(admin.ModelAdmin):

    def itemnames(self, obj):
        return format_html('<p>{}</p>'.format(obj.itemname))

    itemnames.short_description = 'Programs'
    itemnames.allow_tags = True

    def was_published_recently(self, obj):
        parks = obj.created_on >= timezone.now() - timedelta(days=1)
        return format_html('<p>{}</p>'.format(parks))
        # self.created_on >= timezone.now() - datetime.timedelta(days=1)

    list_display = ['itemnames', 'was_published_recently', 'created_by']
    list_filter = ('itemname', 'created_on')
    search_fields = ('itemname',)
    ordering = ('itemname', 'created_on', 'created_by')


class ElectronicsSolutionsAdmin(admin.ModelAdmin):

    def itemnames(self, obj):
        return format_html('<p>{}</p>'.format(obj.itemname))

    itemnames.short_description = 'Programs'
    itemnames.allow_tags = True

    def was_published_recently(self, obj):
        parks = obj.created_on >= timezone.now() - timedelta(days=1)
        return format_html('<p>{}</p>'.format(parks))
        # self.created_on >= timezone.now() - datetime.timedelta(days=1)

    list_display = ['itemnames', 'was_published_recently', 'created_by']
    list_filter = ('itemname', 'created_on')
    search_fields = ('itemname',)
    ordering = ('itemname', 'created_on', 'created_by')


class AboutAdmin(admin.ModelAdmin):

    def itemnames(self, obj):
        return format_html('<p>{}</p>'.format(obj.itemname))

    itemnames.short_description = 'Programs'
    itemnames.allow_tags = True

    def was_published_recently(self, obj):
        parks = obj.created_on >= timezone.now() - timedelta(days=1)
        return format_html('<p>{}</p>'.format(parks))
        # self.created_on >= timezone.now() - datetime.timedelta(days=1)

    list_display = ['itemnames', 'was_published_recently', 'created_by']
    list_filter = ('itemname', 'created_on')
    search_fields = ('itemname',)
    ordering = ('itemname', 'created_on', 'created_by')


class EduSolutionsoverviewAdmin(admin.ModelAdmin):
    def overviews(self, obj):
        return format_html('<p>{}</p>'.format(obj.overview))

    overviews.short_description = 'Programs'
    overviews.allow_tags = True

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:400px; max-height:400px"/>'.format(obj.itemimage.url))

    overviews.short_description = 'Programs'

    def was_published_recently(self, obj):
        parks = obj.created_on >= timezone.now() - timedelta(days=1)
        return format_html('<p>{}</p>'.format(parks))

    list_display = ['overviews', 'image_tag']


class MediaSolutionsoverviewAdmin(admin.ModelAdmin):
    list_display = ['overview', 'itemimage']


class ConsultancyServicesoverviewAdmin(admin.ModelAdmin):
    list_display = ['overview', 'itemimage']


class ICTSolutionsoverviewAdmin(admin.ModelAdmin):
    list_display = ['overview', 'itemimage']


class IndustriesAdmin(admin.ModelAdmin):

    def itemnames(self, obj):
        return format_html('<p>{}</p>'.format(obj.itemname))

    itemnames.short_description = 'Programs'
    itemnames.allow_tags = True

    def was_published_recently(self, obj):
        parks = obj.created_on >= timezone.now() - timedelta(days=1)
        return format_html('<p>{}</p>'.format(parks))
        # self.created_on >= timezone.now() - datetime.timedelta(days=1)

    list_display = ['itemnames', 'was_published_recently', 'created_by']
    list_filter = ('itemname', 'created_on')
    search_fields = ('itemname',)
    ordering = ('itemname', 'created_on', 'created_by')


class IndustriesoverviewAdmin(admin.ModelAdmin):
    list_display = ['overview', 'itemimage']


class AboutoverviewAdmin(admin.ModelAdmin):
    list_display = ['overview', 'itemimage']


class InnovationoverviewAdmin(admin.ModelAdmin):
    list_display = ['overview', 'itemimage']


class InnovationAdmin(admin.ModelAdmin):

    def itemnames(self, obj):
        return format_html('<p>{}</p>'.format(obj.itemname))

    itemnames.short_description = 'Programs'
    itemnames.allow_tags = True

    def was_published_recently(self, obj):
        parks = obj.created_on >= timezone.now() - timedelta(days=1)
        return format_html('<p>{}</p>'.format(parks))
        # self.created_on >= timezone.now() - datetime.timedelta(days=1)

    list_display = ['itemnames', 'was_published_recently', 'created_by']
    list_filter = ('itemname', 'created_on')
    search_fields = ('itemname',)
    ordering = ('itemname', 'created_on', 'created_by')


class InvestorRelationsAdmin(admin.ModelAdmin):

    def itemnames(self, obj):
        return format_html('<p>{}</p>'.format(obj.itemname))

    itemnames.short_description = 'Programs'
    itemnames.allow_tags = True

    def was_published_recently(self, obj):
        parks = obj.created_on >= timezone.now() - timedelta(days=1)
        return format_html('<p>{}</p>'.format(parks))
        # self.created_on >= timezone.now() - datetime.timedelta(days=1)

    list_display = ['itemnames', 'was_published_recently', 'created_by']
    list_filter = ('itemname', 'created_on')
    search_fields = ('itemname',)
    ordering = ('itemname', 'created_on', 'created_by')


class CareersAdmin(admin.ModelAdmin):

    def itemnames(self, obj):
        return format_html('<p>{}</p>'.format(obj.itemname))

    itemnames.short_description = 'Programs'
    itemnames.allow_tags = True

    def was_published_recently(self, obj):
        parks = obj.created_on >= timezone.now() - timedelta(days=1)
        return format_html('<p>{}</p>'.format(parks))
        # self.created_on >= timezone.now() - datetime.timedelta(days=1)

    list_display = ['itemnames', 'was_published_recently', 'created_by']
    list_filter = ('itemname', 'created_on')
    search_fields = ('itemname',)
    ordering = ('itemname', 'created_on', 'created_by')


class InvestorRelationsoverviewAdmin(admin.ModelAdmin):
    list_display = ['overview', 'itemimage']


class CareersoverviewAdmin(admin.ModelAdmin):
    list_display = ['overview', 'itemimage']


class FeedbackAdmin(admin.ModelAdmin):

    def itemnames(self, obj):
        return format_html('<p>{}</p>'.format(obj.itemname))

    itemnames.short_description = 'Programs'
    itemnames.allow_tags = True

    def was_published_recently(self, obj):
        parks = obj.created_on >= timezone.now() - timedelta(days=1)
        return format_html('<p>{}</p>'.format(parks))
        # self.created_on >= timezone.now() - datetime.timedelta(days=1)

    list_display = ['itemnames', 'was_published_recently', 'created_by']
    list_filter = ('itemname', 'created_on')
    search_fields = ('itemname',)
    ordering = ('itemname', 'created_on', 'created_by')


# class ContactUsAdmin(admin.ModelAdmin):
#
#     def itemnames(self, obj):
#         return format_html('<p>{}</p>'.format(obj.itemname))
#
#     itemnames.short_description = 'Programs'
#     itemnames.allow_tags = True
#
#     def was_published_recently(self, obj):
#         parks = obj.created_on >= timezone.now() - timedelta(days=1)
#         return format_html('<p>{}</p>'.format(parks))
#         # self.created_on >= timezone.now() - datetime.timedelta(days=1)
#
#     list_display = ['itemnames', 'was_published_recently', 'created_by']
#     list_filter = ('itemname', 'created_on')
#     search_fields = ('itemname',)
#     ordering = ('itemname', 'created_on', 'created_by')


class ContactUsOverViewAdmin(admin.ModelAdmin):
    list_display = ['overview', 'itemimage']


#
# class ApplicationsAdmin(admin.ModelAdmin):
#     list_display = ["name", "image", "country", "city", "Job",
#                     "status"]
#     list_filter = ('Job', 'user__username', 'user__last_name', 'user__first_name')
#     search_fields = ('status', 'user__username', 'user__last_name', 'user__first_name')
#
#     ordering = ('Job', 'user')

# class Applications_ApprovalAdmin(admin.ModelAdmin):
#

# admin.site.register(Applications_Approval, ApplicationsApprovalAdmin)

class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('user', 'Job', 'status', 'date_created')
    list_filter = ('status', 'country', 'city', 'Job')
    search_fields = ('user__first_name', 'user__last_name', 'Job__title')
    ordering = ('Job', 'user')


#
# admin.site.register(Applications, ApplicationsAdmin)

# class SolutionsGeneralOverViewAdmin(admin.ModelAdmin):
#     list_display = ['overview', 'itemimage']


admin.site.register(Job)
# admin.site.register(JobSubcategory)
admin.site.register(JobCategory)
admin.site.register(Country)

admin.site.register(Applications, ApplicationsAdmin)
admin.site.register(City)
admin.site.register(Subscriber)

admin.site.register(EduSolutions, EduSolutionsAdmin)
admin.site.register(ICTSolutions, ICTSolutionsAdmin)
admin.site.register(MediaSolutions, MediaSolutionsAdmin)
admin.site.register(ConsultancyServices, ConsultancyServicesAdmin)
admin.site.register(ElectronicsSolutions, ElectronicsSolutionsAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(EduSolutionsoverview, EduSolutionsoverviewAdmin)
admin.site.register(MediaSolutionsoverview, MediaSolutionsoverviewAdmin)

admin.site.register(ConsultancyServicesoverview, ConsultancyServicesoverviewAdmin)
admin.site.register(ICTSolutionsoverview, ICTSolutionsoverviewAdmin)
admin.site.register(Industries, IndustriesAdmin)
admin.site.register(Industriesoverview, IndustriesoverviewAdmin)
admin.site.register(Aboutoverview, AboutoverviewAdmin)
admin.site.register(Innovationoverview, InnovationoverviewAdmin)
admin.site.register(Innovation, InnovationAdmin)
admin.site.register(InvestorRelations, InvestorRelationsAdmin)
admin.site.register(Careers, CareersAdmin)
admin.site.register(InvestorRelationsoverview, InvestorRelationsoverviewAdmin)
admin.site.register(Careersoverview, CareersoverviewAdmin)
# admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(ContactUsOverView, ContactUsOverViewAdmin)
# admin.site.register(SolutionsGeneralOverView, SolutionsGeneralOverViewAdmin)
# admin.site.register(Course, TranslatableAdmin)
admin.site.register(User, UserAdmin)


# admin.site.register(BlogSection1)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


    list_display = ('title', 'category', 'publish_date')
    search_fields = ('title', 'summary', 'content')
    list_filter = ('category', 'publish_date')


class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the queryset to staff users only
        self.fields['user'].queryset = User.objects.filter(is_staff=True)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm
    # other admin customization goes here...


admin.site.register(Applications_Approval, )
admin.site.register(Category, admin.ModelAdmin)
admin.site.register(indexbottom)
admin.site.register(indexmiddlebottom1)
admin.site.register(indexmiddlebottom2)
admin.site.register(indexmiddlebottom3)
admin.site.register(indexmiddlevideo)
admin.site.register(indexmiddlebottom4)

