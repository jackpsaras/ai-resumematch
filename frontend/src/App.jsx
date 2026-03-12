import { useState } from 'react';
import UploadForm from './components/UploadForm';
import Results from './components/Results';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50 py-12">
      <div className="max-w-4xl mx-auto px-6">
        <h1 className="text-5xl font-bold text-center mb-2">ResumeMatch AI</h1>
        <p className="text-center text-slate-600 mb-12">Upload → AI Match Score + Skill Gaps + Bullet Rewrites</p>

        {!results ? (
          <UploadForm onAnalysisComplete={setResults} setLoading={setLoading} />
        ) : (
          <Results results={results} onNewAnalysis={() => setResults(null)} />
        )}

        {loading && <div className="text-center py-12">Analyzing with AI...</div>}
      </div>
    </div>
  );
}

export default App;