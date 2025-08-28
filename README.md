The only prerequisite is Docker.

How to Run: docker-compose up --build


API Documentation:

POST /api/register/ (body: {"username": "...", "password": "..."})

POST /api/login/ (body: {"username": "...", "password": "..."})

POST /api/paragraphs/submit/ (Header: Authorization: Bearer <token>, body: {"paragraphs": ["...", "..."]})

GET /api/paragraphs/search/?word=test (Header: Authorization: Bearer <token>)

