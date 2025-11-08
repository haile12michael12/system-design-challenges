# API Reference

## Authentication

### POST /api/v1/auth/register
Register a new user

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "created_at": "datetime"
}
```

### POST /api/v1/auth/login
Login user

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "string"
}
```

## Prompts

### GET /api/v1/prompts
Get all prompts

**Query Parameters:**
- `skip` (integer, optional): Number of prompts to skip
- `limit` (integer, optional): Maximum number of prompts to return

**Response:**
```json
[
  {
    "id": "integer",
    "title": "string",
    "description": "string",
    "difficulty": "string",
    "created_at": "datetime"
  }
]
```

### GET /api/v1/prompts/{prompt_id}
Get a specific prompt

**Response:**
```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "difficulty": "string",
  "created_at": "datetime"
}
```

### POST /api/v1/prompts
Create a new prompt (admin only)

**Request Body:**
```json
{
  "title": "string",
  "description": "string",
  "difficulty": "string"
}
```

**Response:**
```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "difficulty": "string",
  "created_at": "datetime"
}
```

## Submissions

### GET /api/v1/submissions
Get all submissions for the current user

**Query Parameters:**
- `skip` (integer, optional): Number of submissions to skip
- `limit` (integer, optional): Maximum number of submissions to return

**Response:**
```json
[
  {
    "id": "integer",
    "prompt_id": "integer",
    "user_id": "integer",
    "diagram_data": "string",
    "explanation": "string",
    "created_at": "datetime"
  }
]
```

### GET /api/v1/submissions/{submission_id}
Get a specific submission

**Response:**
```json
{
  "id": "integer",
  "prompt_id": "integer",
  "user_id": "integer",
  "diagram_data": "string",
  "explanation": "string",
  "created_at": "datetime"
}
```

### POST /api/v1/submissions
Create a new submission

**Request Body:**
```json
{
  "prompt_id": "integer",
  "diagram_data": "string",
  "explanation": "string"
}
```

**Response:**
```json
{
  "id": "integer",
  "prompt_id": "integer",
  "user_id": "integer",
  "diagram_data": "string",
  "explanation": "string",
  "created_at": "datetime"
}
```

## Gradings

### GET /api/v1/gradings/{grading_id}
Get a specific grading

**Response:**
```json
{
  "id": "integer",
  "submission_id": "integer",
  "score": "number",
  "feedback": "string",
  "created_at": "datetime"
}
```

### PUT /api/v1/gradings/{grading_id}
Update a grading (admin only)

**Request Body:**
```json
{
  "score": "number",
  "feedback": "string"
}
```

**Response:**
```json
{
  "id": "integer",
  "submission_id": "integer",
  "score": "number",
  "feedback": "string",
  "created_at": "datetime"
}
```