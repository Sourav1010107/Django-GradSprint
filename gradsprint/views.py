from django.shortcuts import get_object_or_404
from django.http import JsonResponse


from .models import Test

# Create your views here.


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
                "instruction": question.instruction,
                "passage": question.passage,
                "passageRef": (
                    question.passage_ref_id
                    if question.passage_ref
                    else None
                ),
                
            }

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