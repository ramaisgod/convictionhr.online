from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse, Http404
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
def client_registration(request, id=None):
    context = {
        'form': ClientRegistrationForm(),
        'formAdd': ClientAddressForm(),
        'formDocs': ClientDocumentsForm()
    }
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            PAN_NUMBER = form.cleaned_data['PAN_NUMBER']
            obj_client = Client.objects.filter(PAN_NUMBER=PAN_NUMBER.upper())
            if len(obj_client) > 0:
                context['form'] = ClientRegistrationForm(request.POST)
                messages.warning(request, "Already registered !!!")
                return render(request, 'client/client_registration.html', context)
            else:
                obj.save()
                id = obj.pk
                context['id'] = id
                obj_client = Client.objects.get(id=id)
                obj_client.REGISTERED_BY = request.user.username
                # Converting to upper case
                obj_client.PAN_NUMBER = obj_client.PAN_NUMBER.upper() if obj_client.PAN_NUMBER else None
                obj_client.GSTIN_NUMBER = obj_client.GSTIN_NUMBER.upper() if obj_client.GSTIN_NUMBER else None
                contract_start_date = obj_client.CONTRACT_START_DATE
                obj_client.CUSTOMER_CODE = 'C' + str(id).zfill(3)
                obj_client.save()
                obj_client = Client.objects.get(id=id)
                context['form'] = ClientRegistrationForm(instance=obj_client)
                context['obj_client'] = obj_client
                context['activeTab_No'] = 1
                messages.success(request, f"Registration Success !!! Customer Code is {obj_client.CUSTOMER_CODE}")
                # Create User
                try:
                    obj_user = User.objects.create_user(username=obj_client.CUSTOMER_CODE,
                                                        password="Welcome@" + str(obj_client.CUSTOMER_CODE),
                                                        user_type=2,
                                                        first_name=obj_client.CUSTOMER_CODE)
                    messages.success(request, "User account has been created.")
                except Exception as e:
                    print(e)
                return HttpResponseRedirect(f'/client/{id}/details/')
        else:
            context['form'] = ClientRegistrationForm(request.POST)
            messages.warning(request, form.errors)
            return render(request, 'client/client_registration.html', context)
    return render(request, 'client/client_registration.html', context)


