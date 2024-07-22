from datetime import timedelta, date

from django.core.exceptions import ValidationError
from django.db.models.functions import datetime
from django.utils import timezone
from django.db import models
# from ckeditor.fields import CKEditor5Field
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.humanize.templatetags import humanize
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


# Create your models here.
class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), max_length=254, unique=True)
    username = models.CharField(_('username'), max_length=254, null=True, blank=True)
    last_name = models.CharField(_('last_name'), max_length=254, null=True, blank=True)
    first_name = models.CharField(_('first_name'), max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_superuser = models.BooleanField(_('is_superuser'), default=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    address = models.CharField(_('address'), max_length=50, null=True)
    phone = models.IntegerField(_('address'), null=True)
    last_login = models.DateTimeField(_('last_login'), null=True, blank=True)
    date_joined = models.DateTimeField(_('date_joined'), auto_now_add=True)
    birthdate = models.DateTimeField(null=True, blank=True)
    user_avatar = models.FileField(_('user_avatar'), default='media/default.jpg', upload_to='profile_photos', null=True)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    @property
    def age(self):
        # age = date.today()-self.birthdate
        today = date.today()
        dob = self.birthdate
        return int(today.year - dob.year)

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def get_date(self):
        return humanize.naturaltime(self.date_joined)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name_plural = 'Users'


class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(null=True, auto_now_add=True, blank=True)
    Jobcategory = models.ForeignKey('JobCategory', related_name='jobcategory', on_delete=models.CASCADE)
    Description = CKEditor5Field(_('description'), default='Update Info Here', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class JobCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


# class JobSubcategory(models.Model):
#     id = models.AutoField(primary_key=True, unique=True)
#     name = models.CharField(max_length=100)
#     JobCategory = models.ForeignKey('JobCategory', related_name='jobsubcategory', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name


class Applications(models.Model):
    status_choices = (
        ('Received', 'Received'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    )
    status = models.CharField(max_length=250, choices=status_choices)
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    Profession = models.CharField(max_length=250, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    Job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)
    # JobCategory = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, )
    # JobSubcategory = models.ForeignKey(JobSubcategory, on_delete=models.SET_NULL, null=True)
    AdditionalComment = CKEditor5Field(default="Write Your Text here", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(_('date_joined'), auto_now_add=True)
    ResumeUpload = models.FileField(default='resumeUpload/default.pdf', upload_to='resumeUpload', null=True)
    CoverletterUpload = models.FileField(default='CoverletterUpload/default.pdf', upload_to='CoverletterUpload',
                                         null=True)

    class Meta:
        verbose_name_plural = 'Applications'
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.first_name}  {self.user.last_name} -{self.Job}  "

    @property
    def image(self):
        return format_html(
            '<img src="{}" style="max-width:100px; max-height:100px"/>'.format(self.user.user_avatar.url))

    @property
    def name(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Applications_Approval(models.Model):
    id = models.AutoField(primary_key=True)
    Application_id = models.ForeignKey('Applications', related_name='applications_approval', on_delete=models.CASCADE)
    ApprovalUpload = models.FileField(default='approval_message/default.xlsx', upload_to='approval_message', null=True)
    Approvalmessage = models.TextField(_('approval_message'), default='Write Your message here', blank=True, null=True)
    date_created = models.DateTimeField(_('date_joined'), auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='None')

    class Meta:
        verbose_name_plural = 'Applications_Approvals'

    def __str__(self):
        return f"{self.Application_id} -- {self.Application_id.status} "

    @property
    def image(self):
        return format_html(
            '<img src="{}" style="max-width:100px; max-height:100px"/>'.format(self.user.user_avatar.url))

    @property
    def name(self):
        return f"{self.Application_id.user.first_name} {self.Application_id.user.last_name}"


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def get_date(self):
        return humanize.naturaltime(self.created_on)

    class Meta:
        verbose_name_plural = 'Author'


class ElectronicsSolutions(models.Model):
    id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=50, unique=True)
    # itemimage=models.ImageField(max_length=100)
    itemcontent = CKEditor5Field()
    created_on = models.DateTimeField("date published")
    created_by = models.ForeignKey('Author', related_name='electronicsSolution', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.itemname}"

    def was_published_recently(self):
        return self.created_on >= timezone.now() - timedelta(days=1)

    class Meta:
        verbose_name = 'Electronics Solutions Content'
        verbose_name_plural = 'Electronics Solutions Content'
        ordering = ['itemname']


class ElectronicsSolutionsoverview(models.Model):
    overview = CKEditor5Field(default='overview contents', blank=True, unique=True)
    itemimage = models.FileField(default='media/default.jpg', upload_to='profile_photos', null=True)
    mapped_by = models.ForeignKey('ElectronicsSolutions', related_name='electronicsSolutionoverview',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.overview}"

    class Meta:
        verbose_name = 'Electronics Solutions Overview'
        verbose_name_plural = 'Electronics Solutions Overview'


class ICTSolutions(models.Model):
    id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=50, unique=True)
    itemcontent = CKEditor5Field(default='Contents', unique=True)
    created_on = models.DateTimeField("date published")
    created_by = models.ForeignKey('Author', related_name='ICTSolution', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'ICTSolutions Content'
        verbose_name_plural = 'ICTSolutions Content'
        ordering = ['itemname']

    def __str__(self):
        return f"{self.itemname}"

    def was_published_recently(self):
        return self.created_on >= timezone.now() - timedelta(days=1)


class ICTSolutionsoverview(models.Model):
    overview = CKEditor5Field(default='overview contents', verbose_name='Overview content', blank=True, unique=True)
    itemimage = models.FileField(default='media/default.jpg', upload_to='profile_photos', null=True)
    mapped_by = models.ForeignKey('ICTSolutions', related_name='electronicsSolutionoverview', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.overview}"

    class Meta:
        verbose_name = 'ICTSolutions Overview'
        verbose_name_plural = 'ICTSolutions Overview'
        ordering = ['mapped_by']


class EduSolutions(models.Model):
    id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=50, unique=True)
    itemcontent = CKEditor5Field(default='Contents', unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Author', related_name='EduSolution', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.itemname}"

    def was_published_recently(self):
        return self.created_on >= timezone.now() - timedelta(days=1)

    class Meta:
        verbose_name = 'EduSolutions Content'
        verbose_name_plural = 'EduSolutions Content'
        ordering = ['itemname']


class EduSolutionsoverview(models.Model):
    overview = CKEditor5Field(default='overview contents', blank=True, unique=True)
    itemimage = models.FileField(default='media/default.jpg', upload_to='profile_photos', null=True)
    mapped_by = models.ForeignKey('EduSolutions', related_name='electronicsSolutionoverview', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.overview}"

    class Meta:
        verbose_name = 'EduSolutions Overview'
        verbose_name_plural = 'EduSolutions Overview'
        ordering = ['overview']


class MediaSolutions(models.Model):
    id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=50, unique=True)
    itemcontent = CKEditor5Field(default='Contents', unique=True)
    created_on = models.DateTimeField("date published")
    created_by = models.ForeignKey('Author', related_name='MediaSolution', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.itemname}"

    def was_published_recently(self):
        return self.created_on >= timezone.now() - timedelta(days=1)

    class Meta:
        verbose_name = 'Media Solutions Content'
        verbose_name_plural = 'Media Solutions Content'
        ordering = ['itemname']


class MediaSolutionsoverview(models.Model):
    overview = CKEditor5Field(default='overview contents', blank=True, unique=True)
    itemimage = models.FileField(default='media/default.jpg', upload_to='profile_photos', null=True)
    mapped_by = models.ForeignKey('MediaSolutions', related_name='electronicsSolutionoverview',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.overview}"

    class Meta:
        verbose_name = 'MediaSolutions Overview'
        verbose_name_plural = 'MediaSolutions Overview'


class ConsultancyServices(models.Model):
    id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=50, unique=True)
    itemcontent = CKEditor5Field(default='Contents', unique=True)
    created_on = models.DateTimeField("date published")
    created_by = models.ForeignKey('Author', related_name='consultancyServicess', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.itemname}"

    def was_published_recently(self):
        return self.created_on >= timezone.now() - timedelta(days=1)

    class Meta:
        verbose_name = 'Consultancy Services Content'
        verbose_name_plural = 'Consultancy Services Content'
        ordering = ['itemname']


class ConsultancyServicesoverview(models.Model):
    overview = CKEditor5Field(default='overview contents', blank=True, unique=True)
    itemimage = models.FileField(default='media/default.jpg', upload_to='profile_photos', null=True)
    mapped_by = models.ForeignKey('ConsultancyServices', related_name='electronicsSolutionoverview',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.overview}"

    class Meta:
        verbose_name = 'Consultancy Services Overview'
        verbose_name_plural = 'Consultancy Services Overview'


class Industries(models.Model):
    id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=50, unique=True)
    itemcontent = CKEditor5Field(default='Contents')
    created_on = models.DateTimeField("date published")
    created_by = models.ForeignKey('Author', related_name='industriess', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.itemname}"

    def was_published_recently(self):
        return self.created_on >= timezone.now() - timedelta(days=1)

    class Meta:
        verbose_name = 'industries Content'
        verbose_name_plural = 'industries Content'
        ordering = ['itemname']


class Industriesoverview(models.Model):
    overview = CKEditor5Field(default='overview contents', blank=True, unique=True)
    itemimage = models.FileField(default='media/default.jpg', upload_to='profile_photos', null=True)
    mapped_by = models.ForeignKey('Industries', related_name='industriesoverview',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.overview}"

    class Meta:
        verbose_name = 'industries Overview'
        verbose_name_plural = 'industries Overview'


###begining ofabout us
class About(models.Model):
    id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=50, unique=True)
    itemcontent = CKEditor5Field(default='Contents', unique=True)
    created_on = models.DateTimeField("date published")
    created_by = models.ForeignKey('Author', related_name='abouts', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.itemname}"

    def was_published_recently(self):
        return self.created_on >= timezone.now() - timedelta(days=1)

    class Meta:
        verbose_name = 'About Us Content'
        verbose_name_plural = 'About Us Content'
        ordering = ['itemname']


