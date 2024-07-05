import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import PropTypes from 'prop-types';

const DragDropUpload = ({ onFileUploaded }) => {
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    setIsUploading(true);
    const file = acceptedFiles[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/upload-dataset', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      onFileUploaded(data.dataset_path);
    } catch (error) {
      console.error('Error uploading dataset:', error);
      alert('Failed to upload dataset. Please try again.');
    } finally {
      setIsUploading(false);
    }
  }, [onFileUploaded]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div 
      {...getRootProps()} 
      className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
        ${isDragActive ? 'border-green-500 bg-green-100' : 'border-gray-300 hover:border-green-500'}
        ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}
      `}
    >
      <input {...getInputProps()} />
      {isUploading ? (
        <p className="text-gray-600">Uploading...</p>
      ) : isDragActive ? (
        <p className="text-green-600">Drop the file here...</p>
      ) : (
        <p className="text-gray-600">Drag and drop a dataset file here, or click to select a file</p>
      )}
    </div>
  );
};

DragDropUpload.propTypes = {
  onFileUploaded: PropTypes.func.isRequired,
};

export default DragDropUpload;