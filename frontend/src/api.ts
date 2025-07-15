import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export const uploadDocument = async (file: File, title?: string) => {
  const formData = new FormData();
  formData.append('file', file);
  if (title) formData.append('title', title);
  const response = await axios.post(`${API_BASE}/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const chatWithBot = async (question: string) => {
  const response = await axios.post(`${API_BASE}/chat`, { question });
  return response.data;
}; 