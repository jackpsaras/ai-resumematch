import { useState } from 'react';
import api from '../api';

// UploadForm component allows users to upload their resume as a PDF and paste the job description. On submission, it sends the data to the backend for analysis and handles the response or any errors. It also manages loading state to provide feedback to the user while the analysis is being performed.
export default function UploadForm({ onAnalysisComplete, setLoading }) {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please select a PDF");
    if (!jobDesc.trim()) return alert("Please paste the job description");

    setLoading(true);
    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_description", jobDesc);

    // send the form data to the backend for analysis, handle the response or any errors, and update the loading state accordingly
    try {
      const res = await api.post("/analyze/", formData);
      onAnalysisComplete(res.data);
    } catch (err) {
      alert("Error: " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };
  // simple form with file input for PDF and textarea for job description, styled with Tailwind CSS. On submit, it sends the data to the backend and handles the response or any errors.
  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-3xl shadow-xl p-10">
      <input type="file" accept=".pdf" onChange={e => setFile(e.target.files[0])} className="block w-full mb-6" />
      <textarea
        value={jobDesc}
        onChange={e => setJobDesc(e.target.value)}
        placeholder="Paste the FULL job description here..."
        className="w-full h-48 p-4 border border-slate-300 rounded-2xl focus:outline-none focus:border-blue-500"
      />
      <button type="submit" className="mt-8 w-full bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-2xl font-semibold text-lg">
        Analyze My Resume
      </button>
    </form>
  );
}