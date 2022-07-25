from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse, Http404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import os
from django.utils.timezone import now
from apps.accounts.models import User
from django.db.models import Q


@login_required
def employee_registration(request, id=None):
    context = {
        'form': EmployeeRegistrationForm(),
        'formWork': WorkDetailsForm(),
        'formEmp': LastEmploymentForm(),
        'formBank': BankDetailsForm(),
        'formDocs': EmployeeDocumentsForm()
    }
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            FIRST_NAME = form.cleaned_data['FIRST_NAME']
            LAST_NAME = form.cleaned_data['LAST_NAME']
            DATE_OF_BIRTH = form.cleaned_data['DATE_OF_BIRTH']
            GENDER = form.cleaned_data['GENDER']
            PERSONNEL_EMAIL = form.cleaned_data['PERSONNEL_EMAIL']
            PRIMARY_MOBILE_NO = form.cleaned_data['PRIMARY_MOBILE_NO']
            obj_emp = Employee.objects.filter(DATE_OF_BIRTH=DATE_OF_BIRTH, PERSONNEL_EMAIL=str(PERSONNEL_EMAIL).upper())
            if len(obj_emp)>0:
                messages.warning(request, "Employee already exists !!!")
                context['form'] = EmployeeRegistrationForm(request.POST)
                return render(request, 'employee/emp_registration.html', context)
            else:
                obj.save()
                id = obj.pk
                context['id'] = id
                obj_emp = Employee.objects.get(id=id)
                obj_emp.CREATED_BY = request.user.username
                # Converting to upper case
                obj_emp.FIRST_NAME = obj_emp.FIRST_NAME.upper() if obj_emp.FIRST_NAME else None
                obj_emp.MIDDLE_NAME = obj_emp.MIDDLE_NAME.upper() if obj_emp.MIDDLE_NAME else None
                obj_emp.LAST_NAME = obj_emp.LAST_NAME.upper() if obj_emp.LAST_NAME else None
                obj_emp.FATHER_NAME = obj_emp.FATHER_NAME.upper() if obj_emp.FATHER_NAME else None
                obj_emp.PRESENT_ADDRESS = obj_emp.PRESENT_ADDRESS.upper() if obj_emp.PRESENT_ADDRESS else None
                obj_emp.PRESENT_CITY = obj_emp.PRESENT_CITY.upper() if obj_emp.PRESENT_CITY else None
                obj_emp.EMERGENCY_CONTACT_NAME = obj_emp.EMERGENCY_CONTACT_NAME.upper() if obj_emp.EMERGENCY_CONTACT_NAME else None
                obj_emp.PERSONNEL_EMAIL = obj_emp.PERSONNEL_EMAIL.upper() if obj_emp.PERSONNEL_EMAIL else None
                # # Generate employee code
                # obj_emp.EMPLOYEE_CODE = str(2812) + str(id).zfill(3)
                obj_emp.save()
                obj_emp = Employee.objects.get(id=id)
                # Employee full name
                if (obj_emp.MIDDLE_NAME) and (obj_emp.LAST_NAME):
                    obj_emp.EMPLOYEE_FULL_NAME = obj_emp.FIRST_NAME + " " + obj_emp.MIDDLE_NAME + " " + obj_emp.LAST_NAME
                elif (not obj_emp.MIDDLE_NAME) and (obj_emp.LAST_NAME):
                    obj_emp.EMPLOYEE_FULL_NAME = obj_emp.FIRST_NAME + " " + obj_emp.LAST_NAME
                elif (obj_emp.MIDDLE_NAME) and (not obj_emp.LAST_NAME):
                    obj_emp.EMPLOYEE_FULL_NAME = obj_emp.FIRST_NAME + " " + obj_emp.MIDDLE_NAME
                elif (not obj_emp.MIDDLE_NAME) and (not obj_emp.LAST_NAME):
                    obj_emp.EMPLOYEE_FULL_NAME = obj_emp.FIRST_NAME
                obj_emp.save()
                context['form'] = EmployeeRegistrationForm(instance=obj_emp)
                context['obj_emp'] = obj_emp
                context['activeTab_No'] = 1
                # messages.success(request, f"Registration Success !!! Employee Code is {obj_emp.EMPLOYEE_CODE}")
                messages.success(request, "Registration Success !!!")
                # return render(request, 'employee/emp_details_edit.html', context)
                return HttpResponseRedirect(f'/employee/{id}/details/')
        else:
            context['form'] = EmployeeRegistrationForm(request.POST)
            messages.warning(request, form.errors)
            return render(request, 'employee/emp_registration.html', context)
    return render(request, 'employee/emp_registration.html', context)


