import React from "react";

export default function DraftSelector({ drafts, selectedId, onSelect }) {
  return (
    <>
      <h2>Select a Draft</h2>
      <select onChange={(e) => onSelect(e.target.value)} value={selectedId || ""}>
        <option value="">-- Select Draft --</option>
        {drafts.map((d) => (
          <option key={d._id} value={d._id}>
            {d.draft_name}
          </option>
        ))}
      </select>
    </>
  );
}
