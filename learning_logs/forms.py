from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
        #We're importing the Topic model defined in the models file, using it as a template, and telling this that the only field we want from Topics is the text field. Not the date_added.
        #Then we want this text key in the label dictionary to not have a value paired with it

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
        #Here we are telling Django to expand the number of columns in the text box to 80. Instead of the default 40