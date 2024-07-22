# Create your views here.
import logging
from django.core.exceptions import MiddlewareNotUsed
from django_otp.decorators import otp_required
from django_otp.forms import OTPAuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView
from django.contrib.auth.views import (
    PasswordResetView as DjangoPasswordResetView,
    PasswordResetDoneView as DjangoPasswordResetDoneView,
    PasswordResetConfirmView as DjangoPasswordResetConfirmView,
    PasswordResetForm as DjangoPasswordResetForm,
    PasswordResetCompleteView as DjangoPasswordResetCompleteView
)
from django.db.models import Q
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import UploadedFile
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.http import *
from django.shortcuts import render, redirect
from allauth.account.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.html import strip_tags

from .forms import *
from django.conf import settings
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from uttermostcontent.models import *
from .forms import PersonForm
from django.shortcuts import render, HttpResponse
from .models import *
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import *
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .decorators import non_staff_required


def custom_404(request, exception=None):
    return render(request, 'uttermostcontent/error_404.html', status=404)


def error_500(request):
    return render(request, 'uttermostcontent/500.html', status=500)


def custom_permission_denied_view(request, exception):
    return render(request, 'registration/403.html', status=403)


def download_cheatsheet(request, Applications_Approval_id):
    cheatsheet = get_object_or_404(Applications_Approval, pk=Applications_Approval_id)
    file_path = cheatsheet.ApprovalUpload.path
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{cheatsheet.ApprovalUpload.name}"'
    return response


def cheatsheet(request):
    files = Applications_Approval.objects.filter(user=request.user)
    print(files)
    context = {
        'files': files
    }
    return render(request, 'uttermostcontent/downloads.html', context)


def search_view(request):
    query = request.GET.get('q')
    if query:
        # Search for jobs that contain the query in their name or description
        jobs = Job.objects.filter(Q(name__icontains=query) | Q(Description__icontains=query))
        context = {
            'jobs': jobs,
            'query': query,
        }
        return render(request, 'registration/search_results.html', context)
    else:
        # No query provided, return an empty result
        return render(request, 'registration/search_results.html', {})


def search_results(request):
    query = request.GET.get('q')
    if query:
        # Search for jobs that contain the query in their name or description
        jobs = Job.objects.filter(Q(name__icontains=query) | Q(Description__icontains=query))
        context = {
            'jobs': jobs,
            'query': query,
        }
        return render(request, 'registration/search_results.html', context)
    else:
        # No query provided, return an empty result
        return render(request, 'registration/search_results.html', {})


class PersonListView(ListView):
    model = Applications
    template_name = 'uttermostcontent/applications_list.html'
    context_object_name = 'people'
    paginate_by = 6

    def get_queryset(self):
        return Applications.objects.filter(user=self.request.user).select_related('Job', 'Job__Jobcategory', 'country',
                                                                                  'city')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PersonCreateView(CreateView, LoginRequiredMixin):
    model = Applications
    form_class = PersonForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('person_changelist')


class PersonUpdateView(UpdateView, LoginRequiredMixin):
    model = Applications
    form_class = PersonForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('person_changelist')


class UserProfileCreateView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'users/account/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        email = form.cleaned_data.get('email')
        activation_link = f"{self.request.scheme}://{current_site.domain}/activate/{uid}/{token}/"

        # Render HTML email content
        subject = 'Activate Your Account'
        html_message = render_to_string('registration/account_activated.html', {
            'user': user,
            'activation_link': activation_link,
        })

        # Create plain text version of the email
        plain_message = strip_tags(html_message)

        # Send the email
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email='jasonmukama18@gmail.com',  # Update with your sender email
            to=[email],
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)

        return HttpResponseRedirect(self.success_url)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = SignUpForm
    template_name = 'users/account/UpdateProfile.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can log in to your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class UserProfileListView(ListView):
    model = User
    template_name = 'users/account/userprofile_list.html'
    context_object_name = 'profiles'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)


def job_list(request):
    jobs = Job.objects.all()
    categories = JobCategory.objects.all().order_by('-name')[:10]

    return render(request, 'uttermostcontent/job_list.html', {'jobs': jobs, 'categories': categories})


# def category_jobs(request, category_id):
#     category = get_object_or_404(JobCategory, id=category_id)
#     jobs = category.jobcategory.all()
#     return render(request, 'uttermostcontent/category_jobs.html', {'category': category, 'jobs': jobs})
def job_detail(request, category_id):
    category = get_object_or_404(JobCategory, id=category_id)
    jobs = category.jobcategory.all().order_by('-created_on')[:200]
    return render(request, 'uttermostcontent/category_jobs.html', {'category': category, 'jobs': jobs})


def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    context = {
        "cities": cities,
    }
    return render(request, 'uttermostcontent/city_dropdown_list_options.html', context)