###end of about us
class Aboutoverview(models.Model):
    overview = CKEditor5Field(default='overview contents', blank=True, unique=True)
    itemimage = models.FileField(default='media/default.jpg', upload_to='profile_photos', null=True)
    mapped_by = models.ForeignKey('About', related_name='aboutoverview',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.overview}"

    class Meta:
        verbose_name = 'About Us Overview'
        verbose_name_plural = 'About Us Overview'


class Innovation(models.Model):
    id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=50, unique=True)
    itemcontent = CKEditor5Field(default='Contents', unique=True)
    created_on = models.DateTimeField("date published")
    created_by = models.ForeignKey('Author', related_name='innovations', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.itemname}"

    def was_published_recently(self):
        return self.created_on >= timezone.now() - timedelta(days=1)

    class Meta:
        verbose_name = 'Innovation Content'
        verbose_name_plural = 'Innovation Content'
        ordering = ['itemname']


class Innovationoverview(models.Model):
    overview = CKEditor5Field(default='overview contents', blank=True, unique=True)
    itemimage = models.FileField(default='media/default.jpg', upload_to='profile_photos', null=True)
    mapped_by = models.ForeignKey('Innovation', related_name='innovationverview',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.overview}"

    class Meta:
        verbose_name = 'Innovation Overview'
        verbose_name_plural = 'Innovation Overview'


