from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from apps.recruitment.functions import getAge
from django.contrib import messages
from django.db.models import Q
from datetime import date
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import os
from django.conf import settings
from .ResumeParser import *


@login_required
def cvrepo_home(request):
    return render(request, "cvrepo/cvrepo_home.html", {})


@login_required
def my_repository(request):
    obj_cv = CVRepo.objects.filter(CANDIDATE_OWNER=request.user.username).order_by('-TIMESTAMP')
    page = request.GET.get('page', 1)
    paginator = Paginator(obj_cv, 20)
    try:
        obj_cv = paginator.page(page)
    except PageNotAnInteger:
        obj_cv = paginator.page(1)
    except EmptyPage:
        obj_cv = paginator.page(paginator.num_pages)
    return render(request, "cvrepo/my_repository.html", {'obj_cv': obj_cv})


@login_required
def upload_cv(request):
    context = {
        'form': NewCVForm()
    }
    if request.method == 'POST':
        form = NewCVForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            EMAIL = form.cleaned_data['EMAIL']
            MOBILE_NUMBER = form.cleaned_data['MOBILE_NUMBER']
            SECONDARY_EMAIL = form.cleaned_data['SECONDARY_EMAIL']
            SECONDARY_EMAIL = SECONDARY_EMAIL if SECONDARY_EMAIL else 'None'
            PAN_NUMBER = form.cleaned_data['PAN_NUMBER'].upper()
            # Check if attachment size exceeded
            attachment = form.cleaned_data['RESUME']
            if attachment.size > settings.MAX_UPLOAD_SIZE:
                messages.warning(request, "Resume size exceeded. Please Check !!!")
                form = NewCVForm(request.POST, request.FILES)
                context['form'] = form
                return render(request, 'cvrepo/upload_cv.html', context)
            # Check if candidate is above 18 years
            DATE_OF_BIRTH = form.cleaned_data['DATE_OF_BIRTH']
            age = getAge(DATE_OF_BIRTH)
            if age < 18 :
                messages.warning(request, "Date of Birth looks invalid. It is below 18 !!!")
                context['form'] = NewCVForm(request.POST, request.FILES)
                return render(request, 'cvrepo/upload_cv.html', context)

            # Check candidate if already exist
            obj_cv = CVRepo.objects.filter((Q(PAN_NUMBER=PAN_NUMBER) |
                                                 Q(EMAIL=EMAIL) |
                                                Q(EMAIL=SECONDARY_EMAIL) |
                                                Q(MOBILE_NUMBER=MOBILE_NUMBER) |
                                                Q(SECONDARY_EMAIL=SECONDARY_EMAIL) |
                                                Q(SECONDARY_EMAIL=EMAIL)))
            if len(obj_cv) > 0:
                messages.warning(request, "CV already exists !!!")
                context['obj_candidate'] = obj_cv
                context['form'] = NewCVForm(request.POST, request.FILES)
                return render(request, 'cvrepo/upload_cv.html', context)
            else:
                # form.save()
                # obj = form.save(commit=False)
                obj.save()
                id = obj.pk
                context['id'] = id
                obj_candidate = CVRepo.objects.get(id=id)
                # Converting to upper case
                obj_candidate.FIRST_NAME = obj_candidate.FIRST_NAME.upper() if obj_candidate.FIRST_NAME else None
                obj_candidate.LAST_NAME = obj_candidate.LAST_NAME.upper() if obj_candidate.LAST_NAME else None
                obj_candidate.CURRENT_LOCATION = obj_candidate.CURRENT_LOCATION.upper() if obj_candidate.CURRENT_LOCATION else None
                obj_candidate.PAN_NUMBER = obj_candidate.PAN_NUMBER.upper() if obj_candidate.PAN_NUMBER else None
                year = date.today().strftime('%Y')
                month = date.today().strftime('%m')
                obj_candidate.CV_NUMBER = 'CV' + str(year) + str(1000+id)
                obj_candidate.CANDIDATE_OWNER = request.user.username
                obj_candidate.save()
                messages.success(request, f"CV has been uploaded !!! CV Number is {obj_candidate.CV_NUMBER}")
                return render(request, 'cvrepo/upload_cv.html', context)
        else:
            context['form'] = NewCVForm(request.POST, request.FILES)
            messages.warning(request, form.errors)
            return render(request, 'cvrepo/upload_cv.html', context)
    return render(request, 'cvrepo/upload_cv.html', context)


