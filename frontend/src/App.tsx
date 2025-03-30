import React, { useEffect, useState } from "react";
import EntryGroup from "./EntryGroup";
import DraftSelector from "./DraftSelector";
import DraftDetails from "./DraftDetails";
import BASE_URL from "./config";

type Entry = {
  _id: string;
  id: string;
  type: string;
  name: string;
  [key: string]: any;
};

type Draft = {
  draftName: string;
  templateName: string;
  name: string;
  contact?: Entry;
  experience?: Entry[];
  education?: Entry[];
  projects?: Entry[];
  skills?: string[];
  certificates?: string[];
};

export default function App() {
  const [entries, setEntries] = useState<Record<string, Entry[]>>({});
  const [edits, setEdits] = useState<Record<string, Entry>>({});
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [selectedDraftName, setSelectedDraftName] = useState<string | null>(null);
  const [templates, setTemplates] = useState<string[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string>("");

  const grouped = ["contact", "experience", "education", "project"];

  useEffect(() => {
    async function fetchAll() {
      const entryData: Record<string, Entry[]> = {};
      for (const type of grouped) {
        const res = await fetch(`${BASE_URL}/entries/${type}`);
        entryData[type] = await res.json();
      }
      setEntries(entryData);
    }

    async function fetchDrafts() {
      const query = `
        query {
          drafts {
            draftName
            templateName
            name
            skills
            certificates
            contact {
              name
              email
              phone
              website
            }
            experience {
              name
              title
              company
              date
              bullets
            }
            education {
              name
              school
              degree
              years
            }
            projects {
              name
              date
              bullets
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

    fetchAll();
    fetchDrafts();
    fetchTemplates();
  }, []);

  const handleEdit = (id: string, field: string, value: any) => {
    setEdits((prev) => ({
      ...prev,
      [id]: {
        ...prev[id],
        [field]: value,
      },
    }));
  };

  const handleSave = async (entry: Entry) => {
    const updated = edits[entry.id] || entry;
    await fetch(`${BASE_URL}/entries/${entry.type}/${entry.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updated),
    });
    window.location.reload();
  };

  const selectedDraft = drafts.find((d) => d.draftName === selectedDraftName);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Resume Builder</h1>

      <h2>All Entries</h2>
      {grouped.map((type) =>
        entries[type]?.length ? (
          <EntryGroup
            key={type}
            type={type}
            entries={entries[type]}
            edits={edits}
            onEdit={handleEdit}
            onSave={handleSave}
          />
        ) : null
      )}

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
        <DraftDetails draft={selectedDraft} entries={entries} />

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
              if (!selectedDraft?.draftName) return;

              const response = await fetch(
                `http://localhost:8000/generate-draft-resume?draft_name=${selectedDraft.draftName}`,
                {
                  method: "POST",
                }
              );

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
