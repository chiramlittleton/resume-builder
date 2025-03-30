import React from "react";

type Entry = {
  id: string;
  name: string;
  [key: string]: any;
};

type Draft = {
  draftName: string;
  templateName: string;
  name: string;
  contact?: Entry;
  experience: Entry[];
  education: Entry[];
  projects: Entry[];
  skills: string[];
  certificates: string[];
};

type Props = {
  draft: Draft;
  entries: Record<string, Entry[]>;
};

export default function DraftDetails({ draft, entries }: Props) {
  const handleContactChange = (id: string) => {
    console.log(`Change contact to: ${id}`);
    // Add actual update logic here
  };

  const handleEntryChange = (
    type: "experience" | "education" | "projects",
    index: number,
    newId: string
  ) => {
    console.log(`Change ${type} entry at index ${index} to: ${newId}`);
    // Add update logic here
  };

  const handleRemoveEntry = (
    type: "experience" | "education" | "projects",
    index: number
  ) => {
    console.log(`Remove ${type} entry at index ${index}`);
    // Add update logic here
  };

  const handleAddEntry = (type: "experience" | "education" | "projects", id: string) => {
    console.log(`Add ${type} entry with ID: ${id}`);
    // Add logic here
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <h3>Draft: {draft.draftName}</h3>
      <p><strong>Template:</strong> {draft.templateName}</p>
      <p><strong>Resume Name:</strong> {draft.name}</p>

      {/* Contact Selection */}
      <div style={{ marginTop: "1.5rem" }}>
        <strong>CONTACT:</strong>
        <select
          value={draft.contact?.id || ""}
          onChange={(e) => handleContactChange(e.target.value)}
        >
          <option value="">Select a contact</option>
          {(entries["contact"] || []).map((entry) => (
            <option key={entry.id} value={entry.id}>
              {entry.name}
            </option>
          ))}
        </select>
      </div>

      {/* Entry Sections */}
      {["experience", "education", "projects"].map((type) => {
        const current = draft[type as keyof Draft] as Entry[];
        const all = entries[type] || [];
        return (
          <div key={type} style={{ marginTop: "1.5rem" }}>
            <strong>{type.toUpperCase()}:</strong>
            {current.length > 0 ? (
              current.map((entry, index) => (
                <div key={entry.id} style={{ display: "flex", marginTop: "0.5rem" }}>
                  <select
                    value={entry.id}
                    onChange={(e) =>
                      handleEntryChange(type as any, index, e.target.value)
                    }
                  >
                    {all.map((opt) => (
                      <option key={opt.id} value={opt.id}>
                        {opt.name}
                      </option>
                    ))}
                  </select>
                  <button
                    onClick={() => handleRemoveEntry(type as any, index)}
                    style={{ marginLeft: "0.5rem" }}
                  >
                    Remove
                  </button>
                </div>
              ))
            ) : (
              <p>(none)</p>
            )}

            {/* Add New Entry */}
            <div style={{ marginTop: "0.5rem" }}>
              <select
                defaultValue=""
                onChange={(e) => {
                  if (e.target.value) {
                    handleAddEntry(type as any, e.target.value);
                    e.target.value = "";
                  }
                }}
              >
                <option value="">Add {type} entry</option>
                {all.map((entry) => (
                  <option key={entry.id} value={entry.id}>
                    {entry.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        );
      })}
    </div>
  );
}
