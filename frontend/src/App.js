import React, { useState } from 'react';
import axios from 'axios';

const UploadPDF = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [responseText, setResponseText] = useState('');
  const [loading, setLoading] = useState(false);
  const [filePreview, setFilePreview] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setFilePreview(e.target.result);
      };
      reader.readAsDataURL(file);
    } else {
      setFilePreview(null);
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResponseText(response.data); // Update response text state
    } catch (error) {
      console.error('Error:', error);
      setError('An error occurred while uploading.'); // Provide user feedback for error
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="upload-area">
        <h1>Document Summarizer</h1>
        <div className="file-preview">
          {filePreview && (
            <img src={filePreview} alt="Document Preview" />
          )}
        </div>
        {selectedFile ? (
          <p className="file-name">Selected File: {selectedFile.name}</p>
        ) : (
          <label htmlFor="fileInput" className="fileLabel">
            <input id="fileInput" type="file" onChange={handleFileChange} />
            Choose File
          </label>
        )}
        <button onClick={handleSubmit} disabled={loading || !selectedFile}>
          {loading ? 'Uploading...' : 'Upload'}
        </button>
        {responseText && <p className="response success">{responseText}</p>}
        {error && <p className="response error">{error}</p>}
      </div>
      <style jsx>{`
        .container {
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          background-color: #f5f5f5;
        }

        .upload-area {
          background-color: #ffffff;
          padding: 50px;
          border-radius: 10px;
          text-align: center;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
          border: 2px dashed #cccccc;
        }

        .fileLabel {
          margin-right: 20px;
          background-color: #007bff;
          color: #ffffff;
          padding: 10px 20px;
          border-radius: 5px;
          cursor: pointer;
          transition: background-color 0.3s;
        }

        .fileLabel input {
          display: none;
        }

        .fileLabel:hover {
          background-color: #0056b3;
        }

        button {
          padding: 13px 32px;
          margin-top: 25px;
          background-color: #007bff;
          color: #fff;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          transition: background-color 0.3s;
        }

        button:disabled {
          background-color: #cccccc;
          cursor: not-allowed;
        }

        button:hover {
          background-color: #0056b3;
        }

        .response {
          margin-top: 20px;
          padding: 20px;
          border-radius: 5px;
        }

        .response.success {
          background-color: #d4edda;
          color: #155724;
        }

        .response.error {
          background-color: #f8d7da;
          color: #721c24;
        }

        .file-name {
          margin-bottom: 20px;
        }

        .file-preview img {
          max-width: 100%;
          max-height: 300px;
          border-radius: 5px;
        }
      `}</style>
    </div>
  );
};

export default UploadPDF;
