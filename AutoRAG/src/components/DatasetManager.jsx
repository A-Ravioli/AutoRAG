import { useState } from 'react';
import PropTypes from 'prop-types';

const DatasetManager = ({ onDatasetLoaded }) => {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/upload-dataset', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      onDatasetLoaded(data.dataset_path);
    } catch (error) {
      console.error('Error uploading dataset:', error);
      alert('Failed to upload dataset. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mb-4">
      <h2 className="text-xl font-bold mb-2">Dataset Manager</h2>
      <form onSubmit={handleSubmit} className="flex flex-col space-y-2">
        <input
          type="file"
          onChange={handleFileChange}
          className="border p-2 rounded"
          accept=".csv,.txt,.json"
        />
        <button
          type="submit"
          className="bg-green-500 text-white p-2 rounded hover:bg-green-600 disabled:bg-gray-400"
          disabled={!file || isLoading}
        >
          {isLoading ? 'Uploading...' : 'Upload Dataset'}
        </button>
      </form>
    </div>
  );
};

DatasetManager.propTypes = {
  onDatasetLoaded: PropTypes.func.isRequired,
};

export default DatasetManager;