import { useState } from 'react';
import ModelSelector from './components/ModelSelector';
import ChatInterface from './components/ChatInterface';
import DragDropUpload from './components/DragDropUpload';
import './App.css';

const App = () => {
  const [selectedModel, setSelectedModel] = useState('');
  const [datasetPath, setDatasetPath] = useState('');
  const [isRAGSetup, setIsRAGSetup] = useState(false);

  const handleDatasetUploaded = (path) => {
    setDatasetPath(path);
  };

  const setupRAG = async () => {
    if (!selectedModel || !datasetPath) {
      alert('Please select a model and upload a dataset first.');
      return;
    }

    try {
      const response = await fetch('/api/setup-rag', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model: selectedModel, dataset_path: datasetPath }),
      });
      const data = await response.json();
      if (data.success) {
        setIsRAGSetup(true);
        alert('RAG system set up successfully!');
      } else {
        alert('Failed to set up RAG system. Please try again.');
      }
    } catch (error) {
      console.error('Error setting up RAG:', error);
      alert('An error occurred while setting up the RAG system.');
    }
  };

  return (
    <div className="min-h-screen bg-green-900 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="absolute inset-0 bg-gradient-to-r from-green-400 to-green-600 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <h1 className="text-3xl font-bold mb-8 text-center text-green-800">RAG LLM System</h1>
          
          <div className="space-y-8">
            <div className="bg-green-50 p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold mb-4 text-green-800">1. Select Model</h2>
              <ModelSelector onSelect={setSelectedModel} />
            </div>

            <div className="bg-green-50 p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold mb-4 text-green-800">2. Upload Dataset</h2>
              <DragDropUpload onFileUploaded={handleDatasetUploaded} />
              {datasetPath && (
                <p className="mt-2 text-sm text-green-600">Dataset uploaded: {datasetPath}</p>
              )}
            </div>

            <div className="bg-green-50 p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold mb-4 text-green-800">3. Set up RAG System</h2>
              <button
                onClick={setupRAG}
                className="w-full bg-green-600 text-white p-2 rounded hover:bg-green-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
                disabled={!selectedModel || !datasetPath}
              >
                Set up RAG System
              </button>
            </div>

            {isRAGSetup && (
              <div className="bg-green-50 p-6 rounded-lg shadow-md">
                <h2 className="text-xl font-semibold mb-4 text-green-800">4. Chat Interface</h2>
                <ChatInterface model={selectedModel} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;