class InvestorRelations(models.Model):
    id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=50, unique=True)
    itemcontent = CKEditor5Field(default='Contents', unique=True)
    created_on = models.DateTimeField("date published")
    created_by = models.ForeignKey('Author', related_name='investorRelations', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.itemname}"

    def was_published_recently(self):
        return self.created_on >= timezone.now() - timedelta(days=1)

    class Meta:
        verbose_name = 'Investor Relations'
        verbose_name_plural = 'Investor Relations'
        ordering = ['itemname']


class InvestorRelationsoverview(models.Model):
    overview = CKEditor5Field(default='overview contents', blank=True, unique=True)
    itemimage = models.FileField(default='media/default.jpg', upload_to='profile_photos', null=True)
    mapped_by = models.ForeignKey('InvestorRelations', related_name='investorRelationsverview',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.overview}"

    class Meta:
        verbose_name = 'InvestorRelations Overview'
        verbose_name_plural = 'InvestorRelations Overview'


class Careers(models.Model):
    id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=300, unique=True)
    itemcontent = CKEditor5Field(default='Contents', unique=True, max_length=200000)
    created_on = models.DateTimeField("date published")
    created_by = models.ForeignKey('Author', related_name='careers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.itemname}"

    def was_published_recently(self):
        return self.created_on >= timezone.now() - timedelta(days=1)

    class Meta:
        verbose_name = 'Careers'
        verbose_name_plural = 'Careers'
        ordering = ['itemname']


class Careersoverview(models.Model):
    overview = CKEditor5Field(default='overview contents', blank=True, unique=True)
    itemimage = models.FileField(default='media/default.jpg', upload_to='profile_photos', null=True)
    mapped_by = models.ForeignKey('Careers', related_name='careersoverview',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.overview}"

    class Meta:
        verbose_name = 'Careers Overview'
        verbose_name_plural = 'Careers Overview'


class ContactUs(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    Name = models.CharField(max_length=250)
    Email = models.CharField(max_length=50)
    Message = models.TextField(default='Write Your message here')
    # MapAddress = models.CharField(max_length=400, unique=True)
    PhoneNumber = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey('Author', related_name='contactus', on_delete=models.CASCADE

    # def was_published_recently(self):
    #     return self.created_on >= timezone.now() - datetime.timedelta(days=1)


class ContactUsOverView(models.Model):
    overview = CKEditor5Field(default='overview contents', blank=True, unique=True)
    itemimage = models.FileField(default='media/default.jpg', upload_to='profile_photos', null=True)
    mapped_by = models.ForeignKey('ContactUs', related_name='contactus',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.overview}"

    class Meta:
        verbose_name = 'Contact Us Overview'
        verbose_name_plural = 'Contact Us Overview'


class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=50, unique=True)
    itemcontent = CKEditor5Field(default='Contents', unique=True)
    PhoneNumber = models.CharField(max_length=50, unique=True)
    Email = models.CharField(max_length=50, unique=True)
    created_on = models.DateTimeField("date published")
    created_by = models.ForeignKey('Author', related_name='feedback', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.itemname}"

    def was_published_recently(self):
        return self.created_on >= timezone.now() - timedelta(days=1)

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'
        ordering = ['itemname']


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class SolutionsGeneralOverView(models.Model):
    id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=50, unique=True)
    itemcontent = CKEditor5Field(default='Contents', unique=True)
    created_on = models.DateField(default=timezone.now)
    created_by = models.ForeignKey('Author', related_name='solutionsgeneraloverview', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.itemname}"

    def was_published_recently(self):
        return self.created_on >= timezone.now() - timedelta(days=1)

    class Meta:
        verbose_name = 'Solutions General Over View'
        verbose_name_plural = 'Solutions General Over View'
        ordering = ['itemname']


# class BlogSection1(models.Model):
#     id = models.AutoField(primary_key=True)
#     itemname = models.CharField(max_length=50, unique=True)
#     itemcontent = CKEditor5Field(default='Contents', unique=True)
#     created_on = models.DateTimeField("date published")
#     created_by = models.ForeignKey('Author', related_name='blog', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"{self.itemname}"
#
#     def was_published_recently(self):
#         return self.created_on >= timezone.now() - timedelta(days=1)
#
#     class Meta:
#         verbose_name = 'BlogSection1'
#         verbose_name_plural = 'BlogSection1'
#         ordering = ['created_on']

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name






class indexbottom(models.Model):
    title = models.CharField(max_length=200)
    heading=models.CharField(max_length=50)
    content = CKEditor5Field(default='Contents')
    imagebottom = models.ImageField(upload_to='articles/images/')
    thumbnailbottom = models.ImageField(upload_to='thumnailbottom/images/')
    related_articles = models.ManyToManyField('self', blank=True)
    created_by = models.ForeignKey('Author', related_name='lastsectioncontent', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
           return self.title + ' - ' + ', '.join([related_article.title for related_article in self.related_articles.all()])
    
class indexmiddlevideo(models.Model):
    title = models.CharField(max_length=200)
    videoupload = models.FileField(upload_to='IndexLandingVideo/Videos/',unique=True)
    video_link = models.URLField(max_length=200, blank=True,unique=True)
    created_by = models.ForeignKey('Author', related_name='indexmiddlevideo', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 
        
class indexmiddlebottom1(models.Model):
    title = models.CharField(max_length=200)
    heading=models.CharField(max_length=50)
    content = CKEditor5Field(default='Contents')
    imagebottom = models.ImageField(upload_to='articles/images/')
    thumbnailbottom = models.ImageField(upload_to='thumnailmiddlebottombottom/images/')
    created_by = models.ForeignKey('Author', related_name='indexmiddlebottom1', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 
    
class indexmiddlebottom2(models.Model):
    title = models.CharField(max_length=200)
    heading=models.CharField(max_length=50)
    content = CKEditor5Field(default='Contents')
    imagebottom = models.ImageField(upload_to='articles/images/')
    thumbnailbottom = models.ImageField(upload_to='thumnailmiddlebottombottom/images/')
    created_by = models.ForeignKey('Author', related_name='indexmiddlebottom2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title     
    
class indexmiddlebottom3(models.Model):
    title = models.CharField(max_length=200)
    heading=models.CharField(max_length=50)
    content = CKEditor5Field(default='Contents')
    imagebottom = models.ImageField(upload_to='articles/images/')
    thumbnailbottom = models.ImageField(upload_to='thumnailmiddlebottombottom/images/')
    created_by = models.ForeignKey('Author', related_name='indexmiddlebottom3', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title    
class indexmiddlebottom4(models.Model):
    title = models.CharField(max_length=200)
    heading=models.CharField(max_length=50)
    content = CKEditor5Field(default='Contents')
    imagebottom = models.ImageField(upload_to='articles/images/')
    thumbnailbottom = models.ImageField(upload_to='thumnailmiddlebottombottom/images/')
    created_by = models.ForeignKey('Author', related_name='indexmiddlebottom4', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 

        # return self.title + ' - ' + self.thumbnailbottom.url

