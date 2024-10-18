// FileUpload.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const navigate = useNavigate();

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Upload failed:', errorData.error); // Log the error
                alert(`Error: ${errorData.error}`);
                return; // Exit early on error
            }

            const data = await response.json();
            console.log('Data received:', data); // Log the response data
            navigate('/results', { state: { results: data.summary } });
        } catch (err) {
            console.error('Failed to upload file:', err);
            alert('Failed to upload file');
        }
    };

    return (
        <div className="upload-container">
            <h1>Upload Financial Data</h1>
            <form onSubmit={handleSubmit}>
                <input type="file" accept=".json" onChange={handleFileChange} required />
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default FileUpload;
