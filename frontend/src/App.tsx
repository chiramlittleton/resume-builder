import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    experience: [
      {
        company: "",
        role: "",
        date: "",
        bullets: [""],
      },
    ],
  });

  const handleChange = (field: string, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleExperienceChange = (index: number, field: string, value: string) => {
    const updated = [...form.experience];
    updated[index][field] = value;
    setForm((prev) => ({ ...prev, experience: updated }));
  };

  const handleBulletChange = (expIdx: number, bulletIdx: number, value: string) => {
    const updated = [...form.experience];
    updated[expIdx].bullets[bulletIdx] = value;
    setForm((prev) => ({ ...prev, experience: updated }));
  };

  const submit = async () => {
    try {
      const res = await axios.post("http://localhost:8000/generate-resume", form, {
        responseType: "blob",
      });
      const blob = new Blob([res.data], { type: "application/pdf" });
      const url = URL.createObjectURL(blob);
      window.open(url, "_blank");
    } catch (err) {
      console.error("Resume generation failed:", err);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Resume Builder</h1>
      <input placeholder="Name" value={form.name} onChange={(e) => handleChange("name", e.target.value)} />
      <br />
      <input placeholder="Email" value={form.email} onChange={(e) => handleChange("email", e.target.value)} />
      <br />
      <input placeholder="Phone" value={form.phone} onChange={(e) => handleChange("phone", e.target.value)} />
      <br />
      <h3>Experience</h3>
      {form.experience.map((exp, i) => (
        <div key={i}>
          <input
            placeholder="Company"
            value={exp.company}
            onChange={(e) => handleExperienceChange(i, "company", e.target.value)}
          />
          <input
            placeholder="Role"
            value={exp.role}
            onChange={(e) => handleExperienceChange(i, "role", e.target.value)}
          />
          <input
            placeholder="Date"
            value={exp.date}
            onChange={(e) => handleExperienceChange(i, "date", e.target.value)}
          />
          <br />
          {exp.bullets.map((b, j) => (
            <input
              key={j}
              placeholder={`Bullet ${j + 1}`}
              value={b}
              onChange={(e) => handleBulletChange(i, j, e.target.value)}
            />
          ))}
        </div>
      ))}
      <br />
      <button onClick={submit}>Generate Resume PDF</button>
    </div>
  );
};

export default App;
