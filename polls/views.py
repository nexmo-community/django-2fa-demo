from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Choice, Question

class IndexView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class OptionsView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Question
    template_name = 'polls/results.html'

class VoteView(LoginRequiredMixin,View):
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/details.html', {
                'question' : question,
                'error_message' : "You didn't select a choice"
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()

            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
