import React from "react";

export default function DraftSelector({ drafts, selectedName, onSelect }) {
  return (
    <>
      <h2>Select a Draft</h2>
      <select onChange={(e) => onSelect(e.target.value)} value={selectedName || ""}>
        <option value="">-- Select Draft --</option>
        {drafts.map((d) => (
          <option key={d.name} value={d.name}>
            {d.name}
          </option>
        ))}
      </select>
    </>
  );
}
