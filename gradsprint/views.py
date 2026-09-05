from django.shortcuts import get_object_or_404, render, redirect 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from collections import defaultdict

from .forms import RegisterForm 



from .models import Test, Section, StudentAnswer, TestResult

# Create your views here.

def register(request):
    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect("gradsprint:dashboard")
    else: 
        form = RegisterForm()
    return render(request, "gradsprint/register.html", 
                  {"form": form}
                )

        


def test_engine(request):
    return render(request, "gradsprint/test_engine.html")



@login_required
def dashboard(request):
    user = request.user

    answers = StudentAnswer.objects.filter(user=user
    ).select_related("question")
    
    test_results = TestResult.objects.filter(user=user
    ).select_related("test").order_by("-completed_at")

    #--------------------------
    #   GENERAL STATISTICS
    #--------------------------

    total_answered = answers.count()
    total_correct = answers.filter(is_correct=True).count()

    if total_answered>0:
        overall_accuracy = round(
            (total_correct/total_answered)*100, 1
            )
    else:
        overall_accuracy = 0

    #------------------------
    #  PREDICTED GRE SCORE
    #------------------------

    recent_test_results = list(test_results[:3])

    weights = [0.5, 0.3, 0.2]

    if recent_test_results:
        available_weights = weights[:len(recent_test_results)]

        total_weight = sum(available_weights)

        weighted_score = sum(
            result.total_score*weight
            for result, weight in zip(
                recent_test_results, available_weights
            )
        )

        predicted_score = weighted_score/total_weight

        predicted_score_high = min(340, predicted_score+2)
        predicted_score_low = max(260, predicted_score-2)

        predicted_range = (f"{predicted_score_high} - {predicted_score_low}")

    else:
        predicted_score = None
        predicted_range = "Complete a test."

    #------------------------------
    #  SUB-TOPIC DATA COLLECTION
    #------------------------------

    subtopic_data = defaultdict(
        lambda:{
            "attempted": 0,
            "correct": 0,
            "hard_attempted": 0,
            "hard_correct": 0,
        }
    )

    for answer in answers:
        question = answer.question

        topic = (question.topic or " Uncategorized")
        subtopic = (question.subtopic or " Uncategorized")

        #tuple as key to avoid same subtopic under different topic creating ERRoR
        key = (topic, subtopic)

        data = subtopic_data[key]

        data["attempted"] +=1

        if answer.is_correct:
            data["correct"] +=1

        if question.difficulty in ["hard", "very-hard"]:
            data["hard_attempted"] +=1

            if answer.is_correct:
                data["hard_correct"] +=1

    #------------------------------
    #  SUBTOPIC DATA COLLECTION
    #------------------------------

    subtopic_statistics = []

    for (topic, subtopic), data in subtopic_data.items():

        attempted = data["attempted"]
        correct = data["correct"]

        if attempted >0:
            accuracy = round((correct/attempted)*100, 1)
        else:
            accuracy = None
         

        if data["hard_attempted"]>0:
            hard_accuracy = round((data["hard_correct"]/data["hard_attempted"])*100, 1)
        else:
            hard_accuracy = None

        subtopic_statistics.append({
            "topic": topic,
            "subtopic": subtopic,
            "attempted": attempted,
            "accuracy": accuracy,
            "hard_attempted": data["hard_attempted"],
            "hard_accuracy":  hard_accuracy,
            "enough_data": attempted>= 5,
        })

    #------------------------
    #    SORT SUBTOPICS
    #------------------------

    #lowest accuracy appears first
    reliable_subtopics = [
        item
        for item in subtopic_statistics
        if item["enough_data"]
    ]

    reliable_subtopics.sort(
        key= lambda item:(
            item["accuracy"]
        )
    )

    lowest_accuracy_subtopic = (
        reliable_subtopics[0]
        if reliable_subtopics
        else None
    )

    #-------------------------------
    #  GROUP SUBTOPIC UNDER TOPICS
    #-------------------------------

    topic_statistics = defaultdict(list)

    for item in subtopic_statistics:
        topic_statistics[item["topic"]].append(item)

    topic_statistics = dict(topic_statistics)

    #------------------------------
    #  QUESTION TIME PERFORMANCE
    #------------------------------

    question_time_statistics = []

    for answer in answers:

        question = answer.question

        expected_time = question.expected_time_seconds
        time_taken = answer.time_taken

        # Skip if timing data is missing
        if expected_time is None or time_taken is None:
            continue

        question_time_statistics.append({
            "question_id": question.id,
            "topic": question.topic,
            "subtopic": question.subtopic,
            "difficulty": question.difficulty,

            "expected_time": question.expected_time_seconds,
            "time_taken": time_taken,

            "is_correct": answer.is_correct,
        })



    #--------------------------
    #    TEMPLATE CONTEXT
    #--------------------------

    context = {
        "total_answered": total_answered,
        "total_correct": total_correct,
        "overall_accuracy": overall_accuracy,
        "test_completed": test_results.count(),
        "predicted_score": predicted_score,
        "predicted_range": predicted_range,
        "subtopic_statistics": subtopic_statistics,
        "topic_statistics": topic_statistics,
        "lowest_accuracy_subtopic": lowest_accuracy_subtopic,

        "question_time_statistics": question_time_statistics,
    }

    return render(request, "gradsprint/dashboard.html",
                  context
                  )



def test_data(request, test_id):

    # Get the requested test from PostgreSQL
    test = get_object_or_404(Test, id=test_id)

    sections_data = []

    # Get all sections belonging to this test
    for section in test.sections.order_by("order"):

        questions_data = []

        # Get all questions belonging to this section
        for question in section.questions.order_by("order"):

            question_data = {
                "id": question.id,
                "type": question.question_type,
                "difficulty": question.difficulty,
                "question": question.question,
                "quantityA": question.quantity_a,
                "quantityB": question.quantity_b,
                "instruction": question.instruction,
                "passage": question.passage,
                "image": (
                    question.image.url
                    if question.image
                    else None
                    ),

                "passageRef": (
                    question.passage_ref_id
                    if question.passage_ref
                    else None
                ),

                "maxSelections": question.max_selections,

                "choices": [
                    choice.text
                    for choice in question.choices.order_by("order")
                ],

                "blanks": []
            }

            for blank in question.blanks.order_by("order"):
                question_data["blanks"].append({
                    "id": blank.order,
                    "choices": [
                        choice.text 
                        for choice in blank.choices.order_by("order")
                    ]
                })

            questions_data.append(question_data)


        section_data = {
            "id": section.id,
            "name": section.name,
            "time": section.time,
            "set_name": questions_data,
        }

        sections_data.append(section_data)


    data = {
        "id": test.id,
        "testName": test.name,
        "sections": sections_data,
    }

    return JsonResponse(data)

