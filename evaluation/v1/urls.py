from django.urls import path
from .views import EvaluationRequestCreateView, EvaluationRequestDetailView

urlpatterns = [
    path('evaluate', EvaluationRequestCreateView.as_view(), name='evaluate-create'),
    path('evaluate/<int:id>', EvaluationRequestDetailView.as_view(), name='evaluate-detail'),
]
