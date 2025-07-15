import React, { useState } from 'react';
import { Button, TextField, Box, Typography, LinearProgress } from '@mui/material';
import { uploadDocument } from '../api';

const UploadForm: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setMessage('');
    try {
      const res = await uploadDocument(file, title);
      setMessage(res.message);
      setFile(null);
      setTitle('');
    } catch (err: any) {
      setMessage(err.response?.data?.detail || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
      <Typography variant="h6" gutterBottom>Upload Medical Document</Typography>
      <TextField
        label="Title (optional)"
        value={title}
        onChange={e => setTitle(e.target.value)}
        fullWidth
        sx={{ mb: 2 }}
      />
      <Button variant="contained" component="label" sx={{ mb: 2 }}>
        Choose File
        <input type="file" hidden onChange={handleFileChange} />
      </Button>
      {file && <Typography variant="body2">Selected: {file.name}</Typography>}
      <Box sx={{ mt: 2 }}>
        <Button type="submit" variant="contained" disabled={!file || loading}>
          Upload
        </Button>
      </Box>
      {loading && <LinearProgress sx={{ mt: 2 }} />}
      {message && <Typography sx={{ mt: 2 }}>{message}</Typography>}
    </Box>
  );
};

export default UploadForm; 