def contact_us(request):
    if request.method == 'POST':
        contact_form = ContactForms(request.POST)
        search_form = SearchForm(request.POST)
        subscription_form = SubscriptionForm(request.POST)

        if contact_form.is_valid():
            Name = contact_form.cleaned_data['Name']
            Email = contact_form.cleaned_data['Email']
            Message = contact_form.cleaned_data['Message']
            PhoneNumber = contact_form.cleaned_data['PhoneNumber']

            full_message = f"Message from {Name} ({Email} {PhoneNumber}):\n\n{Message}"

            send_mail(
                Name,
                full_message,
                'jasonmukama18@gmail.com',  # Replace with your email or a specific contact email
                [Email],  # Send the email to the user
                fail_silently=False,
            )

            return render(request, 'pages/success.html')

        elif search_form.is_valid():
            # Handle search form logic
            query = search_form.cleaned_data['query']
            model = search_form.cleaned_data['model']
            # Process the search query based on the selected model

        elif subscription_form.is_valid():
            # Handle subscription form logic
            subscription_form.save()
            return render(request, 'pages/success.html')

    else:
        contact_form = ContactForms()
        search_form = SearchForm()
        subscription_form = SubscriptionForm()

    return render(request, 'pages/Contact Us.html', {
        'contact_form': contact_form,
        'search_form': search_form,
        'subscription_form': subscription_form,
    })


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('index')
    else:
        form = SubscriptionForm()

    return render(request, 'base.html', {'form': form})


@non_staff_required
def home(request):
    if request.user.is_authenticated:
        user = request.user
        full_name = f"{user.last_name} {user.first_name}"
        profileimage = user.user_avatar.url
        email = user.email

        return render(
            request,
            "users/dashboard/home.html",
            {
                "full_name": full_name,
                "profileimage": profileimage,
                "email": email
            },
        )
    else:
        return HttpResponseRedirect("/login/")


# Dashboard
@non_staff_required
def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        full_name = f"{user.last_name} {user.first_name}"
        phonenum = user.phone
        address = user.address
        profileimage = user.user_avatar.url
        Profession = Applications.objects.filter(user=request.user)
        email = user.email
        jobsapplied = Applications_Approval.objects.filter(user=request.user).count()
        jobsavailable = Applications_Approval.objects.all().count()
        return render(
            request,
            "users/dashboard/dashboard.html",
            {
                "full_name": full_name,
                "profileimage": profileimage,
                "email": email,
                "jobsapplied": jobsapplied,
                "jobsavailable": jobsavailable,
                "phonenum": phonenum,
                "address": address,
                "Profession": Profession

            },
        )
    else:
        return HttpResponseRedirect("/login/")


# Sigup




def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data["username"]
                upass = form.cleaned_data["password"]
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    if user.is_superuser:
                        return HttpResponseForbidden("Staff members are not allowed to log in! "
                                                     "Please contact the administrator")
                    login(request, user)
                    messages.success(request, "Logged in Successfully !!")
                    return HttpResponseRedirect("/dashboard/")
        else:
            form = LoginForm()
        return render(request, "registration/login.html", {"form": form})
    else:
        return HttpResponseRedirect("/dashboard/")

