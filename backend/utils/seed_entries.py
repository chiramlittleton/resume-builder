import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client.resume_db


async def seed_entries_and_draft():
    experience = [
        {
            "id": "exp-gusto",
            "type": "experience",
            "name": "Staff Engineer at Gusto",
            "title": "Staff Software Engineer",
            "company": "Gusto",
            "date": "1/24 - 2/25",
            "bullets": [
                "Built and maintained full-stack custom reporting tools for payroll/HR, using React, TypeScript, and GraphQL.",
                "Optimized system performance by refactoring frontend/backend integrations and improving API efficiency.",
                "Tools: Ruby on Rails, GraphQL, React, AWS, Kafka, Typescript, SQL, Redis, Datadog, Buildkite, GitHub Actions"
            ]
        },
        {
            "id": "exp-viasat",
            "type": "experience",
            "name": "Team Lead at Viasat",
            "title": "Software Engineering Team Lead",
            "company": "Viasat, Inc",
            "date": "7/22 - 11/23",
            "bullets": [
                "Led two engineering teams (6 total developers) with ownership of design, delivery, and mentoring.",
                "Architected OTA update infrastructure for aircraft using Java and Python microservices.",
                "Redesigned AWS infrastructure using CloudFormation, reducing outages significantly."
            ]
        }
    ]

    projects = [
        {
            "id": "proj-exam-mentor",
            "type": "project",
            "name": "Exam Mentor",
            "date": "2024",
            "bullets": [
                "Machine learning-powered adaptive learning platform for generating personalized exam questions.",
                "Technologies: Go, Python, GraphQL, OpenAI, RAG, React, PostgreSQL, AWS, Docker"
            ]
        },
        {
            "id": "proj-code-mastery",
            "type": "project",
            "name": "Code Mastery",
            "date": "2024",
            "bullets": [
                "AI-powered Python syntax quiz app for reinforcing skills with real-time feedback.",
                "Technologies: Python, FastAPI, ChromaDB, OpenAI, Docker, React"
            ]
        }
    ]

    education = [
        {
            "id": "edu-usc",
            "type": "education",
            "name": "USC MS",
            "degree": "MS Computer Science",
            "school": "University of Southern California",
            "years": ""
        },
        {
            "id": "edu-usp",
            "type": "education",
            "name": "USP BSE",
            "degree": "BSE Comp. Sci. & Eng.",
            "school": "University of Southern Pennsylvania",
            "years": ""
        }
    ]

    contact = {
        "id": "contact-chiram",
        "type": "contact",
        "name": "Chiram Littleton",
        "email": "chiram.littleton@gmail.com",
        "phone": "+1 310-435-6014",
        "website": "https://www.linkedin.com/in/chiram"
    }

    print("🌱 Seeding entries...")
    await db.entries.delete_many({})
    await db.entries.insert_many(experience + projects + education + [contact])

    shared_draft_data = {
        "name": "Chiram Littleton",
        "contact_id": contact["id"],
        "experience_ids": [e["id"] for e in experience],
        "education_ids": [e["id"] for e in education],
        "project_ids": [p["id"] for p in projects],
        "skills": [
            "Java", "SQL", "Python", "React", "GraphQL", "AWS", "Kafka", "Docker", "Redis"
        ],
        "certificates": ["Certified Java Programmer", "AWS certified cloud practitioner"],
        "user_id": "demo-user"
    }

    print("📝 Creating drafts...")
    await db.drafts.delete_many({})

    draft_simple = {
        "draft_name": "Full Resume Draft",
        "template_name": "simple-modern",
        **shared_draft_data
    }
    draft_elegant = {
        "draft_name": "Elegant Resume Draft",
        "template_name": "elegant",
        **shared_draft_data
    }

    result_simple = await db.drafts.insert_one(draft_simple)
    result_elegant = await db.drafts.insert_one(draft_elegant)

    print(f"✅ Drafts created: simple={result_simple.inserted_id}, elegant={result_elegant.inserted_id}")


if __name__ == "__main__":
    asyncio.run(seed_entries_and_draft())
