from django.views.generic import TemplateView, DetailView, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

import nexmo

from .models import TwoFactor

class NewView(LoginRequiredMixin, DetailView):
    template_name = 'two_factor/new.html'

    def get_object(self):
        try:
            return self.request.user.twofactor
        except TwoFactor.DoesNotExist:
            return TwoFactor.objects.create(user=self.request.user)



class CreateView(LoginRequiredMixin, View):
    def post(self, request):
        number = self.find_or_set_number(request)
        response = self.send_verification_request(request, number)

        if (response['status'] == '0'):
            request.session['verification_id'] = response['request_id']
        else:
            logout(request)
            messages.add_message(request, messages.INFO, 'Could not verify your number. Please contact support.')
            return HttpResponseRedirect('/')

        return HttpResponseRedirect(reverse('two_factor:verify')+"?next="+request.POST['next'])

    def find_or_set_number(self, request):
        two_factor = request.user.twofactor

        if (not two_factor.number):
            two_factor.number = request.POST['number']
            two_factor.save()

        return two_factor.number

    def send_verification_request(self, request, number):
        client = nexmo.Client()
        return client.start_verification(number=number, brand='Pollstr')


class VerifyView(LoginRequiredMixin, TemplateView):
    template_name = 'two_factor/verify.html'

class ConfirmView(LoginRequiredMixin, View):
    def post(self, request):
        response = self.check_verification_request(request)

        if (response['status'] == '0'):
            request.session['verified'] = True
            return HttpResponseRedirect(request.POST['next'])
        else:
            messages.add_message(request, messages.INFO, 'Could not verify code. Please try again.')
            return HttpResponseRedirect(reverse('two_factor:verify')+"?next="+request.POST['next'])


    def check_verification_request(self, request):
        return nexmo.Client().check_verification(request.session['verification_id'], code=request.POST['code'])