@login_required
def client_info(request, id=None):
    obj_client = Client.objects.get(id=id)
    obj_client_docs = ClientDocuments.objects.filter(CUSTOMER_CODE_id=id).order_by('-UPLOAD_TIMESTAMP')
    obj_spoc = ClientSPOC.objects.filter(CUSTOMER_id=id).order_by('-TIMESTAMP')
    context = {
        'form': ClientRegistrationForm(instance=obj_client),
        'obj_client': obj_client,
        'obj_client_docs': obj_client_docs,
        'obj_spoc': obj_spoc,
        'formAdd': ClientAddressForm(instance=obj_client),
        'formDocs': ClientDocumentsForm(),
        'activeTab_No': 1,
    }
    if (request.method == 'POST') and ('btn_basicDetails' in request.POST):
        context['activeTab_No'] = 1
        form = ClientRegistrationForm(request.POST, instance=obj_client)
        if form.is_valid():
            form.save()
            obj_client = Client.objects.get(id=id)
            obj_client.MODIFIED_BY = request.user.username
            obj_client.LAST_MODIFIED = now()
            # Converting to upper case
            obj_client.PAN_NUMBER = obj_client.PAN_NUMBER.upper() if obj_client.PAN_NUMBER else None
            obj_client.GSTIN_NUMBER = obj_client.GSTIN_NUMBER.upper() if obj_client.GSTIN_NUMBER else None
            obj_client.save()
            messages.success(request, "Data has been updated !!!")
            return render(request, 'client/client_details_edit.html', context)
        else:
            context['form'] = ClientRegistrationForm(request.POST, instance=obj_client)
            messages.warning(request, form.errors)
            return render(request, 'client/client_details_edit.html', context)
    if (request.method == 'POST') and ('btn_Address' in request.POST):
        context['activeTab_No'] = 2
        formAdd = ClientAddressForm(request.POST, instance=obj_client)
        if formAdd.is_valid():
            same_add = formAdd.cleaned_data['BOTH_ADDRESS_SAME']
            formAdd.save()
            obj_client = Client.objects.get(id=id)
            obj_client.MODIFIED_BY = request.user.username
            obj_client.LAST_MODIFIED = now()
            # Converting to upper case
            obj_client.CORPORATE_CITY = obj_client.CORPORATE_CITY.upper() if obj_client.CORPORATE_CITY else None
            obj_client.CORPORATE_STATE = obj_client.CORPORATE_STATE.upper() if obj_client.CORPORATE_STATE else None
            obj_client.CORPORATE_COUNTRY = obj_client.CORPORATE_COUNTRY.upper() if obj_client.CORPORATE_COUNTRY else None
            obj_client.save()
            if same_add == 'on':
                obj_client.BOTH_ADDRESS_SAME = 'YES'
                obj_client.BILLING_ADDRESS = obj_client.CORPORATE_ADDRESS
                obj_client.BILLING_CITY = obj_client.CORPORATE_CITY
                obj_client.BILLING_STATE = obj_client.CORPORATE_STATE
                obj_client.BILLING_PINCODE = obj_client.CORPORATE_PINCODE
                obj_client.BILLING_COUNTRY = obj_client.CORPORATE_COUNTRY
                obj_client.save()
            else:
                obj_client.BOTH_ADDRESS_SAME = 'NO'
                obj_client.save()
            context['formAdd'] = ClientAddressForm(instance=obj_client)
            messages.success(request, "Data has been updated !!!")
            return render(request, 'client/client_details_edit.html', context)
        else:
            context['formAdd'] = ClientAddressForm(request.POST, instance=obj_client)
            messages.warning(request, formAdd.errors)
            return render(request, 'client/client_details_edit.html', context)
    if (request.method == 'POST') and ('btn_Docs' in request.POST):
        context['activeTab_No'] = 3
        formDocs = ClientDocumentsForm(request.POST, request.FILES)
        if formDocs.is_valid():
            attachment = formDocs.cleaned_data['DOCUMENTS']
            if attachment.size > settings.MAX_UPLOAD_SIZE:
                messages.warning(request, "Document size exceeded. Please Check !!!")
                formDocs = ClientDocumentsForm(request.POST, request.FILES)
                context['formDocs'] = formDocs
                return render(request, 'client/client_details_edit.html', context)
            else:
                obj = formDocs.save(commit=False)
                obj.save()
                doc_id = obj.pk
                obj_docs = ClientDocuments.objects.get(id=doc_id)
                obj_docs.UPLOADED_BY = request.user.username
                obj_docs.save()
                context['obj_client_docs'] = ClientDocuments.objects.filter(CUSTOMER_CODE_id=id).order_by('-UPLOAD_TIMESTAMP')
                formDocs = ClientDocumentsForm()
                context['formDocs'] = formDocs
                messages.success(request, "Documents has been uploaded !!!")
                return render(request, 'client/client_details_edit.html', context)
        else:
            context['formDocs'] = ClientDocumentsForm(request.POST)
            messages.warning(request, formDocs.errors)
            return render(request, 'client/client_details_edit.html', context)
    return render(request, 'client/client_details_edit.html', context)


@login_required
def client_list(request):
    obj_client = Client.objects.all().order_by('pk')
    if (request.method == 'GET') and ('btn_search' in request.GET):
        searchText = request.GET.get('searchText')
        if searchText:
            obj_client = Client.objects.filter(Q(CUSTOMER_CODE=searchText) |
                                              Q(CUSTOMER_NAME__icontains=searchText)).order_by('pk')
        else:
            obj_client = Client.objects.all().order_by('pk')
    page = request.GET.get('page', 1)
    paginator = Paginator(obj_client, 50)
    try:
        obj_client = paginator.page(page)
    except PageNotAnInteger:
        obj_client = paginator.page(1)
    except EmptyPage:
        obj_client = paginator.page(paginator.num_pages)
    return render(request, 'client/client_list.html', {'obj_client': obj_client})


