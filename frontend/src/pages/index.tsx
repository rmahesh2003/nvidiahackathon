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
  Globe
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

      const uploadResponse = await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const { upload_id } = uploadResponse.data;
      setUploadId(upload_id);
      setAnalysisStatus('analyzing');

      // Start analysis
      await axios.post(`http://localhost:8000/analyze/${upload_id}`);

      // Poll for results
      pollForResults(upload_id);
    } catch (err) {
      setError('Upload failed. Please try again.');
      setAnalysisStatus('error');
    }
  }, []);

  const pollForResults = async (id: string) => {
    const pollInterval = setInterval(async () => {
      try {
        const [statusResponse, resultResponse] = await Promise.all([
          axios.get(`http://localhost:8000/status/${id}`),
          axios.get(`http://localhost:8000/analyze/${id}`)
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
        return <Loader2 className="w-4 h-4 animate-spin text-blue-500" />;
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-500" />;
      default:
        return <div className="w-4 h-4 bg-gray-300 rounded-full" />;
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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Brain className="w-12 h-12 text-blue-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900">DocuSynth AI</h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Multi-agent code intelligence system that auto-generates documentation and provides insights across your codebase
          </p>
        </div>

        {/* Upload Section */}
        {analysisStatus === 'idle' && (
          <div className="max-w-2xl mx-auto mb-8">
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                isDragActive
                  ? 'border-blue-400 bg-blue-50'
                  : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50'
              }`}
            >
              <input {...getInputProps()} />
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-lg font-medium text-gray-700 mb-2">
                {isDragActive ? 'Drop your codebase here' : 'Upload your codebase'}
              </p>
              <p className="text-gray-500">
                Drag and drop a .zip file containing your codebase, or click to browse
              </p>
            </div>
          </div>
        )}

        {/* Analysis Progress */}
        {analysisStatus === 'analyzing' && (
          <div className="max-w-2xl mx-auto mb-8">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center mb-4">
                <Loader2 className="w-6 h-6 animate-spin text-blue-500 mr-3" />
                <h2 className="text-xl font-semibold text-gray-900">Analyzing Codebase</h2>
              </div>
              
              {/* Progress Bar */}
              <div className="mb-6">
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span>Progress</span>
                  <span>{Math.round(progress * 100)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progress * 100}%` }}
                  />
                </div>
              </div>

              {/* Agent Status */}
              {agentStatus && (
                <div className="space-y-3">
                  <h3 className="font-medium text-gray-900">Agent Status</h3>
                  {Object.entries(agentStatus).map(([agent, status]) => (
                    agent !== 'overall_progress' && (
                      <div key={agent} className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">{getAgentName(agent)}</span>
                        {getAgentIcon(status)}
                      </div>
                    )
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="max-w-2xl mx-auto mb-8">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center">
                <AlertCircle className="w-5 h-5 text-red-500 mr-3" />
                <p className="text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Results Display */}
        {result && (
          <div className="space-y-6">
            {/* Project Summary */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center mb-4">
                <FileText className="w-6 h-6 text-blue-500 mr-3" />
                <h2 className="text-xl font-semibold text-gray-900">Project Summary</h2>
              </div>
              <p className="text-gray-700 mb-4">{result.project_summary}</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div className="flex items-center">
                  <Code className="w-4 h-4 text-gray-500 mr-2" />
                  <span>{result.total_files} files analyzed</span>
                </div>
                <div className="flex items-center">
                  <Library className="w-4 h-4 text-gray-500 mr-2" />
                  <span>{result.libraries_used.length} libraries used</span>
                </div>
                {result.analysis_time && (
                  <div className="flex items-center">
                    <Zap className="w-4 h-4 text-gray-500 mr-2" />
                    <span>{result.analysis_time.toFixed(2)}s analysis time</span>
                  </div>
                )}
              </div>
            </div>

            {/* Files Analysis */}
            <div className="space-y-4">
              {result.files.map((file, index) => (
                <div key={index} className="bg-white rounded-lg shadow-lg p-6">
                  <div className="flex items-center mb-4">
                    <Code className="w-5 h-5 text-blue-500 mr-3" />
                    <h3 className="text-lg font-semibold text-gray-900">{file.filename}</h3>
                  </div>
                  
                  <p className="text-gray-700 mb-4">{file.summary}</p>

                  {/* Functions */}
                  {file.functions.length > 0 && (
                    <div className="mb-4">
                      <h4 className="font-medium text-gray-900 mb-2">Functions</h4>
                      <div className="space-y-2">
                        {file.functions.map((func, funcIndex) => (
                          <div key={funcIndex} className="bg-gray-50 rounded p-3">
                            <div className="flex items-center justify-between mb-1">
                              <span className="font-mono text-sm font-medium">{func.name}</span>
                              {func.returns && (
                                <span className="text-xs text-gray-500">→ {func.returns}</span>
                              )}
                            </div>
                            <p className="text-sm text-gray-600">{func.doc}</p>
                            {func.parameters.length > 0 && (
                              <p className="text-xs text-gray-500 mt-1">
                                Parameters: {func.parameters.join(', ')}
                              </p>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* External Libraries */}
                  {file.external_libraries.length > 0 && (
                    <div className="mb-4">
                      <h4 className="font-medium text-gray-900 mb-2">External Libraries</h4>
                      <div className="space-y-2">
                        {file.external_libraries.map((lib, libIndex) => (
                          <div key={libIndex} className="flex items-center justify-between bg-blue-50 rounded p-3">
                            <div>
                              <span className="font-medium text-sm">{lib.name}</span>
                              <p className="text-xs text-gray-600">{lib.doc_summary}</p>
                            </div>
                            {lib.link && (
                              <a
                                href={lib.link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-600 hover:text-blue-800"
                              >
                                <Globe className="w-4 h-4" />
                              </a>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Cross References */}
                  {file.cross_references.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Cross References</h4>
                      <div className="space-y-2">
                        {file.cross_references.map((ref, refIndex) => (
                          <div key={refIndex} className="bg-green-50 rounded p-3">
                            <div className="flex items-center mb-1">
                              <Link className="w-4 h-4 text-green-600 mr-2" />
                              <span className="font-mono text-sm font-medium">{ref.function}</span>
                            </div>
                            <p className="text-xs text-gray-600">
                              Used in: {ref.used_in.join(', ')}
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
          <div className="text-center mt-8">
            <button
              onClick={() => {
                setAnalysisStatus('idle');
                setProgress(0);
                setAgentStatus(null);
                setResult(null);
                setError(null);
                setUploadId(null);
              }}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
            >
              Analyze Another Codebase
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home; 