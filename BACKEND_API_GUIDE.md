# PMS Backend API Documentation

## Overview

The PMS (Performance Management System) module now includes a complete REST API built with Django REST Framework. All endpoints are accessible at `/api/pms/` and require JWT authentication.

## Authentication

### Login Endpoint

**POST** `/api/auth/login/`

Request:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Response:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "employee": {
    "id": 1,
    "employee_first_name": "John",
    "employee_last_name": "Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "profile_image": "http://..."
  }
}
```

### Using JWT Token

Include the access token in the Authorization header:

```
Authorization: Bearer {access_token}
```

### Token Refresh

**POST** `/api/auth/token/refresh/`

Request:
```json
{
  "refresh": "{refresh_token}"
}
```

Response:
```json
{
  "access": "{new_access_token}"
}
```

## API Endpoints

### Periods

**List all periods**
```
GET /api/pms/periods/
```

**Create period**
```
POST /api/pms/periods/
```

**Get period**
```
GET /api/pms/periods/{id}/
```

**Update period**
```
PUT /api/pms/periods/{id}/
```

**Delete period**
```
DELETE /api/pms/periods/{id}/
```

### Key Results

**List key results**
```
GET /api/pms/key-results/
```

**Create key result**
```
POST /api/pms/key-results/
```

**Get key result**
```
GET /api/pms/key-results/{id}/
```

**Update key result**
```
PUT /api/pms/key-results/{id}/
```

**Delete key result**
```
DELETE /api/pms/key-results/{id}/
```

### Objectives

**List objectives**
```
GET /api/pms/objectives/
```

**Create objective**
```
POST /api/pms/objectives/

Body:
{
  "title": "Objective Title",
  "description": "Description",
  "manager_ids": [1, 2],
  "assignee_ids": [3, 4],
  "key_result_ids": [5, 6],
  "duration_unit": "months",
  "duration": 3,
  "company_id": 1
}
```

**Get objective**
```
GET /api/pms/objectives/{id}/
```

**Update objective**
```
PUT /api/pms/objectives/{id}/
```

**Archive objective**
```
POST /api/pms/objectives/{id}/archive/
```

**Delete objective**
```
DELETE /api/pms/objectives/{id}/
```

### Employee Objectives

**List employee objectives**
```
GET /api/pms/employee-objectives/
```

**Create employee objective**
```
POST /api/pms/employee-objectives/

Body:
{
  "objective_id": 1,
  "employee_id": 5,
  "start_date": "2024-01-01",
  "end_date": "2024-03-31"
}
```

**Get employee objective**
```
GET /api/pms/employee-objectives/{id}/
```

**Update employee objective**
```
PUT /api/pms/employee-objectives/{id}/
```

**Update objective status**
```
POST /api/pms/employee-objectives/{id}/status/

Body:
{
  "status": "On Track"
}
```

**Delete employee objective**
```
DELETE /api/pms/employee-objectives/{id}/
```

### Employee Key Results

**List employee key results**
```
GET /api/pms/employee-key-results/
```

**Create employee key result**
```
POST /api/pms/employee-key-results/

Body:
{
  "key_result_id": 1,
  "employee_objective_id": 1,
  "start_value": 0,
  "current_value": 25,
  "target_value": 100
}
```

**Get employee key result**
```
GET /api/pms/employee-key-results/{id}/
```

**Update employee key result**
```
PUT /api/pms/employee-key-results/{id}/
```

**Update key result progress**
```
POST /api/pms/employee-key-results/{id}/progress/

Body:
{
  "current_value": 50
}
```

**Delete employee key result**
```
DELETE /api/pms/employee-key-results/{id}/
```

### Comments

**List comments**
```
GET /api/pms/comments/?employee_objective_id={id}
```

**Create comment**
```
POST /api/pms/comments/

Body:
{
  "comment": "Comment text",
  "employee_objective_id": 1
}
```

**Delete comment**
```
DELETE /api/pms/comments/{id}/
```

### Question Templates

**List templates**
```
GET /api/pms/question-templates/
```

**Create template**
```
POST /api/pms/question-templates/

Body:
{
  "question_template": "Template Name"
}
```

**Get template**
```
GET /api/pms/question-templates/{id}/
```

**Update template**
```
PUT /api/pms/question-templates/{id}/
```

**Delete template**
```
DELETE /api/pms/question-templates/{id}/
```

### Questions

**List questions for template**
```
GET /api/pms/questions/?template_id={id}
```

**Create question**
```
POST /api/pms/questions/

Body:
{
  "question": "Question text",
  "title": "Question Title",
  "question_type": "2",
  "template_id": 1,
  "ordering": 1
}
```

Question types:
- `1`: Text
- `2`: Rating
- `3`: Boolean
- `4`: Multi-choices
- `5`: Likert

**Get question**
```
GET /api/pms/questions/{id}/
```

**Update question**
```
PUT /api/pms/questions/{id}/
```

**Delete question**
```
DELETE /api/pms/questions/{id}/
```

### Feedback

**List feedback cycles**
```
GET /api/pms/feedback/
```

**Create feedback**
```
POST /api/pms/feedback/

