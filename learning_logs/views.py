from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner = request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Show a single topic and all of its entries"""
    topic = Topic.objects.get(id = topic_id)
    
    #Make sure the topic belongs to the current user.
    check_topic_owner(request, topic)
    
    entries = topic.entry_set.order_by('-date_added')
    #THE LOWERCASE ENTRY IS REFERENCING THE ENTRY CLASS IN THE MODELS.PY FILE.
    #IF YOU WANT TO USE FOREIGN_KEYS PROPERLY AND GRAB MANY ITEMS ASSOCIATED TO A SINGLE PIZZA OR TOPIC FOR EXAMPLE
    #YOU WOULD GO (name goes here).(LOWERCASE CLASS NAME)_set.
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        #No data submitted; create a blank form
        #When the User first hits or enters this page their browser is sending a GET request
        #So this is triggered when first hitting the page. If the user submits a form then that is a POST request
        form = TopicForm()

    else:
        #POST data submitted; process data
        form = TopicForm(data = request.POST)
        if form.is_valid():
            new_topic = form.save(commit = False)
            new_topic.owner = request.user
            new_topic.save()
            #The save method writes this to the DB
            return redirect('learning_logs:topics')
            #I think this redirect is saying use the the topics function above which calls a new HTML page to redirect you to.


    #Display a blank or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)
    
    #Make sure the topic belongs to the current user before alowing new entries.
    check_topic_owner(request, topic)
    
    #Grabbing an individual topic

    if request.method != 'POST':
        #No data submitted; create a blank form
        form = EntryForm()

    else:
        #POST data submitted; process data.
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id = topic_id)
            #Telling it to call the topic function above

    #Display a blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic
    
    #Make sure the topic belongs to the current user.
    check_topic_owner(request, topic)

    if request.method != 'POST':
        #Initial request; pre-fill form with the current entry.
        form = EntryForm(instance = entry)
    else:
        #POST data submitted; process data
        form = EntryForm(instance = entry, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id = topic.id)
            #Telling it to call the topic function above

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context) 


def check_topic_owner(request, topic):
    #Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404