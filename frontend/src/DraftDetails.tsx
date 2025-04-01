import React from "react";

type Entry =
  | { __typename: "ContactEntry"; id: string; name: string; location: string; phone: string; email: string; website?: string; github?: string; linkedin?: string }
  | { __typename: "SummaryEntry"; id: string; text: string }
  | { __typename: "SkillsEntry"; id: string; groups: { name: string; items: string[] }[] }
  | { __typename: "ExperienceEntry"; id: string; title: string; organization: string; location?: string; dateRange: string; bulletPoints: string[]; technologies: string[] }
  | { __typename: "ProjectEntry"; id: string; name: string; url?: string; description: string; technologies: string[] }
  | { __typename: "EducationCertEntry"; id: string; education: { school: string; degree: string }[]; certifications: string[] }
  | { __typename: "KeywordsEntry"; id: string; items: string[] };

type Draft = {
  id: string;
  name: string;
  templateName: string;
  entries: Entry[];
};

type Props = {
  draft: Draft;
};

export default function DraftDetails({ draft }: Props) {
  const getEntries = <T extends Entry["__typename"]>(typename: T): Extract<Entry, { __typename: T }>[] =>
    draft.entries.filter((e) => e.__typename === typename) as any;

  const contact = getEntries("ContactEntry")[0];
  const summary = getEntries("SummaryEntry")[0];
  const skills = getEntries("SkillsEntry")[0];
  const experience = getEntries("ExperienceEntry");
  const projects = getEntries("ProjectEntry");
  const educationCert = getEntries("EducationCertEntry")[0];
  const keywords = getEntries("KeywordsEntry")[0];

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>Draft: {draft.name}</h2>
      <p><strong>Template:</strong> {draft.templateName}</p>

      {contact && (
        <>
          <h3>Contact</h3>
          <p>{contact.name}</p>
          <p>{contact.location}</p>
          <p>{contact.phone} — {contact.email}</p>
          {contact.linkedin && <p>LinkedIn: {contact.linkedin}</p>}
          {contact.github && <p>GitHub: {contact.github}</p>}
        </>
      )}

      {summary && (
        <>
          <h3>Professional Summary</h3>
          <p>{summary.text}</p>
        </>
      )}

      {skills && (
        <>
          <h3>Skills</h3>
          {skills.groups.map((group) => (
            <p key={group.name}>
              <strong>{group.name}:</strong> {group.items.join(", ")}
            </p>
          ))}
        </>
      )}

      {experience.length > 0 && (
        <>
          <h3>Professional Experience</h3>
          {experience.map((job) => (
            <div key={job.id} style={{ marginBottom: "1rem" }}>
              <strong>{job.title}</strong> — {job.organization} ({job.dateRange})
              {job.location && <div><em>{job.location}</em></div>}
              <ul>
                {job.bulletPoints.map((point, i) => (
                  <li key={i}>{point}</li>
                ))}
              </ul>
              <div><strong>Stack:</strong> {job.technologies.join(", ")}</div>
            </div>
          ))}
        </>
      )}

      {projects.length > 0 && (
        <>
          <h3>Projects</h3>
          {projects.map((p) => (
            <div key={p.id} style={{ marginBottom: "1rem" }}>
              <strong>{p.name}</strong>
              {p.url && (
                <span> — <a href={p.url} target="_blank" rel="noreferrer">{p.url}</a></span>
              )}
              <p>{p.description}</p>
              <div><strong>Technologies:</strong> {p.technologies.join(", ")}</div>
            </div>
          ))}
        </>
      )}

      {educationCert && (
        <>
          <h3>Education & Certifications</h3>
          {educationCert.education.map((edu, i) => (
            <p key={i}><strong>{edu.school}</strong> — {edu.degree}</p>
          ))}
          <p><strong>Certifications:</strong> {educationCert.certifications.join(", ")}</p>
        </>
      )}

      {keywords && (
        <>
          <h3>Keywords</h3>
          <p>{keywords.items.join(", ")}</p>
        </>
      )}
    </div>
  );
}
