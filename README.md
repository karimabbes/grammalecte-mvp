# Grammalecte FastAPI API

A minimal FastAPI application that wraps the Grammalecte grammar checker for French text.

## Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Grammalecte locally:
```bash
pip install -e .
```

3. Run the application:
```bash
python run.py
```

Or alternatively:
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## Railway Deployment

This project is configured for Railway deployment.

### Railway Setup:
1. Connect your GitHub repository to Railway
2. Railway will automatically detect the Python project
3. The app will be deployed using `railway_start.py`

### Environment Variables:
- `PORT`: Automatically set by Railway

## API Endpoints

### GET /
Health check endpoint that returns a simple message.

### GET /health
Health check endpoint that returns the service status and version information.

### POST /check
Check text for grammar and spelling errors.

**Request Body:**
```json
{
  "text": "Your French text to check here.",
  "format_text": false,
  "options": null
}
```

**Response:**
```json
{
  "program": "grammalecte-fr",
  "version": "2.1.1",
  "lang": "fr",
  "data": [
    {
      "paragraph": 1,
      "start": 0,
      "end": 4,
      "message": "Grammar error description",
      "suggestions": ["suggestion1", "suggestion2"],
      "rule_id": "RULE_ID"
    }
  ]
}
```

### GET /suggest/{token}
Get spelling suggestions for a specific token.

**Response:**
```json
{
  "suggestions": ["suggestion1", "suggestion2", "suggestion3"]
}
```

### GET /options
Get available grammar checking options and their default values.

## Interactive API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example Usage

### Check text for errors:
```bash
curl -X POST "http://localhost:8000/check" \
     -H "Content-Type: application/json" \
     -d '{"text": "Je vais au magasin pour acheter du pain."}'
```

### Get spelling suggestions:
```bash
curl -X GET "http://localhost:8000/suggest/bonjour"
```

### Check with custom options:
```bash
curl -X POST "http://localhost:8000/check" \
     -H "Content-Type: application/json" \
     -d '{"text": "Votre texte ici.", "options": {"typo": true, "esp": true}}'
```

## Demo

Run the demo script to test the API:
```bash
python demo.py
```

## Features

- ✅ Grammar checking for French text
- ✅ Spelling suggestions
- ✅ Configurable checking options
- ✅ Text formatting support
- ✅ RESTful API with OpenAPI documentation
- ✅ Health monitoring
- ✅ Error handling
- ✅ Railway deployment ready

## Grammalecte Information

This API uses Grammalecte v2.1.1, a French grammar checker. The original Grammalecte project can be found at: http://grammalecte.net 