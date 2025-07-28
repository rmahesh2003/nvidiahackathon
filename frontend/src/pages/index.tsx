import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { 
  Upload, 
  FileText, 
  Code, 
  Library, 
  Link, 
  CheckCircle, 
  AlertCircle, 
  Loader2,
  Brain,
  Zap,
  Globe,
  Sparkles,
  Cpu,
  Database,
  Network,
  ArrowRight,
  Play,
  Pause,
  RotateCcw
} from 'lucide-react';

interface AnalysisResult {
  files: Array<{
    filename: string;
    summary: string;
    functions: Array<{
      name: string;
      doc: string;
      parameters: string[];
      returns?: string;
    }>;
    external_libraries: Array<{
      name: string;
      doc_summary: string;
      link?: string;
    }>;
    cross_references: Array<{
      function: string;
      used_in: string[];
    }>;
  }>;
  project_summary: string;
  total_files: number;
  libraries_used: string[];
  analysis_time?: number;
}

interface AgentStatus {
  internal_doc_agent: string;
  library_doc_agent: string;
  context_manager_agent: string;
  overall_progress: number;
}

const Home: React.FC = () => {
  const [uploadId, setUploadId] = useState<string | null>(null);
  const [analysisStatus, setAnalysisStatus] = useState<'idle' | 'uploading' | 'analyzing' | 'completed' | 'error'>('idle');
  const [progress, setProgress] = useState(0);
  const [agentStatus, setAgentStatus] = useState<AgentStatus | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // API base URL - will work on both local and Brev
  const API_BASE = typeof window !== 'undefined' 
    ? `${window.location.protocol}//${window.location.hostname}:8000`
    : 'http://localhost:8000';

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    if (!file.name.endsWith('.zip')) {
      setError('Please upload a .zip file');
      return;
    }

    setAnalysisStatus('uploading');
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const uploadResponse = await axios.post(`${API_BASE}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const { upload_id } = uploadResponse.data;
      setUploadId(upload_id);
      setAnalysisStatus('analyzing');

      // Start analysis
      await axios.post(`${API_BASE}/analyze/${upload_id}`);

      // Poll for results
      pollForResults(upload_id);
    } catch (err) {
      setError('Upload failed. Please try again.');
      setAnalysisStatus('error');
    }
  }, [API_BASE]);

  const pollForResults = async (id: string) => {
    const pollInterval = setInterval(async () => {
      try {
        const [statusResponse, resultResponse] = await Promise.all([
          axios.get(`${API_BASE}/status/${id}`),
          axios.get(`${API_BASE}/analyze/${id}`)
        ]);

        setAgentStatus(statusResponse.data);
        setProgress(statusResponse.data.overall_progress);

        if (resultResponse.data.status === 'completed') {
          setResult(resultResponse.data.result);
          setAnalysisStatus('completed');
          clearInterval(pollInterval);
        } else if (resultResponse.data.status === 'failed') {
          setError(resultResponse.data.error || 'Analysis failed');
          setAnalysisStatus('error');
          clearInterval(pollInterval);
        }
      } catch (err) {
        setError('Failed to fetch analysis results');
        setAnalysisStatus('error');
        clearInterval(pollInterval);
      }
    }, 1000);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/zip': ['.zip']
    },
    multiple: false
  });

  const getAgentIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <Loader2 className="w-5 h-5 animate-spin text-emerald-500" />;
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-emerald-500" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <div className="w-5 h-5 bg-gray-300 rounded-full" />;
    }
  };

  const getAgentName = (agent: string) => {
    switch (agent) {
      case 'internal_doc_agent':
        return 'Internal Documentation Agent';
      case 'library_doc_agent':
        return 'Library Documentation Agent';
      case 'context_manager_agent':
        return 'Context Manager Agent';
      default:
        return agent;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-emerald-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute top-40 left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-emerald-400 to-blue-500 rounded-full blur-lg opacity-75 animate-pulse"></div>
              <Brain className="w-16 h-16 text-white relative z-10 mr-4" />
            </div>
            <div>
              <h1 className="text-6xl font-bold bg-gradient-to-r from-white to-emerald-200 bg-clip-text text-transparent">
                DocuSynth AI
              </h1>
              <div className="flex items-center justify-center mt-2">
                <Sparkles className="w-5 h-5 text-emerald-400 mr-2" />
                <span className="text-emerald-400 font-medium">Powered by NVIDIA Nemotron Super 49B</span>
              </div>
            </div>
          </div>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
            Multi-agent code intelligence system that auto-generates comprehensive documentation and provides 
            <span className="text-emerald-400 font-semibold"> intelligent insights</span> across your codebase
          </p>
        </div>

        {/* Upload Section */}
        {analysisStatus === 'idle' && (
          <div className="max-w-3xl mx-auto mb-12">
            <div
              {...getRootProps()}
              className={`backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl p-12 text-center cursor-pointer transition-all duration-300 hover:scale-105 hover:bg-white/15 ${
                isDragActive
                  ? 'border-emerald-400 bg-emerald-500/20 scale-105'
                  : 'hover:border-emerald-400/50'
              }`}
            >
              <input {...getInputProps()} />
              <div className="relative mb-6">
                <div className="absolute inset-0 bg-gradient-to-r from-emerald-400 to-blue-500 rounded-full blur-lg opacity-50"></div>
                <Upload className="w-16 h-16 text-white relative z-10 mx-auto" />
              </div>
              <h2 className="text-2xl font-bold text-white mb-4">
                {isDragActive ? 'Drop your codebase here' : 'Upload your codebase'}
              </h2>
              <p className="text-gray-300 text-lg mb-6">
                Drag and drop a .zip file containing your codebase, or click to browse
              </p>
              <div className="flex items-center justify-center space-x-4 text-sm text-gray-400">
                <div className="flex items-center">
                  <Cpu className="w-4 h-4 mr-2" />
                  <span>GPU Accelerated</span>
                </div>
                <div className="flex items-center">
                  <Database className="w-4 h-4 mr-2" />
                  <span>Multi-Agent AI</span>
                </div>
                <div className="flex items-center">
                  <Network className="w-4 h-4 mr-2" />
                  <span>Real-time Analysis</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Analysis Progress */}
        {analysisStatus === 'analyzing' && (
          <div className="max-w-3xl mx-auto mb-12">
            <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl p-8">
              <div className="flex items-center mb-6">
                <div className="relative mr-4">
                  <div className="absolute inset-0 bg-gradient-to-r from-emerald-400 to-blue-500 rounded-full blur-lg opacity-75 animate-pulse"></div>
                  <Loader2 className="w-8 h-8 text-white relative z-10 animate-spin" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-white">Analyzing Codebase</h2>
                  <p className="text-gray-300">Our AI agents are processing your code...</p>
                </div>
              </div>
              
              {/* Progress Bar */}
              <div className="mb-8">
                <div className="flex justify-between text-sm text-gray-300 mb-3">
                  <span>Analysis Progress</span>
                  <span className="text-emerald-400 font-semibold">{Math.round(progress * 100)}%</span>
                </div>
                <div className="w-full bg-white/10 rounded-full h-3 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-emerald-400 to-blue-500 h-3 rounded-full transition-all duration-500 ease-out"
                    style={{ width: `${progress * 100}%` }}
                  />
                </div>
              </div>

              {/* Agent Status */}
              {agentStatus && (
                <div className="space-y-4">
                  <h3 className="font-semibold text-white text-lg">Agent Status</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {Object.entries(agentStatus).map(([agent, status]) => (
                      agent !== 'overall_progress' && (
                        <div key={agent} className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-xl p-4">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm text-gray-300">{getAgentName(agent)}</span>
                            {getAgentIcon(status)}
                          </div>
                          <div className="w-full bg-white/10 rounded-full h-1">
                            <div
                              className={`h-1 rounded-full transition-all duration-300 ${
                                status === 'completed' ? 'bg-emerald-400' : 
                                status === 'active' ? 'bg-blue-400' : 'bg-gray-400'
                              }`}
                              style={{ width: status === 'completed' ? '100%' : status === 'active' ? '60%' : '0%' }}
                            />
                          </div>
                        </div>
                      )
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="max-w-3xl mx-auto mb-12">
            <div className="backdrop-blur-xl bg-red-500/10 border border-red-400/20 rounded-2xl p-6">
              <div className="flex items-center">
                <AlertCircle className="w-6 h-6 text-red-400 mr-4" />
                <div>
                  <h3 className="text-lg font-semibold text-red-400 mb-1">Error</h3>
                  <p className="text-red-300">{error}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Results Display */}
        {result && (
          <div className="space-y-8">
            {/* Project Summary */}
            <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl p-8">
              <div className="flex items-center mb-6">
                <div className="relative mr-4">
                  <div className="absolute inset-0 bg-gradient-to-r from-emerald-400 to-blue-500 rounded-full blur-lg opacity-75"></div>
                  <FileText className="w-8 h-8 text-white relative z-10" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-white">Project Summary</h2>
                  <p className="text-gray-300">Comprehensive analysis of your codebase</p>
                </div>
              </div>
              <p className="text-gray-200 text-lg leading-relaxed mb-6">{result.project_summary}</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                  <Code className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">{result.total_files}</div>
                  <div className="text-sm text-gray-300">Files Analyzed</div>
                </div>
                <div className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                  <Library className="w-8 h-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">{result.libraries_used.length}</div>
                  <div className="text-sm text-gray-300">Libraries Used</div>
                </div>
                {result.analysis_time && (
                  <div className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                    <Zap className="w-8 h-8 text-purple-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">{result.analysis_time.toFixed(2)}s</div>
                    <div className="text-sm text-gray-300">Analysis Time</div>
                  </div>
                )}
              </div>
            </div>

            {/* Files Analysis */}
            <div className="space-y-6">
              {result.files.map((file, index) => (
                <div key={index} className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl p-8">
                  <div className="flex items-center mb-6">
                    <div className="relative mr-4">
                      <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full blur-lg opacity-75"></div>
                      <Code className="w-6 h-6 text-white relative z-10" />
                    </div>
                    <h3 className="text-xl font-bold text-white">{file.filename}</h3>
                  </div>
                  
                  <p className="text-gray-200 mb-6 leading-relaxed">{file.summary}</p>

                  {/* Functions */}
                  {file.functions.length > 0 && (
                    <div className="mb-6">
                      <h4 className="font-semibold text-white mb-4 flex items-center">
                        <Database className="w-5 h-5 mr-2 text-emerald-400" />
                        Functions ({file.functions.length})
                      </h4>
                      <div className="grid gap-4">
                        {file.functions.map((func, funcIndex) => (
                          <div key={funcIndex} className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-xl p-4">
                            <div className="flex items-center justify-between mb-2">
                              <span className="font-mono text-sm font-semibold text-emerald-400">{func.name}</span>
                              {func.returns && (
                                <span className="text-xs text-gray-400 bg-white/10 px-2 py-1 rounded">→ {func.returns}</span>
                              )}
                            </div>
                            <p className="text-sm text-gray-300 mb-2">{func.doc}</p>
                            {func.parameters.length > 0 && (
                              <div className="flex flex-wrap gap-1">
                                {func.parameters.map((param, paramIndex) => (
                                  <span key={paramIndex} className="text-xs bg-blue-500/20 text-blue-300 px-2 py-1 rounded">
                                    {param}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* External Libraries */}
                  {file.external_libraries.length > 0 && (
                    <div className="mb-6">
                      <h4 className="font-semibold text-white mb-4 flex items-center">
                        <Library className="w-5 h-5 mr-2 text-blue-400" />
                        External Libraries ({file.external_libraries.length})
                      </h4>
                      <div className="grid gap-4">
                        {file.external_libraries.map((lib, libIndex) => (
                          <div key={libIndex} className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-xl p-4">
                            <div className="flex items-center justify-between">
                              <div className="flex-1">
                                <span className="font-semibold text-blue-400">{lib.name}</span>
                                <p className="text-sm text-gray-300 mt-1">{lib.doc_summary}</p>
                              </div>
                              {lib.link && (
                                <a
                                  href={lib.link}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-blue-400 hover:text-blue-300 transition-colors"
                                >
                                  <Globe className="w-5 h-5" />
                                </a>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Cross References */}
                  {file.cross_references.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-white mb-4 flex items-center">
                        <Link className="w-5 h-5 mr-2 text-purple-400" />
                        Cross References ({file.cross_references.length})
                      </h4>
                      <div className="grid gap-4">
                        {file.cross_references.map((ref, refIndex) => (
                          <div key={refIndex} className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-xl p-4">
                            <div className="flex items-center mb-2">
                              <Link className="w-4 h-4 text-purple-400 mr-2" />
                              <span className="font-mono text-sm font-semibold text-purple-400">{ref.function}</span>
                            </div>
                            <p className="text-sm text-gray-300">
                              Used in: <span className="text-purple-300">{ref.used_in.join(', ')}</span>
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Reset Button */}
        {(analysisStatus === 'completed' || analysisStatus === 'error') && (
          <div className="text-center mt-12">
            <button
              onClick={() => {
                setAnalysisStatus('idle');
                setProgress(0);
                setAgentStatus(null);
                setResult(null);
                setError(null);
                setUploadId(null);
              }}
              className="backdrop-blur-xl bg-gradient-to-r from-emerald-500 to-blue-500 hover:from-emerald-600 hover:to-blue-600 text-white font-semibold py-3 px-8 rounded-xl transition-all duration-300 hover:scale-105 flex items-center mx-auto"
            >
              <RotateCcw className="w-5 h-5 mr-2" />
              Analyze Another Codebase
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home; 