from django.shortcuts import render
from .models import Topic
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import TopicForm, EntryForm, Entry
from django.contrib.auth.decorators import login_required
import random

def index(request):
    """Home Page"""

    motivation = [
        ["Dwa najważniejsze dni Twojego życia to ten, w którym się urodziłeś oraz ten, w którym dowiedziałeś się, po co.","Mark Twain"],
        ["Twoje życie staje się lepsze, tylko, gdy Ty stajesz się lepszym.", "Brian Tracy"],
        ["Pudłujesz 100% strzałów, jeśli w ogóle ich nie wykonujesz.", "Wayne Gretzky"],
        ["Najlepszą zemstą jest ogromny sukces.", "Frank Sinatra"],
        ["Twój czas jest ograniczony, więc nie marnuj go na byciem kimś, kim nie jesteś."," Steve Jobs"],
        ["Aby zer­wać z na­wykiem, wyrób so­bie in­ny, który go wymaże.","Mark Twain"],
        ["Na szczycie zawsze znajdzie się miejsce.","Daniel Webster"],
        ["Człowiek, który goni dwa zające nie złapie ani jednego.","Konfucjusz"],
        ["Za dwadzieścia lat bar­dziej będziesz żałował te­go, cze­go nie zro­biłeś, niż te­go, co zro­biłeś. Więc od­wiąż li­ny, opuść bez­pie­czną przys­tań. Złap w żag­le po­myślne wiat­ry. Podróżuj, śnij, od­kry­waj.","Mark Twain"],
        ["Nie ma nic złego w świętowaniu sukcesu, ale ważniejsze jest wyciągnięcie nauki z porażki","Bill Gates"],
        ["Nic nie jest podawane na tacy – każdy zawsze trafia na jakieś przeszkody po drodze. Kiedy się pojawią, zastanów się jak je pokonać, a nie myśl o tym, że to już koniec drogi.","Michael Jordan"]
    ]

    quotes = random.choice(motivation)

    context = {'cytat': quotes[0], 'autor': quotes[1]}
    return render(request, 'learning_logs/index.html', context)


@login_required
def topics(request):
    """View all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """View single topic and every related entries"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Add new topic"""
    if request.method != 'POST':
        # Then no data , we should create an empty form
        form = TopicForm()
    else:
        # Data in request so we should process this data
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add new entry """
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # No parameters
        form = EntryForm()
    else:
        # Parameters exists
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        """Aktual data in form"""
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