@login_required
@otp_required
def two_factor_auth(request, user_id):
    if request.method == "POST":
        form = OTPAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Logged in Successfully !!")
            return HttpResponseRedirect("/dashboard/")
    else:
        form = OTPAuthenticationForm(request=request)
    return render(request, "registration/two_factor_auth.html", {"form": form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login/")


class CustomPasswordResetView(DjangoPasswordResetView):
    template_name = 'registration/custom_password_reset_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(DjangoPasswordResetDoneView):
    template_name = 'registration/custom_password_reset_done.html'


class CustomPasswordResetConfirmView(DjangoPasswordResetConfirmView):
    template_name = 'registration/custom_password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/custom_password_reset_complete.html'  # Customize this template if needed
    success_url = reverse_lazy('logins')


####
def index(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('index')
    else:
        form = SubscriptionForm()

    # Initialize other forms
    contact_form = ContactForms()
    search_form = SearchForm()
    subscription_form = SubscriptionForm(request.POST)
    indexmiddlevideos = indexmiddlevideo.objects.order_by("-created_at")[:1]
    data_overview = ElectronicsSolutionsoverview.objects.all()
    # Fetching only the latest categories
    indexbottomcontent = indexbottom.objects.order_by("-title")[:3]
    indexmiddlebottom1s = indexmiddlebottom1.objects.order_by("-title")[:3]
    indexmiddlebottom2s = indexmiddlebottom2.objects.order_by("-title")[:3]
    indexmiddlebottom3s = indexmiddlebottom3.objects.order_by("-title")[:3]
    indexmiddlebottom4s = indexmiddlebottom4.objects.order_by("-title")[:3]
    context = {
        "indexmiddlevideos": indexmiddlevideos,
        "data_overview": data_overview,
        "indexmiddlebottom1s": indexmiddlebottom1s,
        "form": form,
        "contact_form": contact_form,
        "search_form": search_form,
        "subscription_form": subscription_form,
        "indexbottomcontent": indexbottomcontent,
        "indexmiddlebottom2s": indexmiddlebottom2s,
        "indexmiddlebottom3s": indexmiddlebottom3s,
        "indexmiddlebottom4s": indexmiddlebottom4s,
        
    }
    return render(request, "pages/Index.html", context)


def electronicsolutions(request):
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('electronicsolutions')
    else:
        subscription_form = SubscriptionForm()

    data = ElectronicsSolutions.objects.all()
    data_overview = ElectronicsSolutionsoverview.objects.all()
    solutionsdata_overview = SolutionsGeneralOverView.objects.all()
    context = {
        "data": data,
        "data_overview": data_overview,
        "solutionsdata_overview": solutionsdata_overview,
        "subscription_form": subscription_form
    }
    return render(request, "pages/EngineeringSolutions.html", context)


def ictsolutions(request):
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('ictsolutions')
    else:
        subscription_form = SubscriptionForm()

    data = ICTSolutions.objects.all()
    data_overview = ICTSolutionsoverview.objects.all()
    solutionsdata_overview = SolutionsGeneralOverView.objects.all()
    context = {
        "data": data,
        "data_overview": data_overview,
        "solutionsdata_overview": solutionsdata_overview,
        "subscription_form": subscription_form
    }
    return render(request, "pages/IctSolutions.html", context)


def eduSolutions(request):
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('edusolutions')
    else:
        subscription_form = SubscriptionForm()

    data = EduSolutions.objects.all()
    data_overview = EduSolutionsoverview.objects.all()
    solutionsdata_overview = SolutionsGeneralOverView.objects.all()
    context = {
        "data": data,
        "data_overview": data_overview,
        "solutionsdata_overview": solutionsdata_overview,
        "subscription_form": subscription_form
    }
    return render(request, "pages/EduSolutions.html", context)


def mediasolutions(request):
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('mediasolutions')
    else:
        subscription_form = SubscriptionForm()

    data = MediaSolutions.objects.all()
    data_overview = MediaSolutionsoverview.objects.all()
    solutionsdata_overview = SolutionsGeneralOverView.objects.all()
    context = {
        "data": data,
        "data_overview": data_overview,
        "solutionsdata_overview": solutionsdata_overview,
        "subscription_form": subscription_form
    }
    return render(request, "pages/MediaSolutions.html", context)


def consultancysolutions(request):
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('consultancysolutions')
    else:
        subscription_form = SubscriptionForm()

    data = ConsultancyServices.objects.all()
    data_overview = ConsultancyServicesoverview.objects.all()
    solutionsdata_overview = SolutionsGeneralOverView.objects.all()
    context = {
        "data": data,
        "data_overview": data_overview,
        "solutionsdata_overview": solutionsdata_overview,
        "subscription_form": subscription_form
    }
    return render(request, "pages/consultancyServices.html", context)


def aboutpage(request):
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('aboutpage')
    else:
        subscription_form = SubscriptionForm()

    data = About.objects.all()
    data_overview = Aboutoverview.objects.all()
    solutionsdata_overview = SolutionsGeneralOverView.objects.all()
    context = {
        "data": data,
        "data_overview": data_overview,
        "solutionsdata_overview": solutionsdata_overview,
        "subscription_form": subscription_form
    }
    return render(request, "pages/AboutUs.html", context)


def industries(request):
    data = Industries.objects.all()
    data_overview = Industriesoverview.objects.all()
    context = {
        "data": data,
        "data_overview": data_overview,

    }
    return render(request, "pages/industries.html", context)


def innovationcenter(request):
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('innovationcenter')
    else:
        subscription_form = SubscriptionForm()

    data = Innovation.objects.all()
    data_overview = Innovationoverview.objects.all()
    solutionsdata_overview = SolutionsGeneralOverView.objects.all()
    context = {
        "data": data,
        "data_overview": data_overview,
        "solutionsdata_overview": solutionsdata_overview,
        "subscription_form": subscription_form
    }
    return render(request, "pages/InnovationCenter.html", context)


def careers(request):
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('careers')
    else:
        subscription_form = SubscriptionForm()

    data = Careers.objects.all()
    data_overview = Careersoverview.objects.all()
    solutionsdata_overview = SolutionsGeneralOverView.objects.all()
    context = {
        "data": data,
        "data_overview": data_overview,
        "solutionsdata_overview": solutionsdata_overview,
        "subscription_form": subscription_form
    }
    return render(request, "pages/careers.html", context)


def investorrelations(request):
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('investorrelations')
    else:
        subscription_form = SubscriptionForm()

    data = InvestorRelations.objects.all()
    data_overview = InvestorRelationsoverview.objects.all()
    solutionsdata_overview = SolutionsGeneralOverView.objects.all()
    context = {
        "data": data,
        "data_overview": data_overview,
        "solutionsdata_overview": solutionsdata_overview,
        "subscription_form": subscription_form
    }
    return render(request, "pages/InvestorRelations.html", context)
