import React, { useEffect, useState } from "react";
import axios from "axios";

type Entry = {
  _id: string;
  id: string;
  name: string;
  type: "experience" | "education" | "project" | "contact";
  [key: string]: any;
};

type Draft = {
  _id: string;
  draft_name: string;
  name: string;
  template_name: string;
  contact_name?: string;
  education_names?: string[];
  experience_names?: string[];
  project_names?: string[];
  skills?: string[];
  certificates?: string[];
};

export default function App() {
  const [entries, setEntries] = useState<Record<string, Entry[]>>({});
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [selectedDraft, setSelectedDraft] = useState<Draft | null>(null);
  const [entryEdits, setEntryEdits] = useState<Record<string, Entry>>({});

  useEffect(() => {
    const fetchEntries = async () => {
      const types = ["experience", "education", "project", "contact"];
      const groupedEntries: Record<string, Entry[]> = {};
      for (const type of types) {
        const res = await axios.get(`http://localhost:8000/entries/${type}`);
        groupedEntries[type] = res.data;
      }
      setEntries(groupedEntries);
    };

    const fetchDrafts = async () => {
      const res = await axios.get("http://localhost:8000/drafts");
      setDrafts(res.data);
    };

    fetchEntries();
    fetchDrafts();
  }, []);

  const handleEdit = (id: string, field: string, value: string) => {
    setEntryEdits((prev) => ({
      ...prev,
      [id]: {
        ...prev[id],
        [field]: value,
      },
    }));
  };

  const saveEntry = async (entry: Entry) => {
    const update = entryEdits[entry.id];
    if (!update) return;
    await axios.put(`http://localhost:8000/entries/${entry.type}/${entry.id}`, update);
    setEntryEdits((prev) => {
      const next = { ...prev };
      delete next[entry.id];
      return next;
    });
    // Refresh entries
    const res = await axios.get(`http://localhost:8000/entries/${entry.type}`);
    setEntries((prev) => ({ ...prev, [entry.type]: res.data }));
  };

  const renderEntry = (entry: Entry) => {
    const edited = entryEdits[entry.id] || entry;
  
    return (
      <div key={entry.id} style={{ marginBottom: "1rem", borderBottom: "1px solid #ccc", paddingBottom: "1rem" }}>
        <h4>{entry.type.toUpperCase()} Entry</h4>
        {Object.entries(edited).map(([key, val]) => {
          if (["_id", "id", "type"].includes(key)) return null;
          if (Array.isArray(val)) {
            return (
              <div key={key}>
                <label>{key}</label>
                {val.map((v: string, idx: number) => (
                  <input
                    key={idx}
                    type="text"
                    value={v}
                    onChange={(e) => {
                      const updatedList = [...val];
                      updatedList[idx] = e.target.value;
                      handleEdit(entry.id, key, updatedList);
                    }}
                    style={{ display: "block", width: "100%", marginBottom: "4px" }}
                  />
                ))}
              </div>
            );
          } else {
            return (
              <div key={key}>
                <label>{key}</label>
                <input
                  type="text"
                  value={val}
                  onChange={(e) => handleEdit(entry.id, key, e.target.value)}
                  style={{ display: "block", width: "100%", marginBottom: "4px" }}
                />
              </div>
            );
          }
        })}
        <button onClick={() => saveEntry(entry)}>Save</button>
      </div>
    );
  };
  
  const renderEntryGroup = (type: string) => {
    const group = entries[type] || [];
    return (
      <div key={type} style={{ marginBottom: "2rem" }}>
        <h3>{type.toUpperCase()}</h3>
        {group.map(renderEntry)}
      </div>
    );
  };

  const draftContains = (draft: Draft, type: string, entry: Entry): boolean => {
    if (type === "contact") return draft.contact_name === entry.name;
    const list = (draft as any)[`${type}_names`] || [];
    return list.includes(entry.name);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>Resume Builder</h1>

      <h2>All Entries</h2>
      {["contact", "experience", "education", "project"].map(renderEntryGroup)}

      <hr />

      <h2>Select a Draft</h2>
      <select
        onChange={(e) => {
          const draft = drafts.find((d) => d._id === e.target.value);
          setSelectedDraft(draft || null);
        }}
      >
        <option value="">-- Select Draft --</option>
        {drafts.map((d) => (
          <option key={d._id} value={d._id}>
            {d.draft_name}
          </option>
        ))}
      </select>

      {selectedDraft && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Draft: {selectedDraft.draft_name}</h3>
          <p>
            <strong>Template:</strong> {selectedDraft.template_name}
          </p>
          <p>
            <strong>Resume Name:</strong> {selectedDraft.name}
          </p>

          {["contact", "experience", "education", "project"].map((type) => {
            const group = entries[type] || [];
            const matches = group.filter((e) => draftContains(selectedDraft, type, e));
            return (
              <div key={type} style={{ marginTop: "1.5rem" }}>
                <strong>{type.toUpperCase()}:</strong>
                <ul>
                  {matches.map((e) => (
                    <li key={e.id}>{e.name}</li>
                  ))}
                  {matches.length === 0 && <li>(none)</li>}
                </ul>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