@login_required
def employee_info(request, id=None):
    obj_emp = Employee.objects.get(id=id)
    obj_emp_docs = EmployeeDocuments.objects.filter(EMPLOYEE_CODE_id=id).order_by('-UPLOAD_TIMESTAMP')
    context = {
        'form': EmployeeRegistrationForm(instance=obj_emp),
        'obj_emp': obj_emp,
        'obj_emp_docs': obj_emp_docs,
        'formWork': WorkDetailsForm(instance=obj_emp),
        'formEmp': LastEmploymentForm(instance=obj_emp),
        'formBank': BankDetailsForm(instance=obj_emp),
        'formDocs': EmployeeDocumentsForm(),
        'activeTab_No': 1,
    }
    if (request.method == 'POST') and ('btn_basicDetails' in request.POST):
        context['activeTab_No'] = 1
        form = EmployeeRegistrationForm(request.POST, instance=obj_emp)
        if form.is_valid():
            form.save()
            obj_emp = Employee.objects.get(id=id)
            obj_emp.MODIFIED_BY = request.user.username
            obj_emp.LAST_MODIFIED = now()
            # Converting to upper case
            obj_emp.FIRST_NAME = obj_emp.FIRST_NAME.upper() if obj_emp.FIRST_NAME else None
            obj_emp.MIDDLE_NAME = obj_emp.MIDDLE_NAME.upper() if obj_emp.MIDDLE_NAME else None
            obj_emp.LAST_NAME = obj_emp.LAST_NAME.upper() if obj_emp.LAST_NAME else None
            obj_emp.FATHER_NAME = obj_emp.FATHER_NAME.upper() if obj_emp.FATHER_NAME else None
            obj_emp.PRESENT_ADDRESS = obj_emp.PRESENT_ADDRESS.upper() if obj_emp.PRESENT_ADDRESS else None
            obj_emp.PRESENT_CITY = obj_emp.PRESENT_CITY.upper() if obj_emp.PRESENT_CITY else None
            obj_emp.EMERGENCY_CONTACT_NAME = obj_emp.EMERGENCY_CONTACT_NAME.upper() if obj_emp.EMERGENCY_CONTACT_NAME else None
            obj_emp.PERSONNEL_EMAIL = obj_emp.PERSONNEL_EMAIL.upper() if obj_emp.PERSONNEL_EMAIL else None
            obj_emp.save()
            # Employee full name
            obj_emp = Employee.objects.get(id=id)
            if (obj_emp.MIDDLE_NAME) and (obj_emp.LAST_NAME):
                obj_emp.EMPLOYEE_FULL_NAME = obj_emp.FIRST_NAME + " " + obj_emp.MIDDLE_NAME + " " + obj_emp.LAST_NAME
            elif (not obj_emp.MIDDLE_NAME) and (obj_emp.LAST_NAME):
                obj_emp.EMPLOYEE_FULL_NAME = obj_emp.FIRST_NAME + " " + obj_emp.LAST_NAME
            elif (obj_emp.MIDDLE_NAME) and (not obj_emp.LAST_NAME):
                obj_emp.EMPLOYEE_FULL_NAME = obj_emp.FIRST_NAME + " " + obj_emp.MIDDLE_NAME
            elif (not obj_emp.MIDDLE_NAME) and (not obj_emp.LAST_NAME):
                obj_emp.EMPLOYEE_FULL_NAME = obj_emp.FIRST_NAME
            obj_emp.save()
            context['form'] = EmployeeRegistrationForm(instance=obj_emp)
            messages.success(request, "Data has been updated !!!")
            return render(request, 'employee/emp_details_edit.html', context)
        else:
            context['form'] = EmployeeRegistrationForm(request.POST, instance=obj_emp)
            messages.warning(request, form.errors)
            # return render(request, 'employee/emp_details_edit.html', context)
            return HttpResponseRedirect('/employee/')
    if (request.method == 'POST') and ('btn_workDetails' in request.POST):
        context['activeTab_No'] = 2
        formWork = WorkDetailsForm(request.POST, instance=obj_emp)
        if formWork.is_valid():
            formWork.save()
            obj_emp = Employee.objects.get(id=id)
            obj_emp.MODIFIED_BY = request.user.username
            obj_emp.LAST_MODIFIED = now()
            # Converting to upper case
            obj_emp.REFERENCE_NAME = obj_emp.REFERENCE_NAME.upper() if obj_emp.REFERENCE_NAME else None
            obj_emp.OFFICIAL_EMAIL = obj_emp.OFFICIAL_EMAIL.upper() if obj_emp.OFFICIAL_EMAIL else None
            obj_emp.save()
            context['formWork'] = WorkDetailsForm(instance=obj_emp)
            # Generate employee code
            if not obj_emp.EMPLOYEE_CODE:
                obj_emp.EMPLOYEE_CODE = str(2812) + str(id).zfill(3)
                obj_emp.save()
                msg = f"Data has been updated !!! Employee Code is {obj_emp.EMPLOYEE_CODE}"
            else:
                msg = "Data has been updated !!!"
            messages.success(request, msg)
            # Update Reporting manager and HR manager
            if obj_emp.REPORTING_MANAGER_CODE == "1111111":
                obj_emp.REPORTING_MANAGER_CODE = obj_emp.EMPLOYEE_CODE
            if obj_emp.HR_MANAGER_CODE == "1111111":
                obj_emp.HR_MANAGER_CODE = obj_emp.EMPLOYEE_CODE
            obj_emp.save()
            # Create User - Default Role will be recruiter
            try:
                userObj = User.objects.filter(username=obj_emp.EMPLOYEE_CODE)
                if len(userObj) > 0:
                    pass
                else:
                    obj_user = User.objects.create_user(username=obj_emp.EMPLOYEE_CODE,
                                                        email=obj_emp.OFFICIAL_EMAIL.lower(),
                                                        password="Welcome@"+str(obj_emp.EMPLOYEE_CODE),
                                                        user_type=3, roles=1,
                                                        first_name=obj_emp.FIRST_NAME,
                                                        last_name=obj_emp.LAST_NAME if obj_emp.LAST_NAME else '')
                    obj_emp.IS_USER_CREATED=True
                    obj_emp.EMPLOYEE_STATUS = "ACTIVE"
                    obj_emp.save()
                    messages.success(request, "User account has been created.")
            except:
                pass

            context['obj_emp'] = Employee.objects.get(id=id)
            return render(request, 'employee/emp_details_edit.html', context)
        else:
            context['formWork'] = WorkDetailsForm(request.POST, instance=obj_emp)
            messages.warning(request, formWork.errors)
            return render(request, 'employee/emp_details_edit.html', context)
    if (request.method == 'POST') and ('btn_lastEmp' in request.POST):
        context['activeTab_No'] = 3
        formEmp = LastEmploymentForm(request.POST, instance=obj_emp)
        if formEmp.is_valid():
            formEmp.save()
            obj_emp = Employee.objects.get(id=id)
            obj_emp.MODIFIED_BY = request.user.username
            obj_emp.LAST_MODIFIED = now()
            obj_emp.save()
            context['formEmp'] = LastEmploymentForm(instance=obj_emp)
            messages.success(request, "Data has been updated !!!")
            return render(request, 'employee/emp_details_edit.html', context)
        else:
            context['formEmp'] = LastEmploymentForm(request.POST, instance=obj_emp)
            messages.warning(request, formEmp.errors)
            return render(request, 'employee/emp_details_edit.html', context)
    if (request.method == 'POST') and ('btn_Bank' in request.POST):
        context['activeTab_No'] = 4
        formBank = BankDetailsForm(request.POST, instance=obj_emp)
        if formBank.is_valid():
            formBank.save()
            obj_emp = Employee.objects.get(id=id)
            obj_emp.MODIFIED_BY = request.user.username
            obj_emp.LAST_MODIFIED = now()
            # Converting to upper case
            obj_emp.BANK_NAME = obj_emp.BANK_NAME.upper() if obj_emp.BANK_NAME else None
            obj_emp.IFSC_CODE = obj_emp.IFSC_CODE.upper() if obj_emp.IFSC_CODE else None
            obj_emp.BANK_BRANCH_NAME = obj_emp.BANK_BRANCH_NAME.upper() if obj_emp.BANK_BRANCH_NAME else None
            obj_emp.PAN_CARD_NUMBER = obj_emp.PAN_CARD_NUMBER.upper() if obj_emp.PAN_CARD_NUMBER else None
            obj_emp.save()
            context['formBank'] = BankDetailsForm(instance=obj_emp)
            messages.success(request, "Data has been updated !!!")
            return render(request, 'employee/emp_details_edit.html', context)
        else:
            context['formBank'] = BankDetailsForm(request.POST, instance=obj_emp)
            messages.warning(request, formBank.errors)
            return render(request, 'employee/emp_details_edit.html', context)
    if (request.method == 'POST') and ('btn_Docs' in request.POST):
        context['activeTab_No'] = 5
        formDocs = EmployeeDocumentsForm(request.POST, request.FILES)
        # files = request.FILES.getlist('DOCUMENTS')
        # files = request.FILES['DOCUMENTS']
        if formDocs.is_valid():
            attachment = formDocs.cleaned_data['DOCUMENTS']
            if attachment.size > settings.MAX_UPLOAD_SIZE:
                messages.warning(request, "Document size exceeded. Please Check !!!")
                formDocs = EmployeeDocumentsForm(request.POST)
                context['formDocs'] = formDocs
                return render(request, 'employee/emp_details_edit.html', context)
            else:
                obj = formDocs.save(commit=False)
                obj.save()
                doc_id = obj.pk
                obj_doc = EmployeeDocuments.objects.get(id=doc_id)
                obj_doc.UPLOADED_BY = request.user.username
                obj_doc.save()
                formDocs = EmployeeDocumentsForm()
                context['obj_emp_docs'] = EmployeeDocuments.objects.filter(EMPLOYEE_CODE_id=id).order_by('-UPLOAD_TIMESTAMP')
                context['formDocs'] = formDocs
                messages.success(request, "Documents has been uploaded !!!")
                return render(request, 'employee/emp_details_edit.html', context)
        else:
            context['formDocs'] = EmployeeDocumentsForm(request.POST)
            messages.warning(request, formDocs.errors)
            return render(request, 'employee/emp_details_edit.html', context)
    return render(request, 'employee/emp_details_edit.html', context)


