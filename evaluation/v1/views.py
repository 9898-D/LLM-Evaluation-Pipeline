from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EvaluationRequest
from .serializers import EvaluationRequestCreateSerializer, EvaluationRequestSerializer
from .tasks import process_evaluation_request

class EvaluationRequestCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EvaluationRequestCreateSerializer(data=request.data)
        if serializer.is_valid():
            evaluation_request = serializer.save(status='pending')
            # Enqueue Celery task to process the evaluation asynchronously.
            process_evaluation_request.delay(evaluation_request.id)
            return Response({'id': evaluation_request.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EvaluationRequestDetailView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            evaluation_request = EvaluationRequest.objects.get(pk=id)
        except EvaluationRequest.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EvaluationRequestSerializer(evaluation_request)
        return Response(serializer.data)
