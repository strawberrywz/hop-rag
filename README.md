# Hopf Algebra Chat Application

A FastAPI-based chat application using various language models.

## Quick Start

1. Create virtual environment:

```bash
python -m venv env

# On macOS/Linux
source env/bin/activate

# On Windows
.\env\Scripts\activate
```

2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python main.py
```

## API Endpoints

### Chat Endpoint

`POST /api/chat`

Request body:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "{\"input\": \"your message here\"}"
    }
  ]
}
```

Response:

```json
{
  "response": "model response here"
}
```

### Health Check

`GET /`

- Returns HTML template response
- Access at: http://localhost:8000

## Documentation

- API docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Error Handling

The API returns error messages in the format:

```json
{
  "error": "error description"
}
```
