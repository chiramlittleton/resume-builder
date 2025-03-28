import React from "react";

type Entry = {
  _id: string;
  id: string;
  name: string;
  type: string;
  [key: string]: any;
};

type Props = {
  entry: Entry;
  edited: Entry;
  onEdit: (id: string, field: string, value: any) => void;
  onSave: (entry: Entry) => void;
};

export default function EntryEditor({ entry, edited, onEdit, onSave }: Props) {
  return (
    <div style={{ marginBottom: "1rem", borderBottom: "1px solid #ccc", paddingBottom: "1rem" }}>
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
                    const updated = [...val];
                    updated[idx] = e.target.value;
                    onEdit(entry.id, key, updated);
                  }}
                  style={{ display: "block", width: "100%", marginBottom: "4px" }}
                />
              ))}
            </div>
          );
        }
        return (
          <div key={key}>
            <label>{key}</label>
            <input
              type="text"
              value={val}
              onChange={(e) => onEdit(entry.id, key, e.target.value)}
              style={{ display: "block", width: "100%", marginBottom: "4px" }}
            />
          </div>
        );
      })}
      <button onClick={() => onSave(entry)}>Save</button>
    </div>
  );
}
