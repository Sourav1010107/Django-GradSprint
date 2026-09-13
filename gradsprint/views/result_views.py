from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from ..models import Test
from ..services.result_service import generate_test_result



@login_required
@require_POST
def generate_test_result_view(request, test_id):


    result = generate_test_result(
        request.user,
        test_id
    )

    return JsonResponse({
        "success": True,
        "result_id": result.id,
        "verbal_score": result.verbal_score,
        "quant_score": result.quant_score,
        "total_score": result.total_score,
        "correct_answers": result.correct_answers,
        "total_attempted_question": result.total_attempted_question
    })