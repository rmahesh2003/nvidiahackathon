import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

interface AnalysisResult {
  project_summary: string;
  files: Array<{
    filename: string;
    summary: string;
    functions: Array<{
      name: string;
      summary: string;
    }>;
    external_libraries: Array<{
      name: string;
      link: string;
    }>;
  }>;
  cross_references: Array<{
    from: string;
    to: string;
    type: string;
    description: string;
  }>;
  external_libraries_summary: Array<{
    name: string;
    usage: string;
    link: string;
  }>;
  analysis_metadata?: {
    total_files: number;
    total_functions: number;
    total_libraries: number;
  };
}

const CompleteDemo: React.FC = () => {
  const [uploadId, setUploadId] = useState<string>('');
  const [analysisStatus, setAnalysisStatus] = useState<string>('');
  const [progress, setProgress] = useState<number>(0);
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file.name.endsWith('.zip')) {
      alert('Please upload a zip file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://204.52.27.91:8000/upload', formData);
      const { upload_id } = response.data;
      setUploadId(upload_id);
      
      // Start analysis
      await startAnalysis(upload_id);
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed');
    }
  }, []);

  const startAnalysis = async (id: string) => {
    try {
      setIsAnalyzing(true);
      setAnalysisStatus('Starting analysis...');
      setProgress(0);

      // Start analysis
      await axios.post(`http://204.52.27.91:8000/analyze/${id}`);
      
      // Poll for status and results
      pollAnalysis(id);
    } catch (error) {
      console.error('Analysis error:', error);
      setAnalysisStatus('Analysis failed');
      setIsAnalyzing(false);
    }
  };

  const pollAnalysis = async (id: string) => {
    const pollInterval = setInterval(async () => {
      try {
        // Check status
        const statusResponse = await axios.get(`http://204.52.27.91:8000/status/${id}`);
        const { status, progress, message } = statusResponse.data;
        
        setAnalysisStatus(message);
        setProgress(progress);

        if (status === 'completed') {
          // Get results
          const resultsResponse = await axios.get(`http://204.52.27.91:8000/analyze/${id}`);
          setResults(resultsResponse.data);
          setIsAnalyzing(false);
          clearInterval(pollInterval);
        } else if (status === 'error') {
          setAnalysisStatus('Analysis failed');
          setIsAnalyzing(false);
          clearInterval(pollInterval);
        }
      } catch (error) {
        console.error('Polling error:', error);
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

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            DocuSynth AI - Complete Multi-Agent System
          </h1>
          <p className="text-xl text-gray-600">
            Upload any codebase and watch our 3 AI agents analyze it in real-time
          </p>
        </div>

        {/* Upload Section */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">Upload Your Codebase</h2>
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
              isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <input {...getInputProps()} />
            <div className="text-6xl mb-4">📁</div>
            <p className="text-lg text-gray-600">
              {isDragActive ? 'Drop the zip file here' : 'Drag & drop a zip file, or click to select'}
            </p>
            <p className="text-sm text-gray-500 mt-2">Supports .js, .jsx, .ts, .tsx, .py files</p>
          </div>
        </div>

        {/* Analysis Status */}
        {isAnalyzing && (
          <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
            <h2 className="text-2xl font-semibold mb-4">AI Agents at Work</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-700">{analysisStatus}</span>
                <span className="text-blue-600 font-semibold">{progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
              <div className="text-sm text-gray-500">
                InternalDocAgent • LibraryDocAgent • ContextManagerAgent
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {results && (
          <div className="space-y-8">
            {/* Project Summary */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-semibold mb-4">Project Summary</h2>
              <p className="text-lg text-gray-700">{results.project_summary}</p>
              {results.analysis_metadata && (
                <div className="grid grid-cols-3 gap-4 mt-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{results.analysis_metadata.total_files}</div>
                    <div className="text-sm text-gray-500">Files</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">{results.analysis_metadata.total_functions}</div>
                    <div className="text-sm text-gray-500">Functions</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">{results.analysis_metadata.total_libraries}</div>
                    <div className="text-sm text-gray-500">Libraries</div>
                  </div>
                </div>
              )}
            </div>

            {/* Files Analysis */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-semibold mb-4">File Analysis</h2>
              <div className="space-y-6">
                {results.files.map((file, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-blue-600 mb-2">{file.filename}</h3>
                    <p className="text-gray-700 mb-4">{file.summary}</p>
                    
                    {/* Functions */}
                    {file.functions.length > 0 && (
                      <div className="mb-4">
                        <h4 className="font-semibold text-gray-800 mb-2">Functions:</h4>
                        <div className="space-y-2">
                          {file.functions.map((func, funcIndex) => (
                            <div key={funcIndex} className="bg-gray-50 p-3 rounded">
                              <div className="font-medium text-gray-800">{func.name}</div>
                              <div className="text-sm text-gray-600">{func.summary}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* External Libraries */}
                    {file.external_libraries.length > 0 && (
                      <div>
                        <h4 className="font-semibold text-gray-800 mb-2">External Libraries:</h4>
                        <div className="space-y-2">
                          {file.external_libraries.map((lib, libIndex) => (
                            <a
                              key={libIndex}
                              href={lib.link}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded text-sm hover:bg-blue-200"
                            >
                              {lib.name}
                            </a>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Cross References */}
            {results.cross_references.length > 0 && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-semibold mb-4">Cross References</h2>
                <div className="space-y-3">
                  {results.cross_references.map((ref, index) => (
                    <div key={index} className="bg-gray-50 p-4 rounded">
                      <div className="font-medium text-gray-800">
                        {ref.from} → {ref.to}
                      </div>
                      <div className="text-sm text-gray-600">{ref.description}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* External Libraries Summary */}
            {results.external_libraries_summary.length > 0 && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-semibold mb-4">External Libraries</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {results.external_libraries_summary.map((lib, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold text-gray-800">{lib.name}</h3>
                        <a
                          href={lib.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-800 text-sm"
                        >
                          Docs →
                        </a>
                      </div>
                      <p className="text-sm text-gray-600">{lib.usage}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default CompleteDemo; 