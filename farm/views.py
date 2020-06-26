from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.generic import (ListView, DetailView, CreateView, FormView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER

from datetime import datetime

from . import models
from . import forms
from processing.models import ProcessedData
from processing.mask import Mask


def home_view(request):
    return render(request, 'farm/home.html')


class FarmListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = models.Farm
    queryset = models.Farm.objects.all()
    template_name = "farm/farm_list.html"
    context_object_name = "farms"

    def get_context_data(self, **kwargs):
        context = super(FarmListView, self).get_context_data(**kwargs)
        context['users'] = get_user_model().objects.all()
        return context


class FarmDetailView(DetailView):
    model = models.Farm
    template_name = 'farm/farm_detail.html'
    context_object_name = "farm"

    def get_context_data(self, **kwargs):
        context = super(FarmDetailView, self).get_context_data(**kwargs)
        context['data'] = models.Picture.objects.filter(farm_id=self.kwargs['pk'])
        context['processed_data'] = ProcessedData.objects.filter(farm_id=self.kwargs['pk'])
        context['coordinates'] = models.Coordinates.objects.filter(farm=self.kwargs['pk'])
        context['data_form'] = forms.PictureForm
        return context


class FarmCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = models.Farm
    template_name = 'farm/farm_create.html'
    form_class = forms.FarmForm



class FarmUpdateView(UpdateView):

    model = models.Farm
    template_name = 'farm/farm_update.html'
    form_class = forms.FarmForm


class PictureCreateView(CreateView):

    model = models.Picture
    template_name = 'farm/farm_data_upload.html'
    form_class = forms.PictureForm

    def get_context_data(self, **kwargs):
        context = super(PictureCreateView, self).get_context_data(**kwargs)
        context['farm'] = models.Farm.objects.get(id=self.kwargs['pk'])
        return context


def data_fetch_view(request):

    request_date = request.GET.get('date')
    request_type = request.GET.get('type')
    # request_date = datetime.strptime(request_date, '%b. %d, %Y, %I:%M %p')



    # data = models.Picture.objects.get(uploaded_on=request_date)
    # # ProcessedData.objects.get(picture=date)
    print(request_date)

    return JsonResponse({"msg": "Request Success"})

# def picture_upload_form(request):
#
#     if request.method == 'POST':
#         form = forms.PictureForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             form.save()
#             return JsonResponse({"msg": "Data Uploaded"})
#     else:
#         form = forms.PictureForm()
#     return render(request, 'farm/farm_data_upload.html', {'form': form, 'farm_id': 6})


def farm_search_view(request):

    title = 'Search Farm'
    form = forms.FarmSearchForm()

    if request.method == 'POST':
        form = forms.FarmSearchForm(request.POST)

        if form.is_valid():

            lookup_id = form.cleaned_data['farm_lookup']
            farm = models.Farm.objects.filter(farm_lookup=lookup_id).first()
            if farm:
                request.user.managed_farms.add(farm)
                return redirect('farm-detail', pk=farm.pk)
            else:
                context = {
                    'title': title,
                    'form': form
                }
                # messages.warning(request, f'No such tickets exist')
                return render(request, "farm/farm_search.html", context)
        else:
            form = forms.FarmSearchForm()
            context = {'title': 'Search Farm', 'form': form}
            return render(request, "farm/farm_search.html", context)

    return render(request, "farm/farm_search.html", {'title': title, 'form': form})


def add_coordinates_view(request):

    if request.method == 'POST':
        print("Post Method")

    farm = models.Farm.objects.get(id=request.GET.get('farm_id'))
    coordniates = models.Coordinates(
        farm=farm,
        longitude=request.GET.get('longitude'),
        latitude=request.GET.get('latitude')
    )
    coordniates.save();

    return JsonResponse({"msg": "Coordinates Added"})


def get_mask_view(request):

    data = models.Picture.objects.get(id=request.GET.get('data-id'))
    mask = Mask('farm/media/' + str(data.resource_NIR), 'farm/media/' + str(data.resource_RED))

    response = {'green_thresh': mask.green_threshold(), 'red_thresh': mask.red_threshold()}

    return JsonResponse(response)












