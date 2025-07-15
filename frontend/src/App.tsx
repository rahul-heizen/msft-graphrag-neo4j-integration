import React from 'react';
import { Container, Box, Typography, Paper } from '@mui/material';
import UploadForm from './components/UploadForm';
import ChatBot from './components/ChatBot';

const App: React.FC = () => {
  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
        <Typography variant="h4" gutterBottom align="center">
          Medical Chatbot (GraphRAG + Neo4j)
        </Typography>
        <Typography variant="subtitle1" align="center" sx={{ mb: 2 }}>
          Upload medical documents and chat with the AI assistant.
        </Typography>
        <UploadForm />
        <ChatBot />
      </Paper>
    </Container>
  );
};

export default App;
