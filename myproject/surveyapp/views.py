import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Survey, Answer, QuestionAnswer
from .forms import DynamicForm
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def display_survey(request, survey_id):
    # Retrieve the survey instance
    survey_instance = get_object_or_404(Survey, pk=survey_id)

    # Deserialize the survey structure if it's a string
    form_structure = survey_instance.structure
    if isinstance(form_structure, str):
        try:
            form_structure = json.loads(form_structure)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON structure for survey ID {survey_id}")

    # Extract questions from the form structure
    if isinstance(form_structure, dict) and "questions" in form_structure:
        form_structure = form_structure["questions"]

    # Create the form
    if request.method == 'POST':
        form = DynamicForm(request.POST, form_structure=form_structure)
        if form.is_valid():
            # Prepare the response data for the Answer model
            response_data = {}
            for field_name, user_answer in form.cleaned_data.items():
                # Find the corresponding question in the survey structure
                question = next(
                    (q for q in form_structure if q.get("name") == field_name), None
                )
                if question:
                    # Handle additional fields for "No" answers
                    issue = request.POST.get(f"issue_{field_name}")
                    action_taken = request.POST.get(f"action_{field_name}")

                    # Add the answer to the response_data JSON
                    response_data[field_name] = {
                        "answer": user_answer,
                        "issue": issue if user_answer == "No" else None,
                        "action_taken": action_taken if user_answer == "No" else None
                    }

            # Save the response in the Answer model
            answer_instance = Answer.objects.create(
                survey=survey_instance,
                response_data=response_data,
                user=request.user 
            )

            # Save each question-answer as a separate entry in the QuestionAnswer model
            for field_name, user_answer in form.cleaned_data.items():
                question = next(
                    (q for q in form_structure if q.get("name") == field_name), None
                )
                if question:
                    issue = request.POST.get(f"issue_{field_name}")
                    action_taken = request.POST.get(f"action_{field_name}")
                    if issue or action_taken:
                        status_by_admin = 'open'
                    else:
                        status_by_admin = 'closed'

                    QuestionAnswer.objects.create(
                        survey=survey_instance,
                        question_id=question.get("id"),
                        question_text=question.get("label"),
                        answer = answer_instance,
                        response=user_answer,
                        issue=issue if user_answer == "No" else None,
                        action_taken=action_taken if user_answer == "No" else None,
                        status_by_admin=status_by_admin,
                        user=request.user 
                    )
            
            return redirect('surveyapp:survey_success')

    else:
        form = DynamicForm(form_structure=form_structure)

    return render(request, 'surveyapp/display_survey.html', {'form': form, 'survey_instance': survey_instance})


def survey_success(request):
    return render(request, 'surveyapp/survey_success.html')


def survey_list(request):
    # Get the search query from the request
    search_query = request.GET.get("search", "").strip()

    # Retrieve all surveys and answers
    surveys = Survey.objects.all().order_by('sort_order', 'name', 'cell')
    answers = Answer.objects.all().order_by('-created_at')

    if search_query:
        # Split the search query into individual terms
        search_terms = search_query.split()

        # Build Q objects to match all terms across name and cell fields for surveys and answers
        survey_search_q = Q()
        answer_search_q = Q()

        for term in search_terms:
            survey_search_q &= Q(name__icontains=term) | Q(cell__icontains=term)
            answer_search_q &= Q(survey__name__icontains=term) | Q(survey__cell__icontains=term)

        # Filter surveys and answers based on the combined Q objects
        surveys = surveys.filter(survey_search_q)
        answers = answers.filter(answer_search_q)

    # Slice after filtering to get the latest 5 answers
    answers = answers[:5]
    surveys = surveys[:30]

    # Handle HTMX requests separately for surveys and answers
    if request.headers.get('HX-Request'):
        target = request.GET.get('target', '')
        if target == 'answers':
            return render(request, "surveyapp/partials/answers_list.html", {"answers": answers})
        return render(request, "surveyapp/partials/survey_list.html", {"surveys": surveys})

    # For a regular page load, render the full template
    return render(request, "surveyapp/survey.html", {
        "surveys": surveys[:30],  # Limit to 30 surveys for the full page load
        "answers": answers,
    })



def index(request):
    return render(request, 'surveyapp/index.html')

def show_conditional_fields(request, field_name):
    autofill_url = reverse('surveyapp:autofill_action', args=[field_name])
    return HttpResponse(f"""
        <div class="mb-3">
            <label for="issue_{field_name}" class="form-label">Please describe the issue:</label>
            <textarea id="issue_{field_name}" name="issue_{field_name}" class="form-control" rows="4" required></textarea>
        </div>

        <div class="mb-3">
            <label for="action_{field_name}" class="form-label">What action was taken?</label>
            <textarea id="action_{field_name}" name="action_{field_name}" class="form-control" rows="4" required></textarea>
        </div>

        <button type="button" class="btn btn-sm btn-primary mt-2" 
            hx-get="{autofill_url}" 
            hx-target="#action_{field_name}" 
            hx-swap="innerHTML">
            Autofill: Contacted Team Leader / Supervisor
        </button>
    """)

def autofill_action(request, field_name):
    return HttpResponse("Contacted Team Leader / Supervisor")

@login_required
def profile(request):
    return render(request, 'registration/profile.html')