@login_required
def employee_list(request):
    obj_emp = Employee.objects.all().order_by('pk')
    if (request.method == 'GET') and ('btn_search' in request.GET):
        searchText = request.GET.get('searchText')
        if searchText:
            obj_emp = Employee.objects.filter(Q(EMPLOYEE_CODE=searchText) |
                                              Q(EMPLOYEE_FULL_NAME__icontains=searchText) |
                                              Q(FIRST_NAME__icontains=searchText) |
                                              Q(MIDDLE_NAME__icontains=searchText) |
                                              Q(LAST_NAME__icontains=searchText)).order_by('pk')
        else:
            obj_emp = Employee.objects.all().order_by('pk')

    page = request.GET.get('page', 1)
    paginator = Paginator(obj_emp, 50)
    try:
        obj_emp = paginator.page(page)
    except PageNotAnInteger:
        obj_emp = paginator.page(1)
    except EmptyPage:
        obj_emp = paginator.page(paginator.num_pages)
    return render(request, 'employee/emp_list.html', {'obj_emp': obj_emp})


@login_required
def download_emp_docs(request, id=None):
    obj_emp_docs = EmployeeDocuments.objects.get(id=id)
    docs_path = os.path.join(settings.MEDIA_ROOT, str(obj_emp_docs.DOCUMENTS))
    if os.path.exists(docs_path):
        with open(docs_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename='+os.path.basename(docs_path)
            return response
    raise Http404


@login_required
def search_emp(request, id=None):
    emp_code = request.GET.get('empCode', None)
    if emp_code == '1111111':
        data = {'emp_name': 'SELF'}
    else:
        obj_emp = Employee.objects.filter(EMPLOYEE_CODE=emp_code).first()
        if obj_emp:
            if obj_emp.LAST_NAME:
                data = {'emp_name': obj_emp.FIRST_NAME + ' ' + obj_emp.LAST_NAME}
            else:
                data = {'emp_name': obj_emp.FIRST_NAME}
        else:
            data = {'emp_name': ''}
    return JsonResponse(data)


def emp_view(request, id=None):
    obj_emp = Employee.objects.get(id=id)
    obj_emp_docs = EmployeeDocuments.objects.filter(EMPLOYEE_CODE_id=id).order_by('-UPLOAD_TIMESTAMP')
    context = {
        'obj_emp': obj_emp,
        'obj_emp_docs': obj_emp_docs,
        'activeTab_No': 1,
    }
    return render(request, 'employee/emp_details_view.html', context)

