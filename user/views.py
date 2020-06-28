from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, FormView
from django.http import JsonResponse
from mysite.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from collections import defaultdict

from .forms import UserRegisterForm, ForgetPasswordForm
from farm.models import Coordinates

@login_required
def profile(request):

    User = get_user_model().objects.get(id=request.user.id)
    return render(request, 'user/profile.html')


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'user/signup.html'
    success_url = '/farms'


# class ForgetPasswordView(FormView):
#     form_class = ForgetPasswordForm
#     template_name = 'user/forget-password.html'
#     success_url = '/'
#
#     def form_valid(self, form):
#
#         subject = 'Password Reset'
#         message = 'test'
#         recp = self.request.POST.get('email')
#         send_mail(subject, message, EMAIL_HOST_USER, [recp], fail_silently=False)
#         return super().form_valid(form)

class ChangePasswordView(FormView):
    form_class = PasswordChangeForm
    template_name = 'user/password-change.html'
    success_url = '/login'

    def get_form_kwargs(self):
        kwargs = super(ChangePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


def farm_coordinates(request):
    user = get_user_model().objects.get(id=request.GET.get('user_id'))
    managed_farms = user.managed_farms.all()
    context = defaultdict(list)

    for farm in managed_farms:
        context["farm_list"].append(farm.farm_name)
        coordinates = Coordinates.objects.filter(farm=farm.id)

        for coordinate in coordinates:
            context[farm.farm_name].append(coordinate.longitude + "," + coordinate.latitude)

    return JsonResponse(context)







# def register_view(request):
#     form = UserRegisterForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     if form.is_valid():
#         form.save()
#
#     return render(request, 'user/signup.html', context)
