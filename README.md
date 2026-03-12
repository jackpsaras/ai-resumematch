# ResumeMatch AI

**AI-Powered Resume → Job Match Analyzer**

Upload your resume (PDF) + paste a job description and get:
- A **real weighted match score** (0-100%)
- Missing skills with visual gap bars
- Clickable AI bullet rewrites (3 improved versions per bullet)

Built as a full-stack portfolio project to showcase AI integration, modern UI, and production-ready practices.

## Features
- PDF text extraction
- Structured AI analysis using OpenAI
- Redis caching (saves money on API calls)
- Beautiful score circle + skill gap visualization
- One click AI bullet rewriter
- Dockerized backend + database

## Tech Stack

**Frontend**
- React + Vite
- Tailwind CSS
- Lucide React (icons)
- Axios

**Backend**
- FastAPI
- SQLAlchemy + PostgreSQL
- Redis (caching)
- Pydantic (structured outputs)
- pdfplumber (PDF parsing)
- OpenAI (gpt-4o-mini with structured parsing)

**Infrastructure**
- Docker + Docker Compose
- CORS middleware
- Async processing