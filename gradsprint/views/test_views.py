#==============================
#  Test Data request from DB ?????? OPTIMIZATION REQUIRED: Test object caling
#  Test Engine view function
#==============================


from django.shortcuts import get_object_or_404, render 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from ..models import Test




# Test Engine 
@ensure_csrf_cookie
def test_engine(request):
    return render(request, "gradsprint/test_engine.html")




#================================
#     TEST DATA LOADING
#================================

@login_required   
def test_data(request, test_id):

    # Get the requested test from PostgreSQL
    test = get_object_or_404(Test.objects.prefetch_related(
        "sections__questions__choices",                             # ????? optimize
        "sections__questions__blanks__choices"
    ), id=test_id)

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


                "choices": [
                    choice.text
                    for choice in question.choices.order_by("order")
                ],

                "blanks": []
            }

            for blank in question.blanks.order_by("order"):
                question_data["blanks"].append({
                    "id": blank.id,
                    "order": blank.order,
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