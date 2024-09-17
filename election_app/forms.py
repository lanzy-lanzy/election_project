from django import forms
from .models import Candidate, Election

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = instance.name.capitalize()  # Capitalize the name before saving
        if commit:
            instance.save()
        return instance

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['title']
        widgets = {
            'title': forms.Select(choices=Election.ELECTION_TYPES),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.title = instance.title.capitalize()  # Capitalize the title before saving
        if commit:
            instance.save()
        return instance

class VoteForm(forms.Form):
    candidate = forms.ModelChoiceField(queryset=Candidate.objects.all(), label='Select a Candidate')

# Note: The VoteForm doesn't require overriding save since it doesn't save to the database
