import { useState } from 'react';
import api from '../api';
import { RefreshCw, Target, Edit3 } from 'lucide-react';

export default function Results({ results, onNewAnalysis }) {
  const [selectedBullet, setSelectedBullet] = useState(null);
  const [rewrites, setRewrites] = useState([]);
  const [rewriting, setRewriting] = useState(false);

  const handleRewrite = async (bullet) => {
    setSelectedBullet(bullet);
    setRewriting(true);
    const res = await api.post("/rewrite/", { bullet, job_description: "Full job description" });
    setRewrites(res.data);
    setRewriting(false);
  };

  return (
    <div className="bg-white rounded-3xl shadow-xl p-10 space-y-12">
      {/* SCORE CIRCLE */}
      <div className="flex flex-col items-center">
        <div className="relative w-48 h-48">
          <svg className="w-48 h-48 -rotate-90" viewBox="0 0 36 36">
            <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#e5e7eb" strokeWidth="3" />
            <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831" fill="none" stroke="#3b82f6" strokeWidth="3" strokeDasharray={`${results.match_score}, 100`} />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center text-6xl font-bold">{results.match_score}<span className="text-2xl">%</span></div>
        </div>
        <p className="mt-4 text-xl font-semibold">Resume Match Score</p>
      </div>

      {/* SKILL GAP BARS */}
      <div>
        <h3 className="font-semibold mb-4 flex items-center gap-2"><Target className="w-5 h-5" /> Missing Skills</h3>
        {results.missing_skills.map((skill, i) => (
          <div key={i} className="flex items-center gap-4 mb-3">
            <div className="w-28 font-medium text-red-600">{skill}</div>
            <div className="flex-1 h-3 bg-slate-200 rounded-full"><div className="h-full bg-red-500 rounded-full" style={{width: `${100 - i*15}%`}}></div></div>
          </div>
        ))}
      </div>

      {/* BULLET REWRITER */}
      <div>
        <h3 className="font-semibold mb-4 flex items-center gap-2"><Edit3 className="w-5 h-5" /> Click any bullet to rewrite</h3>
        {results.suggested_edits.map((bullet, i) => (
          <div key={i} onClick={() => handleRewrite(bullet)} className="p-5 bg-slate-50 hover:bg-blue-50 rounded-2xl cursor-pointer mb-3">
            {bullet}
          </div>
        ))}
      </div>

      {selectedBullet && (
        <div className="border border-blue-200 bg-blue-50 p-6 rounded-3xl">
          <h4>AI Rewritten Versions:</h4>
          {rewriting ? <p>Rewriting...</p> : rewrites.map((r, i) => <div key={i} className="p-3 bg-white mt-2 rounded-xl">• {r}</div>)}
        </div>
      )}

      <button onClick={onNewAnalysis} className="w-full py-4 border rounded-2xl flex items-center justify-center gap-2">
        <RefreshCw className="w-5 h-5" /> New Analysis
      </button>
    </div>
  );
}