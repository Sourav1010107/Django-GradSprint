#==============================
#      ANSWER SAVING
#==============================

import json
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from ..models import Question, Choice, BlankChoice, NumericValue, StudentAnswer




@login_required
@require_POST
def save_answer(request):

    try:
        # --------------------------------
        # RECEIVE JSON FROM JAVASCRIPT
        # --------------------------------

        data = json.loads(request.body)

        question_id = data.get("question_id")
        selected_answer = data.get("selected_answer", [])
        time_taken = data.get("time_taken", 0)

        # --------------------------------
        # BASIC VALIDATION
        # --------------------------------

        if not question_id:
            return JsonResponse(
                {
                    "success": False,
                    "error": "question_id is required"
                },
                status=400
            )

        question = get_object_or_404(
            Question,
            id=question_id
        )

        question_type = question.question_type

        #=================================
        #        EMPTY ANSWER
        #=================================

        is_empty = (
            selected_answer is None
            or selected_answer == ""
            or selected_answer == []
            or (
                isinstance(selected_answer, list)
                and all(
                    value in [None, ""]
                    for value in selected_answer
                )
            )
        )

        if is_empty:
            StudentAnswer.objects.filter(
                user = request.user,
                question = question
            ).delete()

            return JsonResponse({
                "success": True,
                "cleared": True,
            })
        
        is_correct = False


        # ==========================================
        # CHOICE-BASED QUESTIONS
        # ==========================================

        if question_type in [
            "sentence-equivalence",
            "reading-single",
            "reading-multiple",
            "quant-single",
            "quant-multiple",
            "quantitative-comparison",
            "data-interpretation-single",
        ]:

            # --------------------------------
            # MAKE ANSWER ALWAYS A LIST
            # --------------------------------

            if isinstance(selected_answer, list):
                selected_values = selected_answer
            elif selected_answer in [None, ""]:
                selected_values = []
            else:
                selected_values = [
                    selected_answer
                ]

            # --------------------------------
            # VALIDATE CHOICES
            # --------------------------------

            valid_choice_texts = set(
                Choice.objects.filter(
                    question=question
                ).values_list(
                    "text",
                    flat=True
                )
            )

            for answer_text in selected_values:

                if answer_text not in valid_choice_texts:

                    return JsonResponse(
                        {
                            "success": False,
                            "error": "Invalid choice submitted"
                        },
                        status=400
                    )


            # --------------------------------
            # GET CORRECT CHOICES
            # --------------------------------

            correct_answers = set(
                Choice.objects.filter(
                    question=question,
                    is_correct=True
                ).values_list(
                    "text",
                    flat=True
                )
            )

            # --------------------------------
            # COMPARE ANSWERS
            # --------------------------------

            selected_values_set = set(
                selected_values
            )

            is_correct = (
                selected_values_set
                == correct_answers
            )


        # ==========================================
        # TEXT COMPLETION
        # ==========================================

        elif question_type == "text-completion":

            if not isinstance(selected_answer, list):
                return JsonResponse(
                    {
                        "success": False,
                        "error": (
                            "Text completion answer "
                            "must be a list"
                        )
                    },
                    status=400
                )

            blanks = list(question.blanks.prefetch_related("choices")
                .order_by("order")
            )

            # Student must have one position
            # for each blank

            if len(selected_answer) != len(blanks):
                is_correct = False

            else:
                is_correct = True

                for index, blank in enumerate(blanks):
                    student_choice = (selected_answer[index])

                    # Blank still unanswered
                    if not student_choice:
                        is_correct = False
                        break

                    # Make sure the submitted text
                    # belongs to THIS blank
                    valid_choice = (
                        blank.choices.filter(
                            text=student_choice
                        ).exists()
                    )


                    if not valid_choice:
                        is_correct = False
                        break

                    correct_choice = (
                        blank.choices.filter(
                            is_correct=True
                        ).first()
                    )

                    if (
                        correct_choice is None
                        or correct_choice.text
                        != student_choice
                    ):
                        is_correct = False
                        break

        # ==========================================
        # NUMERIC ENTRY
        # ==========================================

        elif question_type == "numeric-entry":

            try:

                # Your JS stores numeric-entry
                # as a string
                student_value = Decimal(
                    str(selected_answer)
                )

                numeric_answer = (
                    NumericValue.objects.get(
                        question=question
                    )
                )

                is_correct = (
                    student_value
                    == numeric_answer.correct_value
                )


            except (
                InvalidOperation,
                ValueError,
                TypeError,
                NumericValue.DoesNotExist
            ):
                is_correct = False


        # ==========================================
        # UNKNOWN QUESTION TYPE
        # ==========================================

        else:
            return JsonResponse(
                {
                    "success": False,
                    "error": (
                        f"Unsupported question type: "
                        f"{question_type}"
                    )
                },
                status=400
            )

        # ==========================================
        # SAVE / UPDATE POSTGRESQL
        # ==========================================

        student_answer, created = (
            StudentAnswer.objects.update_or_create(

                user=request.user,
                question=question,

                defaults={
                    "selected_answer": selected_answer,
                    "is_correct": is_correct,
                    "time_taken": time_taken,
                }

            )
        )


        # --------------------------------
        # RETURN RESPONSE
        # --------------------------------

        return JsonResponse(
            {
                "success": True,
                "answer_id": student_answer.id,
                "created": created
            }
        )


    except json.JSONDecodeError:

        return JsonResponse(
            {
                "success": False,
                "error": "Invalid JSON"
            },
            status=400
        )