import React, { useState } from "react";
import axios from "axios";

export default function App() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const onFileChange = (e) => setFile(e.target.files[0]);

  const upload = async () => {
    if (!file) return setMessage("Choose a PDF first");
    const form = new FormData();
    form.append("file", file);
    try {
      const res = await axios.post("/api/docs/upload", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage(JSON.stringify(res.data));
    } catch (err) {
      setMessage(err.message);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>PDF Intelligence — Client</h2>
      <input type="file" accept="application/pdf" onChange={onFileChange} />
      <button onClick={upload} style={{ marginLeft: 8 }}>Upload</button>
      <pre style={{ marginTop: 20 }}>{message}</pre>
    </div>
  );
}
