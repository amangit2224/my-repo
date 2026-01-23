import React, { useState, useEffect, useRef } from 'react';
import { reportAPI } from '../utils/api';

function ChatSection({ reportId, isOpen, onClose }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const messagesEndRef = useRef(null);

  // Fetch suggestions when component opens
  useEffect(() => {
    if (isOpen && reportId) {
      fetchSuggestions();
      // Add welcome message
      setMessages([{
        role: 'assistant',
        content: "Hello! I'm here to help you understand your medical report. Ask me anything about your test results, what they mean, or what you should do next.",
        timestamp: new Date().toISOString()
      }]);
    }
  }, [isOpen, reportId]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchSuggestions = async () => {
    try {
      const response = await reportAPI.getChatSuggestions(reportId);
      setSuggestions(response.data.suggestions || []);
    } catch (error) {
      console.error('Failed to fetch suggestions:', error);
    }
  };

  const handleSendMessage = async (question = null) => {
    const userQuestion = question || input.trim();
    
    if (!userQuestion) return;

    // Add user message
    const userMessage = {
      role: 'user',
      content: userQuestion,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Send to backend
      const response = await reportAPI.chatWithReport(reportId, {
        question: userQuestion,
        history: messages
      });

      // Add AI response
      const aiMessage = {
        role: 'assistant',
        content: response.data.answer,
        timestamp: response.data.timestamp
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      
      // Add error message
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
        isError: true
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    handleSendMessage(suggestion);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (!isOpen) return null;

  return (
    <div style={{
      marginTop: '32px',
      border: '2px solid #E5E7EB',
      borderRadius: '12px',
      backgroundColor: 'white',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)'
    }}>
      {/* Header */}
      <div style={{
        padding: '20px 24px',
        borderBottom: '2px solid #E5E7EB',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        backgroundColor: '#F9FAFB'
      }}>
        <div>
          <h3 style={{ margin: 0, fontSize: '20px', fontWeight: '600', color: '#1F2937' }}>
            💬 Chat About Your Report
          </h3>
          <p style={{ margin: '4px 0 0', fontSize: '14px', color: '#6B7280' }}>
            Ask questions about your test results
          </p>
        </div>
        <button
          onClick={onClose}
          style={{
            background: '#E5E7EB',
            border: 'none',
            color: '#374151',
            fontSize: '24px',
            cursor: 'pointer',
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'background 0.2s'
          }}
          onMouseEnter={(e) => e.target.style.background = '#D1D5DB'}
          onMouseLeave={(e) => e.target.style.background = '#E5E7EB'}
        >
          ×
        </button>
      </div>

      {/* Suggested Questions */}
      {suggestions.length > 0 && messages.length <= 1 && (
        <div style={{
          padding: '16px 24px',
          backgroundColor: '#FFFBEB',
          borderBottom: '1px solid #FDE68A'
        }}>
          <p style={{ 
            margin: '0 0 12px', 
            fontSize: '14px', 
            fontWeight: '600', 
            color: '#92400E' 
          }}>
            💡 Suggested Questions:
          </p>
          <div style={{ 
            display: 'flex', 
            flexWrap: 'wrap', 
            gap: '8px' 
          }}>
            {suggestions.map((suggestion, idx) => (
              <button
                key={idx}
                onClick={() => handleSuggestionClick(suggestion)}
                style={{
                  padding: '8px 16px',
                  backgroundColor: 'white',
                  border: '1px solid #FCD34D',
                  borderRadius: '20px',
                  fontSize: '13px',
                  color: '#92400E',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  fontWeight: '500'
                }}
                onMouseEnter={(e) => {
                  e.target.style.backgroundColor = '#FEF3C7';
                  e.target.style.borderColor = '#F59E0B';
                }}
                onMouseLeave={(e) => {
                  e.target.style.backgroundColor = 'white';
                  e.target.style.borderColor = '#FCD34D';
                }}
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Messages */}
      <div style={{
        padding: '24px',
        maxHeight: '500px',
        overflowY: 'auto',
        minHeight: '300px'
      }}>
        {messages.map((message, idx) => (
          <div
            key={idx}
            style={{
              marginBottom: '16px',
              display: 'flex',
              justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start'
            }}
          >
            <div style={{
              maxWidth: '75%',
              padding: '12px 16px',
              borderRadius: message.role === 'user' ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
              backgroundColor: message.role === 'user' ? '#3B82F6' : '#F3F4F6',
              color: message.role === 'user' ? 'white' : '#1F2937',
              fontSize: '15px',
              lineHeight: '1.6',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word'
            }}>
              {message.content}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            color: '#6B7280',
            fontSize: '14px'
          }}>
            <div className="spinner" style={{ 
              width: '16px', 
              height: '16px', 
              borderWidth: '2px' 
            }}></div>
            Typing...
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div style={{
        padding: '16px 24px',
        borderTop: '2px solid #E5E7EB',
        backgroundColor: '#F9FAFB'
      }}>
        <div style={{ display: 'flex', gap: '12px' }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about your report..."
            disabled={loading}
            style={{
              flex: 1,
              padding: '12px 16px',
              border: '2px solid #E5E7EB',
              borderRadius: '8px',
              fontSize: '15px',
              outline: 'none',
              transition: 'border-color 0.2s',
              backgroundColor: 'white'
            }}
            onFocus={(e) => e.target.style.borderColor = '#3B82F6'}
            onBlur={(e) => e.target.style.borderColor = '#E5E7EB'}
          />
          <button
            onClick={() => handleSendMessage()}
            disabled={!input.trim() || loading}
            style={{
              padding: '12px 24px',
              backgroundColor: input.trim() && !loading ? '#3B82F6' : '#D1D5DB',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '15px',
              fontWeight: '600',
              cursor: input.trim() && !loading ? 'pointer' : 'not-allowed',
              transition: 'background 0.2s'
            }}
            onMouseEnter={(e) => {
              if (input.trim() && !loading) {
                e.target.style.backgroundColor = '#2563EB';
              }
            }}
            onMouseLeave={(e) => {
              if (input.trim() && !loading) {
                e.target.style.backgroundColor = '#3B82F6';
              }
            }}
          >
            Send
          </button>
        </div>
        <p style={{
          margin: '8px 0 0',
          fontSize: '12px',
          color: '#9CA3AF',
          textAlign: 'center'
        }}>
          Press Enter to send • Shift + Enter for new line
        </p>
      </div>
    </div>
  );
}

export default ChatSection;