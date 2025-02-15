
# LLM Evaluation Pipeline
Overview

This project is a simplified backend service built using Django and PostgreSQL that simulates an evaluation pipeline for an LLM (Large Language Model) application. It exposes REST API endpoints to submit evaluation requests, process them asynchronously using Celery, and store/retrieve results. The system also sends an email notification via the Resend API upon task completion.


## Features

* Submit an evaluation request via API.

* Process evaluation requests asynchronously using Celery.

* Fetch evaluation results through an API.

* Generate responses using the Hugging Face API.

* Send email notifications upon completion via the Resend API.

* Dockerized setup for easy deployment.

## Prerequisites

Before using the Hugging Face API and Resend API, you need to create accounts and generate API keys:

* Hugging Face API: Sign up at Hugging Face and generate an API key.

* Resend API: Sign up at Resend and generate an API key.

## Technologies Used

* Django (Web framework)

* PostgreSQL (Database)

* Celery (Task queue for asynchronous processing)

* Redis (Message broker for Celery)

* Hugging Face API (For text generation)

* Resend API (For email notifications)

* Docker (For containerization)

## Setup Instructions

### Prerequisites

* Ensure you have the following installed:

* Docker

* Python (>=3.8)

* PostgreSQL

* Redis

## Environment Variables

### Create a .env file in the same directory as settings.py and add the following variables:

- DATABASE_NAME=db_name 
- DATABASE_PASS=db_pass
- HUGGING_SPACE_API=your_hugging_face_api_key
- HOST=your_host_ip
- RESEND_API=your_resend_api_key


## Running with Docker

### Navigate to the directory containing the Dockerfile and execute the following commands:

## 1. Build the Docker image:
```bash
docker build -t llm-eval-pipeline .
```

## 2. Run the container:
```bash
docker run -p 8000:8000 llm-eval-pipeline
```

## API Endpoints

### 1. Submit an Evaluation Request

#### Endpoint:

```bash
POST /api/evaluate
```

#### Request Body:

```bash
{
    "input_prompt": "explain generators in python",
    "recipient_email": "example@email.com"
}
```

#### Response:
```bash
{
    "id": "123",
    "status": "pending",
    "message": "Evaluation request submitted successfully"
}
```

### 2. Retrieve Evaluation Result

#### Endpoint:

```bash
GET /api/evaluate/{id}
```

#### Response:
```bash
{
    "id": "123",
    "status": "pending",
    "message": "Evaluation request submitted successfully"
}
```

## Design Overview

#### 1. A request is submitted via /api/evaluate.

#### 2. The request is stored in the database with a status of pending.

* Celery processes the request asynchronously:

* Calls Hugging Face API to generate text based on the input prompt.

* Updates the database with the generated response.

* Sends an email notification via Resend API.

#### 3. The result can be fetched via /api/evaluate/{id}.

### Additional Notes

* The API uses Django REST Framework (DRF) for handling requests.

* Background tasks are handled using Celery with Redis as the message broker.

* Hugging Face API is used to generate responses dynamically.

* The Resend API is used to send email notifications.
