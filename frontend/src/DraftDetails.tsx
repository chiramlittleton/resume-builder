import React from "react";

export default function DraftDetails({ draft, entries }) {
  const draftContains = (type, entry) => {
    if (type === "contact") return draft.contact_name === entry.name;
    const list = draft[`${type}_names`] || [];
    return list.includes(entry.name);
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <h3>Draft: {draft.draft_name}</h3>
      <p><strong>Template:</strong> {draft.template_name}</p>
      <p><strong>Resume Name:</strong> {draft.name}</p>

      {["contact", "experience", "education", "project"].map((type) => {
        const group = entries[type] || [];
        const matches = group.filter((e) => draftContains(type, e));
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
  );
}
