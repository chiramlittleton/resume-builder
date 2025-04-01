import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client.resume_db

async def seed_entries_and_draft():
    contact = {
        "id": "contact-1",
        "type": "contact",
        "name": "Chiram Littleton",
        "location": "South Pasadena, CA 91030",
        "phone": "+1 310-435-6014",
        "email": "chiram.littleton@gmail.com",
        "website": None,
        "github": "github.com/chiramlittleton",
        "linkedin": "linkedin.com/in/chiram"
    }

    experience = [
        {
            "id": "exp-gusto",
            "type": "experience",
            "title": "Staff Software Engineer",
            "organization": "Gusto",
            "location": "San Francisco, CA",
            "dateRange": "Jan 2024 – Feb 2025",
            "bulletPoints": [
                "Designed and implemented full-stack reporting tools using React, TypeScript, and GraphQL",
                "Refactored core frontend/backend integrations to improve API efficiency and user experience",
                "Modularized reporting layers and introduced caching to improve performance and maintainability"
            ],
            "technologies": [
                "Ruby on Rails", "GraphQL", "React", "AWS", "Kafka", "Redis", "SQL", "TypeScript", "Datadog", "Buildkite", "GitHub Actions"
            ]
        },
        {
            "id": "exp-viasat",
            "type": "experience",
            "title": "Software Engineering Team Lead",
            "organization": "Viasat, Inc",
            "location": "Carlsbad, CA",
            "dateRange": "Jul 2022 – Nov 2023",
            "bulletPoints": [
                "Led two cross-functional teams responsible for OTA software updates for aircraft systems",
                "Built and maintained Java and Python-based microservices supporting ground-to-air update delivery",
                "Improved availability and resilience by redesigning AWS architecture using CloudFormation"
            ],
            "technologies": [
                "Java", "Python", "AWS", "Docker", "Kubernetes", "REST", "SQL", "Redis", "Datadog", "Splunk"
            ]
        }
    ]

    projects = [
        {
            "id": "proj-exam-mentor",
            "type": "project",
            "name": "Exam Mentor",
            "url": "https://github.com/chiramlittleton/exam_mentor",
            "description": "Adaptive learning platform",
            "technologies": ["Go", "Python", "GraphQL", "PostgreSQL", "React", "AWS", "Docker"]
        },
        {
            "id": "proj-code-mastery",
            "type": "project",
            "name": "Code Mastery",
            "url": "https://github.com/chiramlittleton/code-mastery",
            "description": "Python syntax quiz app",
            "technologies": ["Python", "FastAPI", "React", "Docker", "ChromaDB"]
        }
    ]

    education_certs = {
        "id": "edu-cert-1",
        "type": "educationCerts",
        "education": [
            {
                "school": "University of Southern California",
                "degree": "MS in Computer Science"
            },
            {
                "school": "University of Southern Pennsylvania",
                "degree": "BSE in Computer Science & Engineering"
            }
        ],
        "certifications": [
            "Certified Java Programmer",
            "AWS Certified Cloud Practitioner"
        ]
    }

    skills = {
        "id": "skills-1",
        "type": "skills",
        "groups": [
            {
                "name": "Backend",
                "items": ["Java", "Python", "Go", "GraphQL", "REST"]
            },
            {
                "name": "Frontend",
                "items": ["React", "TypeScript", "JavaScript"]
            },
            {
                "name": "Cloud & DevOps",
                "items": ["AWS", "Docker", "Kubernetes", "Kafka", "Redis", "Elasticsearch", "Jenkins"]
            },
            {
                "name": "Databases",
                "items": ["PostgreSQL", "MySQL", "MariaDB", "Oracle", "Sybase", "NoSQL"]
            },
            {
                "name": "Data & ML",
                "items": ["Pandas", "Machine Learning", "Data Warehousing"]
            }
        ]
    }

    summary = {
        "id": "summary-1",
        "type": "summary",
        "text": "Senior Software Engineer with 15+ years of experience building high-performance backend services, scalable frontend applications, and distributed systems across fintech, healthcare, and SaaS. Proven technical leader with expertise in Java, Python, Go, and cloud infrastructure. Passionate about adaptive learning, system design, and cross-functional collaboration."
    }

    keywords = {
        "id": "keywords-1",
        "type": "keywords",
        "items": [
            "Spring Boot", "Docker", "Kubernetes", "AWS", "Kafka", "Redis", "GraphQL", "FastAPI",
            "Elasticsearch", "Logstash", "ChromaDB", "RAG", "Vector DBs", "Adaptive Learning",
            "PostgreSQL", "FIX/QuickFIX", "RESTful APIs", "OAuth 2.0", "JWT", "Jenkins", "CI/CD",
            "GitHub Actions", "Angular", "React", "Python"
        ]
    }

    all_entries = experience + projects + [education_certs, skills, summary, keywords, contact]

    print("🌱 Seeding entries...")
    await db.entries.delete_many({})
    await db.entries.insert_many(all_entries)

    draft = {
        "id": "draft-1",
        "name": "Chiram Littleton",
        "templateName": "simple-modern",
        "entries": [entry["id"] for entry in all_entries]
    }

    print("📝 Creating draft...")
    await db.drafts.delete_many({})
    result = await db.drafts.insert_one(draft)
    print(f"✅ Draft created with ID: {result.inserted_id}")

if __name__ == "__main__":
    asyncio.run(seed_entries_and_draft())
