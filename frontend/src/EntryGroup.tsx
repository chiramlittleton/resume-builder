import React from "react";
import EntryEditor from "./EntryEditor";

export default function EntryGroup({ type, entries, edits, onEdit, onSave }) {
  return (
    <div style={{ marginBottom: "2rem" }}>
      <h3>{type.toUpperCase()}</h3>
      {entries.map((entry) => (
        <EntryEditor
          key={entry.id}
          entry={entry}
          edited={edits[entry.id] || entry}
          onEdit={onEdit}
          onSave={onSave}
        />
      ))}
    </div>
  );
}
