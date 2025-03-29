import React from "react";

export default function DraftDetails({ draft }) {
  return (
    <div style={{ marginTop: "2rem" }}>
      <h3>Draft: {draft.draftName}</h3>
      <p><strong>Template:</strong> {draft.templateName}</p>
      <p><strong>Resume Name:</strong> {draft.name}</p>

      {/* Contact */}
      <div style={{ marginTop: "1.5rem" }}>
        <strong>CONTACT:</strong>
        {draft.contact ? (
          <ul>
            <li>{draft.contact.name} ({draft.contact.email})</li>
          </ul>
        ) : (
          <ul><li>(none)</li></ul>
        )}
      </div>

      {/* Experience */}
      <div style={{ marginTop: "1.5rem" }}>
        <strong>EXPERIENCE:</strong>
        {draft.experience?.length ? (
          <ul>
            {draft.experience.map((e) => (
              <li key={e.name}>
                <strong>{e.title}</strong> at {e.company}
              </li>
            ))}
          </ul>
        ) : (
          <ul><li>(none)</li></ul>
        )}
      </div>

      {/* Education */}
      <div style={{ marginTop: "1.5rem" }}>
        <strong>EDUCATION:</strong>
        {draft.education?.length ? (
          <ul>
            {draft.education.map((e) => (
              <li key={e.name}>
                {e.degree}, {e.school}
              </li>
            ))}
          </ul>
        ) : (
          <ul><li>(none)</li></ul>
        )}
      </div>

      {/* Projects */}
      <div style={{ marginTop: "1.5rem" }}>
        <strong>PROJECTS:</strong>
        {draft.projects?.length ? (
          <ul>
            {draft.projects.map((p) => (
              <li key={p.name}>{p.name}</li>
            ))}
          </ul>
        ) : (
          <ul><li>(none)</li></ul>
        )}
      </div>

      {/* Skills */}
      <div style={{ marginTop: "1.5rem" }}>
        <strong>SKILLS:</strong>
        {draft.skills?.length ? (
          <ul>
            {draft.skills.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        ) : (
          <ul><li>(none)</li></ul>
        )}
      </div>

      {/* Certificates */}
      <div style={{ marginTop: "1.5rem" }}>
        <strong>CERTIFICATES:</strong>
        {draft.certificates?.length ? (
          <ul>
            {draft.certificates.map((c, i) => <li key={i}>{c}</li>)}
          </ul>
        ) : (
          <ul><li>(none)</li></ul>
        )}
      </div>
    </div>
  );
}
