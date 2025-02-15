from rest_framework import serializers
from .models import EvaluationRequest

class EvaluationRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationRequest
        # Only allow these fields on creation; status and result are managed internally.
        fields = ('input_prompt', 'recipient_email')

class EvaluationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationRequest
        fields = ('id', 'input_prompt', 'recipient_email', 'status', 'result', 'created_at', 'updated_at')