Body:
{
  "review_cycle": "H1 2024 Feedback",
  "employee_id": 5,
  "manager_id": 1,
  "colleague_ids": [2, 3],
  "subordinate_ids": [6, 7],
  "others_ids": [8, 9],
  "question_template_id": 1,
  "start_date": "2024-01-01",
  "end_date": "2024-03-31"
}
```

**Get feedback**
```
GET /api/pms/feedback/{id}/
```

**Update feedback**
```
PUT /api/pms/feedback/{id}/
```

**Archive feedback**
```
POST /api/pms/feedback/{id}/archive/
```

**Submit feedback answers**
```
POST /api/pms/feedback/{id}/submit-answers/

Body:
{
  "answers": [
    {
      "question_id": 1,
      "answer": "Answer text"
    },
    {
      "question_id": 2,
      "answer": 4
    }
  ]
}
```

**View feedback answers**
```
GET /api/pms/feedback/{id}/answers/
```

**Delete feedback**
```
DELETE /api/pms/feedback/{id}/
```

### Meetings

**List meetings**
```
GET /api/pms/meetings/
```

**Create meeting**
```
POST /api/pms/meetings/

Body:
{
  "title": "Meeting Title",
  "date": "2024-01-15T10:00:00Z",
  "employee_ids": [5, 6],
  "manager_ids": [1, 2],
  "question_template": 1
}
```

**Get meeting**
```
GET /api/pms/meetings/{id}/
```

**Update meeting**
```
PUT /api/pms/meetings/{id}/
```

**Submit meeting answers**
```
POST /api/pms/meetings/{id}/submit-answers/

Body:
{
  "answers": [
    {
      "question_id": 1,
      "answer": "Answer text"
    }
  ]
}
```

**View meeting answers**
```
GET /api/pms/meetings/{id}/answers/
```

**Delete meeting**
```
DELETE /api/pms/meetings/{id}/
```

### Bonus Points

**List bonus point settings**
```
GET /api/pms/bonus-settings/
```

**Create bonus point setting**
```
POST /api/pms/bonus-settings/

Body:
{
  "model": "pms.models.EmployeeObjective",
  "applicable_for": "owner",
  "bonus_for": "Closed",
  "points": 100,
  "is_active": true
}
```

**Get bonus point setting**
```
GET /api/pms/bonus-settings/{id}/
```

**Update bonus point setting**
```
PUT /api/pms/bonus-settings/{id}/
```

**Delete bonus point setting**
```
DELETE /api/pms/bonus-settings/{id}/
```

**List employee bonus points**
```
GET /api/pms/employee-bonus-points/
```

**Create employee bonus point**
```
POST /api/pms/employee-bonus-points/

Body:
{
  "employee_id": 5,
  "bonus_point": 50,
  "based_on": "Objective Completion"
}
```

**Get employee bonus point**
```
GET /api/pms/employee-bonus-points/{id}/
```

**Update employee bonus point**
```
PUT /api/pms/employee-bonus-points/{id}/
```

**Delete employee bonus point**
```
DELETE /api/pms/employee-bonus-points/{id}/
```

### Anonymous Feedback

**List anonymous feedback**
```
GET /api/pms/anonymous-feedback/
```

**Create anonymous feedback**
```
POST /api/pms/anonymous-feedback/

Body:
{
  "feedback_subject": "Feedback Topic",
  "based_on": "general",
  "feedback_description": "Feedback details"
}
```

**Get anonymous feedback**
```
GET /api/pms/anonymous-feedback/{id}/
```

**Update anonymous feedback**
```
PUT /api/pms/anonymous-feedback/{id}/
```

**Delete anonymous feedback**
```
DELETE /api/pms/anonymous-feedback/{id}/
```

### Dashboard

**Get dashboard statistics**
```
GET /api/pms/dashboard/stats/

Response:
{
  "objectives": {
    "total": 10,
    "on_track": 7,
    "behind": 2,
    "at_risk": 1,
    "closed": 0,
    "not_started": 0
  },
  "feedback": {
    "total": 5,
    "on_track": 3,
    "behind": 1,
    "at_risk": 0,
    "closed": 1,
    "not_started": 0
  },
  "meetings_count": 2,
  "average_progress": 65.5
}
```

## Pagination

List endpoints support pagination:

```
GET /api/pms/objectives/?page=1&page_size=20
```

Response includes:
```json
{
  "count": 100,
  "next": "http://...",
  "previous": null,
  "results": [...]
}
```

## Filtering

Use query parameters to filter results:

```
GET /api/pms/objectives/?status=On%20Track
GET /api/pms/feedback/?employee_id=5
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid data",
  "details": {...}
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Permission Requirements

Most endpoints require the following permissions:

- **View**: `pms.view_*` permission
- **Create**: `pms.add_*` permission
- **Update**: `pms.change_*` permission
- **Delete**: `pms.delete_*` permission

## Testing with cURL

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "password"}'
```

### Create Objective

```bash
curl -X POST http://localhost:8000/api/pms/objectives/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {access_token}" \
  -d '{
    "title": "New Objective",
    "description": "Description",
    "manager_ids": [1],
    "duration": 3,
    "duration_unit": "months"
  }'
```

### Get Objectives

```bash
curl -X GET http://localhost:8000/api/pms/objectives/ \
  -H "Authorization: Bearer {access_token}"
```

## Rate Limiting

Currently, no rate limiting is implemented. Consider adding for production use.

## Versioning

API version: v1 (implicit)
Base path: `/api/pms/`

## CORS Headers

The API includes proper CORS headers for frontend integration:

```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

---

**Last Updated**: January 2025
**API Version**: 1.0
**Status**: Production Ready
