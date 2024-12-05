import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Survey, Answer, QuestionAnswer
from .forms import DynamicForm


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

                    # Save each question-answer as a separate entry in the QuestionAnswer model
                    QuestionAnswer.objects.create(
                        survey=survey_instance,
                        question_id=question.get("id"),
                        question_text=question.get("label"),
                        answer=user_answer,
                        issue=issue if user_answer == "No" else None,
                        action_taken=action_taken if user_answer == "No" else None
                    )

            # Save the response in the Answer model
            Answer.objects.create(
                survey=survey_instance,
                response_data=response_data
            )

            return redirect('surveyapp:survey_success')
    else:
        form = DynamicForm(form_structure=form_structure)

    return render(request, 'surveyapp/display_survey.html', {'form': form, 'survey': survey_instance})

def survey_success(request):
    return render(request, 'surveyapp/survey_success.html')
    
def survey_list(request):
    search_query = request.GET.get("search", "")  # Get the search term from the URL
    if search_query:
        surveys = Survey.objects.filter(name__icontains=search_query)  # Filter by name
    else:
        surveys = Survey.objects.all()  # Show all surveys if no search term
    return render(request, "surveyapp/survey.html", {"surveys": surveys, "search_query": search_query})


def index(request):
    return render(request, 'surveyapp/index.html')


    
# def display_survey(request, survey_id):
#     # Retrieve the survey instance
#     survey_instance = get_object_or_404(Survey, pk=survey_id)

#     # Deserialize the survey structure if it's a string
#     form_structure = survey_instance.structure
#     if isinstance(form_structure, str):
#         try:
#             form_structure = json.loads(form_structure)
#         except json.JSONDecodeError:
#             raise ValueError("Invalid JSON structure for survey ID {survey_id}")

#     # Extract questions from the form structure
#     if isinstance(form_structure, dict) and "questions" in form_structure:
#         form_structure = form_structure["questions"]

#     # Create the form
#     if request.method == 'POST':
#         form = DynamicForm(request.POST, form_structure=form_structure)
#         if form.is_valid():
#             # Save the response
#             Answer.objects.create(
#                 survey=survey_instance,
#                 response_data=form.cleaned_data
#             )
#             # Save each question-answer as a separate entry in the QuestionAnswer model
#             for field_name, user_answer in form.cleaned_data.items():
#                 # Find the corresponding question in the survey structure
#                 question = next(
#                     (q for q in form_structure if q.get("name") == field_name), None
#                 )
#                 if question:
#                     QuestionAnswer.objects.create(
#                         survey=survey_instance,
#                         question_id=question.get("id"),
#                         question_text=question.get("label"),
#                         answer=user_answer
#                     )

#             return redirect('surveyapp:survey_success')
#     else:
#         form = DynamicForm(form_structure=form_structure)

#     return render(request, 'surveyapp/display_survey.html', {'form': form, 'survey': survey_instance})

