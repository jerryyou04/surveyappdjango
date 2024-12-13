import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Survey, Answer, QuestionAnswer
from .forms import DynamicForm
from django.db.models import Q

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
                response_data=response_data
            )

            # Save each question-answer as a separate entry in the QuestionAnswer model
            for field_name, user_answer in form.cleaned_data.items():
                question = next(
                    (q for q in form_structure if q.get("name") == field_name), None
                )
                if question:
                    issue = request.POST.get(f"issue_{field_name}")
                    action_taken = request.POST.get(f"action_{field_name}")

                    QuestionAnswer.objects.create(
                        survey=survey_instance,
                        question_id=question.get("id"),
                        question_text=question.get("label"),
                        answer = answer_instance,
                        response=user_answer,
                        issue=issue if user_answer == "No" else None,
                        action_taken=action_taken if user_answer == "No" else None
                    )
            
            return redirect('surveyapp:survey_success')
            #  # Store the Answer ID in a cookie
            # response = redirect('surveyapp:survey_success')

            # # Get existing submitted answer IDs from cookies
            # submitted_answers = request.COOKIES.get('submitted_answers', '[]')
            # submitted_answers = json.loads(submitted_answers)

            # # Add the new Answer ID
            # submitted_answers.append(answer_instance.id)

            # # Keep only the last 5 submissions
            # submitted_answers = submitted_answers[-5:]

            # # Set the updated cookie (expires in 1 year)
            # response.set_cookie('submitted_answers', json.dumps(submitted_answers), max_age=31536000)

            # return response
    else:
        form = DynamicForm(form_structure=form_structure)

    return render(request, 'surveyapp/display_survey.html', {'form': form, 'survey_instance': survey_instance})


def survey_success(request):
    return render(request, 'surveyapp/survey_success.html')

def survey_list(request):
    search_query = request.GET.get("search", "").strip()

    # Retrieve all surveys
    surveys = Survey.objects.all()
    print(f"All Surveys: {surveys}")

    if search_query:
        # Split the search query into individual terms
        search_terms = search_query.split()
        print(f"Search Terms: {search_terms}")

        # Build Q objects to match all terms across name and cell fields
        survey_search_q = Q()
        for term in search_terms:
            survey_search_q &= Q(name__icontains=term.strip()) | Q(cell__icontains=term.strip())

        # Filter surveys based on the combined Q object
        surveys = surveys.filter(survey_search_q)
        print(f"Filtered Surveys: {surveys}")

    # For AJAX request: filter answers and return JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        answers = Answer.objects.all()

        if search_query:
            answer_search_q = Q()
            for term in search_terms:
                answer_search_q &= Q(survey__name__icontains=term) | Q(survey__cell__icontains=term)

            # Apply the filter to answers and get the latest 5 matches
            answers = answers.filter(answer_search_q).order_by('-submitted_at')[:5]
        else:
            # If no search term, get the latest 5 answers
            answers = answers.order_by('-submitted_at')[:5]

        # Serialize answers to JSON
        answers_data = [
            {
                'survey_name': answer.survey.name,
                'survey_cell': answer.survey.cell,
                'submitted_at': answer.submitted_at.strftime("%Y-%m-%d %H:%M:%S"),
                'response_data': answer.response_data
            }
            for answer in answers
        ]

        return JsonResponse({'answers': answers_data})

    # Regular page load
    return render(request, "surveyapp/survey.html", {
        "surveys": surveys,
        "answers": Answer.objects.all().order_by('-submitted_at')[:5],
    })




def index(request):
    return render(request, 'surveyapp/index.html')
