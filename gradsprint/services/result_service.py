#=======================================
#  TestResult Model: SENDING DATA TO DB
#=======================================
##  ????? RELATIONSHIP TRAVERSAL SYNTAX OPTIMIZATION


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from django.utils import timezone

from ..models import Test, StudentAnswer, TestResult




def generate_test_result(user, test_id):

    test = get_object_or_404(
        Test,
        id=test_id
    )

    #--------------------------------
    # GET ANSWERS FOR THIS TEST
    #--------------------------------

    answers = StudentAnswer.objects.filter(
        user = user,
        question__section__test = test
    ).select_related(
        "question",
        "question__section"
    )

    if not answers.exists():
        return JsonResponse({
            "success":False,
            "error":"No answers found for this test"
        },status=400)

    #--------------------------------
    # VERBAL ANSWERS
    #--------------------------------

    verbal_answers = answers.filter(
        question__section__name__istartswith = "verbal" 
    )

    verbal_total = verbal_answers.count() 

    verbal_correct = verbal_answers.filter(
        is_correct=True
    ).count()

    #--------------------
    # QUANT ANSWERS
    #--------------------

    quant_answers = answers.filter(
        question__section__name__istartswith= "quanttitative" 
    )

    quant_total = quant_answers.count() #???????????

    quant_correct = quant_answers.filter(
        is_correct=True
    ).count()

    #--------------------------------
    # CALCULATE ACCURACY
    #--------------------------------

    verbal_accuracy=(
        verbal_correct/verbal_total
        if verbal_total>0
        else 0
    )

    quant_accuracy=(
        quant_correct/quant_total
        if quant_total>0
        else 0
    )

    #--------------------------------
    # TEMPORARY SCORE CONVERSION
    #--------------------------------

    verbal_score = 130 + verbal_correct
    quant_score = 130 + quant_correct

    total_score = verbal_score + quant_score
    total_attempted_question = verbal_total + quant_total
    correct_answers = quant_correct + verbal_correct



    #--------------------------------
    # CREATE TEST RESULT
    #--------------------------------

    test_result, created = TestResult.objects.update_or_create(
        user = user,
        test = test,
        defaults = {
            "verbal_score":verbal_score,
            "quant_score":quant_score,
            "total_score":total_score,
            "correct_answers": correct_answers,
            "total_attempted_question": total_attempted_question,
            "completed_at":timezone.now()
        }
    )

    return test_result 