@login_required
def download_docs(request, id):
    obj_client_docs = ClientDocuments.objects.get(id=id)
    path = obj_client_docs.DOCUMENTS
    file_path = os.path.join(settings.MEDIA_ROOT, str(path))
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


# @login_required
# def download_docs(request, id=None, doc_id=None):
#     obj_client = Client.objects.get(id=id)
#     obj_client_docs = ClientDocuments.objects.get(id=doc_id)
#     docs_path = os.path.join(settings.MEDIA_ROOT, str(obj_client_docs.DOCUMENTS))
#     print(docs_path)
#     if os.path.exists(docs_path):
#         with open(docs_path, 'rb') as file:
#             response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = 'inline; filename='+os.path.basename(docs_path)
#             return response
#     # raise Http404


@login_required
def add_new_spoc(request, id=None):
    context = {
        'form': AddNewSPOCForm(),
    }
    if request.method == 'POST':
        form = AddNewSPOCForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            id = obj.pk
            context['id'] = id
            obj_spoc = ClientSPOC.objects.get(id=id)
            # Converting to upper case
            obj_spoc.LOCATION = obj_spoc.LOCATION.upper() if obj_spoc.LOCATION else None
            obj_spoc.PERSON_NAME = obj_spoc.PERSON_NAME.upper() if obj_spoc.PERSON_NAME else None
            obj_spoc.save()
            context['form'] = AddNewSPOCForm()
            context['obj_spoc'] = obj_spoc
            messages.success(request, "New SPOC Details has been added !!!")
            # return render(request, 'client/add_new_spoc.html', context)
            return HttpResponseRedirect(f'/client/{obj_spoc.CUSTOMER_id}/details/?activeTab=4')
        else:
            context['form'] = AddNewSPOCForm(request.POST)
            messages.warning(request, form.errors)
            return render(request, 'client/add_new_spoc.html', context)
    return render(request, 'client/add_new_spoc.html', context)


@login_required
def spoc_info(request, id=None):
    obj_spoc = ClientSPOC.objects.get(id=id)
    context = {
        'form': AddNewSPOCForm(instance=obj_spoc),
        'obj_spoc': obj_spoc,
    }
    if request.method == 'POST':
        form = AddNewSPOCForm(request.POST, instance=obj_spoc)
        if form.is_valid():
            form.save()
            obj_spoc = ClientSPOC.objects.get(id=id)
            # Converting to upper case
            obj_spoc.LOCATION = obj_spoc.LOCATION.upper() if obj_spoc.LOCATION else None
            obj_spoc.PERSON_NAME = obj_spoc.PERSON_NAME.upper() if obj_spoc.PERSON_NAME else None
            obj_spoc.save()
            context['form'] = AddNewSPOCForm(instance=obj_spoc)
            messages.success(request, "Data has been updated !!!")
            return HttpResponseRedirect(f'/client/{obj_spoc.CUSTOMER_id}/details/?activeTab=4')
        else:
            context['form'] = AddNewSPOCForm(request.POST, instance=obj_spoc)
            messages.warning(request, form.errors)
            return render(request, 'client/view_spoc.html', context)
    return render(request, 'client/view_spoc.html', context)


def client_view(request, id=None):
    obj_client = Client.objects.get(id=id)
    obj_client_docs = ClientDocuments.objects.filter(CUSTOMER_CODE_id=id).order_by('-UPLOAD_TIMESTAMP')
    obj_spoc = ClientSPOC.objects.filter(CUSTOMER_id=id).order_by('-TIMESTAMP')
    context = {
        'obj_client': obj_client,
        'obj_client_docs': obj_client_docs,
        'obj_spoc': obj_spoc,
        'activeTab_No': 1,
    }
    return render(request, 'client/client_details_view.html', context)
