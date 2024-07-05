import { useState, useRef, useEffect } from 'react';
import PropTypes from 'prop-types';

const ChatInterface = ({ model }) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input, model_name: model }),
      });
      const data = await response.json();
      const assistantMessage = { role: 'assistant', content: data.response };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error querying the model:', error);
      const errorMessage = { role: 'system', content: 'An error occurred while processing your request.' };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="h-96 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-3/4 p-3 rounded-lg ${
              msg.role === 'user' ? 'bg-green-500 text-white' : 
              msg.role === 'assistant' ? 'bg-gray-200 text-black' :
              'bg-red-500 text-white'
            }`}>
              {msg.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-center">
            <div className="bg-gray-200 text-black p-3 rounded-lg">
              Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="flex p-4 bg-gray-100">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-grow p-2 border rounded-l focus:outline-none focus:ring-2 focus:ring-green-500"
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button 
          type="submit" 
          className="bg-green-600 text-white p-2 rounded-r hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          disabled={isLoading}
        >
          Send
        </button>
      </form>
    </div>
  );
};

ChatInterface.propTypes = {
  model: PropTypes.string.isRequired,
};

export default ChatInterface;