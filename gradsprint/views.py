from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse


from .models import Test

# Create your views here.

def test_engine(request):
    return render(request, "gradsprint/test_engine.html")


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
                "quantityA": question.quantityA,
                "quantityB": question.quantityB,
                "instruction": question.instruction,
                "passage": question.passage,

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