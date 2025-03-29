import React, { useEffect, useState } from "react";
import EntryGroup from "./EntryGroup";
import DraftSelector from "./DraftSelector";
import DraftDetails from "./DraftDetails";

type Entry = {
  _id: string;
  id: string;
  type: string;
  name: string;
  [key: string]: any;
};

type Draft = {
  _id: string;
  draft_name: string;
  template_name: string;
  name: string;
  contact_name?: string;
  experience_names?: string[];
  education_names?: string[];
  project_names?: string[];
};

export default function App() {
  const [entries, setEntries] = useState<Record<string, Entry[]>>({});
  const [edits, setEdits] = useState<Record<string, Entry>>({});
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [selectedDraftId, setSelectedDraftId] = useState<string | null>(null);
  const [templates, setTemplates] = useState<string[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string>("");

  const grouped = ["contact", "experience", "education", "project"];

  useEffect(() => {
    async function fetchAll() {
      const entryData: Record<string, Entry[]> = {};
      for (const type of grouped) {
        const res = await fetch(`http://localhost:8000/entries/${type}`);
        entryData[type] = await res.json();
      }
      setEntries(entryData);
    }

    async function fetchDrafts() {
      const res = await fetch("http://localhost:8000/drafts");
      setDrafts(await res.json());
    }

    async function fetchTemplates() {
      const res = await fetch("http://localhost:8000/templates");
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
    await fetch(`http://localhost:8000/entries/${entry.type}/${entry.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updated),
    });
    window.location.reload();
  };

  const selectedDraft = drafts.find((d) => d._id === selectedDraftId);

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
      drafts={drafts.filter((d) => d.template_name === selectedTemplate)}
      selectedId={selectedDraftId}
      onSelect={setSelectedDraftId}
    />

      {selectedDraft && (
        <DraftDetails draft={selectedDraft} entries={entries} />
      )}
    </div>
  );
}
