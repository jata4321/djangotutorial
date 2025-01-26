from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from wildewidgets import HorizontalStackedBarChart

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-publication_date')[:5]

    def get_context_data(self, **kwargs):
        barchart = HorizontalStackedBarChart(title="New Customers Through July", money=True, legend=True, width='500', color=False)
        barchart.set_categories(["January", "February", "March", "April", "May", "June", "July"])
        barchart.add_dataset([75, 44, 92, 11, 44, 95, 35], "Central")
        barchart.add_dataset([41, 92, 18, 35, 73, 87, 92], "Eastside")
        barchart.add_dataset([87, 21, 94, 13, 90, 13, 65], "Westside")
        kwargs['barchart'] = barchart
        return super().get_context_data(**kwargs)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question,
                                                     'error_message': "You didn't select a choice."})
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))

def home(request):
    return render(request, 'polls/home.html')
# Create your views here.