@login_required
def edit_cv(request, id=None):
    obj_cv = get_object_or_404(CVRepo, id=id)
    form = NewCVForm(instance=obj_cv)
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = NewCVForm(request.POST, request.FILES, instance=obj_cv)
        if form.is_valid():
            obj = form.save(commit=False)
            EMAIL = form.cleaned_data['EMAIL']
            MOBILE_NUMBER = form.cleaned_data['MOBILE_NUMBER']
            SECONDARY_EMAIL = form.cleaned_data['SECONDARY_EMAIL']
            SECONDARY_EMAIL = SECONDARY_EMAIL if SECONDARY_EMAIL else 'None'
            PAN_NUMBER = form.cleaned_data['PAN_NUMBER'].upper()
            # Check if attachment size exceeded
            attachment = form.cleaned_data['RESUME']
            if attachment.size > settings.MAX_UPLOAD_SIZE:
                messages.warning(request, "Resume size exceeded. Please Check !!!")
                form = NewCVForm(request.POST, request.FILES, instance=obj_cv)
                context['form'] = form
                return render(request, 'cvrepo/edit_cv.html', context)
            # Check if candidate is above 18 years
            DATE_OF_BIRTH = form.cleaned_data['DATE_OF_BIRTH']
            age = getAge(DATE_OF_BIRTH)
            if age < 18 :
                messages.warning(request, "Date of Birth looks invalid. It is below 18 !!!")
                context['form'] = NewCVForm(request.POST, request.FILES)
                return render(request, 'cvrepo/edit_cv.html', context)
            # form.save()
            # obj = form.save(commit=False)
            obj.save()
            obj_candidate = CVRepo.objects.get(id=id)
            # Converting to upper case
            obj_candidate.FIRST_NAME = obj_candidate.FIRST_NAME.upper() if obj_candidate.FIRST_NAME else None
            obj_candidate.LAST_NAME = obj_candidate.LAST_NAME.upper() if obj_candidate.LAST_NAME else None
            obj_candidate.CURRENT_LOCATION = obj_candidate.CURRENT_LOCATION.upper() if obj_candidate.CURRENT_LOCATION else None
            obj_candidate.PAN_NUMBER = obj_candidate.PAN_NUMBER.upper() if obj_candidate.PAN_NUMBER else None
            obj_candidate.save()
            messages.success(request, "Data has been updated !!!")
            return HttpResponseRedirect(reverse(my_repository))
            # return render(request, 'cvrepo/edit_cv.html', context)
        else:
            context['form'] = NewCVForm(request.POST, request.FILES, instance=obj_cv)
            messages.warning(request, form.errors)
            return render(request, 'cvrepo/edit_cv.html', context)
    return render(request, 'cvrepo/edit_cv.html', context)


