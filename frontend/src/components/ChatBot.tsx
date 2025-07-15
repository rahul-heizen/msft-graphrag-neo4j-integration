import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Paper, List, ListItem, ListItemText, Divider, CircularProgress } from '@mui/material';
import { chatWithBot } from '../api';

interface Message {
  question: string;
  answer: string;
  sources: string[];
}

const ChatBot: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setError('');
    try {
      const res = await chatWithBot(input);
      setMessages(prev => [...prev, { question: input, answer: res.answer, sources: res.sources }]);
      setInput('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get response');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>Medical Chatbot</Typography>
      <Paper sx={{ p: 2, mb: 2, minHeight: 300, maxHeight: 400, overflow: 'auto' }}>
        <List>
          {messages.map((msg, idx) => (
            <React.Fragment key={idx}>
              <ListItem alignItems="flex-start">
                <ListItemText
                  primary={<><b>You:</b> {msg.question}</>}
                  secondary={<>
                    <b>Bot:</b> {msg.answer}
                    {msg.sources.length > 0 && (
                      <Box sx={{ mt: 1 }}>
                        <Typography variant="caption" color="text.secondary">
                          Sources: {msg.sources.join(', ')}
                        </Typography>
                      </Box>
                    )}
                  </>}
                />
              </ListItem>
              <Divider component="li" />
            </React.Fragment>
          ))}
        </List>
        {loading && <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}><CircularProgress size={24} /></Box>}
      </Paper>
      <Box sx={{ display: 'flex', gap: 2 }}>
        <TextField
          label="Ask a medical question..."
          value={input}
          onChange={e => setInput(e.target.value)}
          fullWidth
          onKeyDown={e => { if (e.key === 'Enter') handleSend(); }}
          disabled={loading}
        />
        <Button variant="contained" onClick={handleSend} disabled={loading || !input.trim()}>
          Send
        </Button>
      </Box>
      {error && <Typography color="error" sx={{ mt: 2 }}>{error}</Typography>}
    </Box>
  );
};

export default ChatBot; 