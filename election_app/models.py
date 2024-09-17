from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

def check_duplicate_titles(sender, instance, **kwargs):
    existing_titles = Election.objects.filter(title=instance.title)
    if existing_titles.exists():
        instance.id = existing_titles.first().id  # Use the existing title's ID

class Candidate(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
    def clean(self):
        # Check for duplicate candidates with the same name
        existing_candidate = Candidate.objects.filter(name=self.name).exclude(id=self.id).first()
        if existing_candidate:
            raise ValidationError("A candidate with this name already exists.")



class Election(models.Model):
    ELECTION_TYPES = [
        ('President', 'President'),
        ('Vice-President', 'Vice-President'),
        ('Senators', 'Senators'),
    ]
    
    title = models.CharField(max_length=100, choices=ELECTION_TYPES)
    candidates = models.ManyToManyField(Candidate)  # Assuming Candidate is the name of your Candidate model
    is_voting_open = models.BooleanField(default=True)
    def __str__(self):
        return self.title
        
@receiver(pre_save, sender=Election)
def check_duplicate_titles(sender, instance, **kwargs):
    existing_titles = Election.objects.filter(title=instance.title)
    if existing_titles.exists():
        instance.id = existing_titles.first().id
    def __str__(self):
        return self.title
    
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} voted for {self.candidate.name}"

