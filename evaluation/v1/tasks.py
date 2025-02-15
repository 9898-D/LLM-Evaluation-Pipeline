import requests
from celery import shared_task
from .models import EvaluationRequest
import json
import smtplib
from email.message import EmailMessage
import environ
from evaluation import settings

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


@shared_task
def process_evaluation_request(evaluation_request_id):
    """
    Retrieve the EvaluationRequest record, process the input_prompt using OpenAI,
    update the record with the generated result, and send an email notification.
    """
    try:
        # Retrieve the evaluation request record from the database.
        eval_request = EvaluationRequest.objects.get(pk=evaluation_request_id)
    except EvaluationRequest.DoesNotExist:
        print(f"EvaluationRequest with id {evaluation_request_id} does not exist.")
        return

    # Retrieve the user's prompt.
    prompt = eval_request.input_prompt

    payload = {"inputs":prompt}
    try:
        API_URL = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
        headers = {"Authorization": f"Bearer {settings.HUGGING_SPACE_API}"}
        
        response = requests.post(API_URL, headers=headers, json=payload)
        generated_result=json.dumps(response.json())
        print(generated_result.strip())

    except Exception as e:
        # If an error occurs, capture it in the result.
        generated_result = f"Error generating response using HuggingSpzce API: {str(e)}"
        print(generated_result)

    # --- Record Update ---
    # Update the evaluation record with the generated result and mark it as 'completed'.
    eval_request.result = generated_result
    eval_request.status = 'completed'
    eval_request.recipient_email = eval_request.recipient_email
    eval_request.save()
    print(f"Record updated for evaluation id {evaluation_request_id} with result: {generated_result}")

    # --- Email Notification ---
    send_email_notification(eval_request.recipient_email)


def send_email_notification(recipient_email):

    import resend

    resend.api_key = env('RESEND_API')

    params: resend.Emails.SendParams = {
    "from": "Acme <onboarding@resend.dev>",
    "to": [recipient_email],
    "subject": "Test",
    "html": "<p>Hello Evaluation Completed</p>"
    }

    email = resend.Emails.send(params)
    print(email)