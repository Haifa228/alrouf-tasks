# Alrouf Tasks Project

This repo implements the 3 tasks for the AI Integration Engineer role at Alrouf Lighting Technology Pvt Ltd.

## General Notes
- Tools used: Zapier (Task 1), Python/FastAPI/OpenAI/LangChain/FAISS (Tasks 2-3).
- Run locally: Install dependencies with `pip install -r requirements.txt`. Use mocks for APIs.
- Video Walkthrough: [Link to your video, e.g., https://www.loom.com/share/your-video-id] (3-5 min explaining setup and running each task).
- .env.example: Copy to .env and fill in if needed (mocks used by default).

## Task 1: RFQ → CRM Automation
See task1/README_task1.md for setup details, blueprints, and mocks.

## Task 2: Quotation Microservice
Run: `uvicorn task2.main:app --reload`
Endpoint: POST /quote
Tests: `pytest task2/test_main.py`
Docker: Build with `docker build -t quote-service .` (from task2 folder)

## Task 3: RAG Knowledge Base
Run: `python task3/main.py` (CLI interface)
Supports AR/EN queries/answers.
Latency/Cost: See task3/latency_cost_report.md

## How to Run Locally Without Secrets
- All tasks use mocks (e.g., fake OpenAI responses).
- No real API keys needed.
