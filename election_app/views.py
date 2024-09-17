from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CandidateForm, ElectionForm, VoteForm
from .models import Candidate, Election, Vote
from django.db.models import Count


def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def election_results(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    
    if not election.is_voting_open and request.user.is_superuser:
        candidates = election.candidates.all()
        results = []

        for candidate in candidates:
            vote_count = Vote.objects.filter(candidate=candidate).count()
            results.append({'candidate': candidate, 'vote_count': vote_count})

        print("Candidates:", candidates)  # Debugging line
        print("Results:", results)  # Debugging line

        # Determine the winner based on the maximum vote count
        winner = None
        max_vote_count = 0
        
        for result in results:
            if result['vote_count'] > max_vote_count:
                max_vote_count = result['vote_count']
                winner = result['candidate']

        print("Winner:", winner.name if winner else "No winner")  # Debugging line

        context = {
            'election': election,
            'results': results,
            'winner': winner,
        }

        return render(request, 'election_app/election_results.html', context)
    else:
        # Redirect or show an error message if conditions aren't met
        return HttpResponse("Election results are not available for this election.")


def voting_success_view(request):
    return render(request, 'election_app/voting_success.html')
    

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        
        if user.is_staff:
            return redirect('create_election')
        else:
            return redirect('election_list')

def index(request):
    return render(request, 'election_app/index.html')


@login_required
def create_candidate_and_election(request):
    candidate_form = CandidateForm(request.POST)
    election_form = ElectionForm(request.POST)
    message = None

    if request.method == 'POST':
        if candidate_form.is_valid() and election_form.is_valid():
            candidate = candidate_form.save()
            election = election_form.save(commit=False)
            election.save()

            # Clear form fields after successful submission
            candidate_form = CandidateForm()
            election_form = ElectionForm()

            message = f"Candidate '{candidate.name}' and Election for '{election.title}' were successfully created."

    context = {
        'candidate_form': candidate_form,
        'election_form': election_form,
        'message': message,
    }

    return render(request, 'election_app/create_election.html', context)



@login_required
def vote(request, election_id):
    election = get_object_or_404(Election, pk=election_id)

    if not election.is_voting_open:
        messages.warning(request, 'Voting for this election has ended.')
        return redirect('index')

    if request.method == 'POST':
        vote_form = VoteForm(request.POST)
        if vote_form.is_valid():
            candidate = vote_form.cleaned_data['candidate']
            Vote.objects.create(user=request.user, candidate=candidate)
            return redirect('voting_success')
    else:
        # Filter candidates based on the election's title
        candidates = Candidate.objects.filter(election__title=election.title)
        vote_form = VoteForm()

    context = {
        'election': election,
        'candidates': candidates,
        'vote_form': vote_form,
    }

    return render(request, 'election_app/vote.html', context)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log in the user after registration
            login(request, user)
            return redirect('election_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
    
@login_required  
def election_list(request):
    elections = Election.objects.all()
    return render(request, 'election_app/election_list.html', {'elections': elections})
@login_required
def close_election(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    
    if not election.is_voting_open:
        
        # Election is already closed, redirect to the election list
        return redirect('election_list')
    
    # Close the election
    election.is_voting_open = False
    election.save()
    # Redirect to the election results page
    return redirect('election_results', election_id=election_id)
    
@login_required
def election_detail(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    candidates = election.candidates.all()
    return render(request, 'election_app/election_detail.html', {'election': election, 'candidates': candidates})
    
def check_candidate_name(request):
    candidate_name = request.GET.get('name')
    exists = Candidate.objects.filter(name=candidate_name).exists()
    return JsonResponse({'exists': exists})

def delete_election(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    
    # Check if the user is authenticated and is a superuser
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            election.delete()
            return redirect('election_list')  # Redirect to the list of elections after deletion
    
    return render(request, 'election_app/delete_confirmation.html', {'election': election})