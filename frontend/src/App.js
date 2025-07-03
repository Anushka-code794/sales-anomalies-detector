import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [url, setUrl] = useState('');
  const [email, setEmail] = useState('');
  const [file, setFile] = useState(null);
  const [report, setReport] = useState('');

  const handleUrlSubmit = async () => {
    const res = await axios.post('http://localhost:8000/fetch-sheet/', {
      sheet_url: url,
      user_email: email
    });
    setReport(res.data.report);
  };

  const handleCsvSubmit = async () => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_email', email);
    const res = await axios.post('http://localhost:8000/upload-csv/', formData);
    setReport(res.data.report);
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>📊 Anomaly Detector</h2>
      <input type="email" placeholder="Your Email" value={email} onChange={e => setEmail(e.target.value)} />
      <br /><br />
      <input type="text" placeholder="Google Sheet URL" value={url} onChange={e => setUrl(e.target.value)} />
      <button onClick={handleUrlSubmit}>Analyze Sheet</button>
      <br /><br />
      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={handleCsvSubmit}>Upload CSV</button>
      <br /><br />
      <h3>🧾 Report</h3>
      <pre>{report}</pre>
    </div>
  );
}

export default App;
