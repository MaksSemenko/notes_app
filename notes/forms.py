from django import forms
from .models import Category, Note


class NoteForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={'cols': '40', 'rows': '1'}), max_length=200)
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': '40', 'rows': '6'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    reminder = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def save(self):
        note = Note()
        note.title = self.cleaned_data['title']
        note.text = self.cleaned_data['text']
        note.category = self.cleaned_data['category']
        note.reminder = self.cleaned_data['reminder']
        return note