@login_required
def cv_download(request, id=None):
    obj_cv = get_object_or_404(CVRepo, id=id)
    docs_path = os.path.join(settings.MEDIA_ROOT, str(obj_cv.RESUME))
    if os.path.exists(docs_path):
        with open(docs_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename='+os.path.basename(docs_path)
            return response
    raise Http404


@login_required
def view_cv(request, id=None):
    obj_cv = get_object_or_404(CVRepo, id=id)
    form = NewCVForm(instance=obj_cv)
    return render(request, 'cvrepo/view_cv.html', {'form': form})


@login_required
def search_cv(request):
    form = SearchCVForm()
    if request.method == 'GET':
        obj_cv = CVRepo.objects.all().order_by('-TIMESTAMP')
        SEARCH_BY = request.GET.get("SEARCH_BY")
        SEARCH_TEXT = request.GET.get("SEARCH_TEXT")
        GENDER = request.GET.get("GENDER")
        PAN_NUMBER = request.GET.get("PAN_NUMBER")
        EMAIL = request.GET.get("EMAIL")
        QUALIFICATION = request.GET.get("QUALIFICATION")
        if SEARCH_BY == 'CANDIATE_NAME':
            obj_cv = CVRepo.objects.filter(Q(FIRST_NAME__icontains=SEARCH_TEXT) | Q(LAST_NAME__icontains=SEARCH_TEXT)).order_by('-TIMESTAMP')
        if SEARCH_BY == 'SKILLS':
            obj_cv = CVRepo.objects.filter(SKILLS__icontains=SEARCH_TEXT).order_by('-TIMESTAMP')
        if SEARCH_BY == 'CV_NUMBER':
            obj_cv = CVRepo.objects.filter(CV_NUMBER=SEARCH_TEXT).order_by('-TIMESTAMP')
        if SEARCH_BY == 'CANDIDATE_CODE':
            obj_cv = CVRepo.objects.filter(CANDIDATE_CODE=SEARCH_TEXT).order_by('-TIMESTAMP')
        if SEARCH_BY == 'GENDER':
            obj_cv = CVRepo.objects.filter(GENDER=GENDER).order_by('-TIMESTAMP')
        if SEARCH_BY == 'PAN_NUMBER':
            obj_cv = CVRepo.objects.filter(PAN_NUMBER=PAN_NUMBER).order_by('-TIMESTAMP')
        if SEARCH_BY == 'MOBILE_NUMBER':
            obj_cv = CVRepo.objects.filter(Q(MOBILE_NUMBER__icontains=SEARCH_TEXT) | Q(ALTERNATE_PHONE__icontains=SEARCH_TEXT)).order_by('-TIMESTAMP')
        if SEARCH_BY == 'EMAIL':
            obj_cv = CVRepo.objects.filter(Q(EMAIL=EMAIL) | Q(SECONDARY_EMAIL=EMAIL)).order_by('-TIMESTAMP')
        if SEARCH_BY == 'QUALIFICATION':
            obj_cv = CVRepo.objects.filter(QUALIFICATION__icontains=SEARCH_TEXT).order_by('-TIMESTAMP')
        if SEARCH_BY == 'WORK_EXPERIENCE':
            obj_cv = CVRepo.objects.filter(WORK_EXPERIENCE__icontains=SEARCH_TEXT).order_by('-TIMESTAMP')
        if SEARCH_BY == 'CURRENT_LOCATION':
            obj_cv = CVRepo.objects.filter(CURRENT_LOCATION__icontains=SEARCH_TEXT).order_by('-TIMESTAMP')
        if SEARCH_BY == 'SOURCE':
            obj_cv = CVRepo.objects.filter(SOURCE__icontains=SEARCH_TEXT).order_by('-TIMESTAMP')
        if SEARCH_BY == 'CANDIDATE_OWNER':
            obj_cv = CVRepo.objects.filter(CANDIDATE_OWNER=SEARCH_TEXT).order_by('-TIMESTAMP')

        page = request.GET.get('page', 1)
        paginator = Paginator(obj_cv, 50)
        try:
            obj_cv = paginator.page(page)
        except PageNotAnInteger:
            obj_cv = paginator.page(1)
        except EmptyPage:
            obj_cv = paginator.page(paginator.num_pages)
        form = SearchCVForm(request.GET)
        return render(request, "cvrepo/search_cv.html", {'obj_cv': obj_cv, 'form': form})
    # return render(request, "cvrepo/search_cv.html", {'form': form, 'obj_cv': obj_cv})


def handle_uploaded_file(f, extension):
    tempFilePath = os.path.join(settings.MEDIA_ROOT, 'TempFiles/TempResume'+str(extension))
    with open(tempFilePath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required
def auto_upload_cv(request):
    form = AutoUploadCVForm()
    if request.method == 'POST':
        form = AutoUploadCVForm(request.POST, request.FILES)
        attachment = request.FILES['RESUME']
        extension = os.path.splitext(attachment.name)[1]
        handle_uploaded_file(attachment, extension)
        tempFilePath = os.path.join(settings.MEDIA_ROOT, 'TempFiles\TempResume'+str(extension))
        if form.is_valid():
            extension = os.path.splitext(attachment.name)[1]
            if attachment.size > settings.MAX_UPLOAD_SIZE:
                messages.warning(request, "Resume size exceeded.")
                return render(request, "cvrepo/auto_upload_cv.html", {"form": form})

            # if form is valid
            data = resume_parsing(tempFilePath)
            CANDIDATE_FULL_NAME = data.get('name') if data.get('name') else None
            full_name = get_name(CANDIDATE_FULL_NAME)
            mobile_number = data.get('mobile_number') if data.get('mobile_number') else None
            email = data.get('email') if data.get('email') else None
            skills = ", ".join(data.get('skills')) if data.get('skills') else None

            # Check candidate if already exist
            obj_cv = CVRepo.objects.filter(Q(EMAIL=email) | Q(MOBILE_NUMBER=mobile_number))
            if len(obj_cv) > 0:
                messages.warning(request, "This CV is already exists in repository !!!")
                form = AutoUploadCVForm(request.POST, request.FILES)
                return render(request, 'cvrepo/auto_upload_cv.html', {'form': form})

            cv = form.save(commit=False)
            cv.save()
            year = date.today().strftime('%Y')
            obj_cv = get_object_or_404(CVRepo, id=cv.pk)
            CV_NUMBER = 'CV' + str(year) + str(1000 + cv.pk)
            obj_cv.CV_NUMBER = CV_NUMBER
            obj_cv.CANDIDATE_OWNER=request.user.username
            obj_cv.save()
            form = AutoUploadCVForm(instance=obj_cv)
            return render(request, 'cvrepo/auto_upload_cv.html', {'form': form, 'data': data, 'skills': skills})
            # Create object for new cv
            # obj = CVRepo.objects.create(FIRST_NAME=FIRST_NAME,
            #                             LAST_NAME=LAST_NAME,
            #                             MOBILE_NUMBER=str(MOBILE_NUMBER),
            #                             EMAIL=EMAIL,
            #                             SKILLS=SKILLS,
            #                             CANDIDATE_OWNER=request.user.username)
            # obj.save()
            # id = obj.id
            # year = date.today().strftime('%Y')
            # month = date.today().strftime('%m')
            # obj_cv = get_object_or_404(CVRepo, id=id)
            # CV_NUMBER = 'CV' + str(year) + str(1000 + id)
            # obj_cv.CV_NUMBER = CV_NUMBER
            # obj_cv.RESUME = attachment
            # obj_cv.save()
            # # Rename CV
            # cv_path = os.path.join(settings.MEDIA_ROOT, str(obj_cv.RESUME))
            # new_filename = str(obj_cv.CV_NUMBER)+extension
            # obj_cv.RESUME = "CV_Repository/"+new_filename
            # obj_cv.save()
            # messages.success(request, "CV has been uploaded")
            # form = AutoUploadCVForm(request.POST, request.FILES)
            # return HttpResponseRedirect(f'/cvrepo/auto_upload_cv/{id}/')
        else:
            form = AutoUploadCVForm(request.POST, request.FILES)
            messages.warning(request, form.errors)
            return render(request, "cvrepo/auto_upload_cv.html", {'form': form})
    return render(request, "cvrepo/auto_upload_cv.html", {'form': form})


@login_required
def edit_auto_upload_cv(request, id=None):
    obj_cv = get_object_or_404(CVRepo, id=id)
    form = AutoUploadCVForm(instance=obj_cv)
    if request.method == 'POST':
        form = AutoUploadCVForm(request.POST, instance=obj_cv)
        if form.is_valid():
            form.save()
            messages.success(request, "Data has been updated")
            form = AutoUploadCVForm(request.POST, instance=obj_cv)
            return render(request, "cvrepo/auto_upload_cv.html",{'form': form})
        else:
            form = AutoUploadCVForm(request.POST, instance=obj_cv)
            messages.warning(request, form.errors)
            return render(request, "cvrepo/auto_upload_cv.html", {'form': form})
    return render(request, "cvrepo/auto_upload_cv.html", {'form': form})
