import React, { useEffect, useState } from "react";
import DraftSelector from "./DraftSelector";
import DraftDetails from "./DraftDetails";
import BASE_URL from "./config";

type Entry = {
  name: string;
  [key: string]: any;
};

type Draft = {
  id: string;
  name: string;
  templateName: string;
  contact?: Entry;
  experience?: Entry[];
  education?: Entry[];
  projects?: Entry[];
  skills?: string[];
  certificates?: string[];
};

export default function App() {
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [selectedDraftName, setSelectedDraftName] = useState<string | null>(null);
  const [templates, setTemplates] = useState<string[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string>("");

  useEffect(() => {
    async function fetchDrafts() {
    const query = `
      query {
        drafts {
          id
          name
          templateName
          entries {
            __typename
            ... on SummaryEntry {
              id
              text
            }
            ... on SkillsEntry {
              id
              groups {
                name
                items
              }
            }
            ... on ExperienceEntry {
              id
              title
              organization
              location
              dateRange
              bulletPoints
              technologies
            }
            ... on ProjectEntry {
              id
              name
              url
              description
              technologies
            }
            ... on EducationCertEntry {
              id
              education {
                school
                degree
              }
              certifications
            }
            ... on KeywordsEntry {
              id
              items
            }
            ... on ContactEntry {
              id
              name
              location
              phone
              email
              website
              github
              linkedin
            }
          }
        }
      }
    `;

      const res = await fetch(`${BASE_URL}/graphql`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const json = await res.json();
      setDrafts(json.data.drafts);
    }

    async function fetchTemplates() {
      const res = await fetch(`${BASE_URL}/templates`);
      const data = await res.json();
      setTemplates(data);
      if (data.length > 0) {
        setSelectedTemplate(data[0]);
      }
    }

    fetchDrafts();
    fetchTemplates();
  }, []);

useEffect(() => {
  console.log("Selected template:", selectedTemplate);
  console.log("All drafts:", drafts);
  console.log("Filtered drafts:", drafts.filter((d) => d.templateName === selectedTemplate));
}, [selectedTemplate, drafts]);

  const selectedDraft = drafts.find((d) => d.name === selectedDraftName);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Resume Builder</h1>
      <hr />

      <div style={{ marginBottom: "2rem" }}>
        <label>Template: </label>
        <select
          value={selectedTemplate}
          onChange={(e) => setSelectedTemplate(e.target.value)}
          style={{ marginRight: "1rem" }}
        >
          {templates.map((template) => (
            <option key={template} value={template}>
              {template}
            </option>
          ))}
        </select>
      </div>

      <DraftSelector
        drafts={drafts.filter((d) => d.templateName === selectedTemplate)}
        selectedName={selectedDraftName}
        onSelect={setSelectedDraftName}
      />

      {selectedDraft && (
        <>
          <DraftDetails draft={selectedDraft} />

          <div style={{ marginTop: "3rem", textAlign: "center" }}>
            <button
              style={{
                fontSize: "1.5rem",
                padding: "1rem 2rem",
                backgroundColor: "#4CAF50",
                color: "white",
                border: "none",
                borderRadius: "8px",
                cursor: "pointer",
              }}
              onClick={async () => {
                if (!selectedDraft?.name) return;

                const response = await fetch(`${BASE_URL}/generate-resume`, {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(selectedDraft),
                });

                if (!response.ok) {
                  alert("Failed to generate PDF");
                  return;
                }

                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "resume.pdf";
                a.click();
                window.URL.revokeObjectURL(url);
              }}
            >
              📄 Render PDF
            </button>
          </div>
        </>
      )}
    </div>
  );
}
