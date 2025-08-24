// import { useState } from 'react';

// export const Chatbot = () => {
//     const [message, setMessage] = useState('');
//     const [messages, setMessages] = useState([]);
//     const [loading, setLoading] = useState(false);
//     const [error, setError] = useState('');

//     const API_BASE_URL = 'http://localhost:8000/api/chatbot'; // Adjust this to your Django server URL

//     const sendMessage = async () => {
//         if (!message.trim()) {
//             setError('Please enter a message');
//             return;
//         }

//         setLoading(true);
//         setError('');

//         // Add user message to chat
//         const userMessage = {
//             role: 'user',
//             content: message,
//             timestamp: new Date().toLocaleTimeString()
//         };
//         setMessages((prev) => [...prev, userMessage]);

//         try {
//             const response = await fetch(`${API_BASE_URL}/chat/`, {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json'
//                 },
//                 body: JSON.stringify({
//                     message: message
//                 })
//             });

//             const data = await response.json();

//             if (data.success) {
//                 // Add AI response to chat
//                 const aiMessage = {
//                     role: 'assistant',
//                     content: data.response,
//                     timestamp: new Date().toLocaleTimeString()
//                 };
//                 setMessages((prev) => [...prev, aiMessage]);
//             } else {
//                 setError(data.error || 'Failed to get response');
//                 // Add error message to chat
//                 const errorMessage = {
//                     role: 'error',
//                     content: `Error: ${data.error || 'Failed to get response'}`,
//                     timestamp: new Date().toLocaleTimeString()
//                 };
//                 setMessages((prev) => [...prev, errorMessage]);
//             }
//         } catch (err) {
//             setError('Network error: Could not connect to server');
//             const errorMessage = {
//                 role: 'error',
//                 content: 'Network error: Could not connect to server',
//                 timestamp: new Date().toLocaleTimeString()
//             };
//             setMessages((prev) => [...prev, errorMessage]);
//         }

//         setMessage('');
//         setLoading(false);
//     };

//     const handleKeyPress = (e) => {
//         if (e.key === 'Enter' && !e.shiftKey) {
//             e.preventDefault();
//             sendMessage();
//         }
//     };

//     const checkHealth = async () => {
//         try {
//             const response = await fetch(`${API_BASE_URL}/health/`);
//             const data = await response.json();
//             alert(`Health Status: ${data.status}\nMessage: ${data.message}`);
//         } catch (err) {
//             alert('Could not check health status');
//         }
//     };

//     const clearChat = () => {
//         setMessages([]);
//         setError('');
//     };

//     return (
//         <div
//             style={{
//                 maxWidth: '800px',
//                 margin: '20px auto',
//                 padding: '20px',
//                 border: '1px solid #ddd',
//                 borderRadius: '8px',
//                 fontFamily: 'Arial, sans-serif'
//             }}
//         >
//             <h2>Chatbot Test Interface</h2>

//             {/* Health Check Button */}
//             <div style={{ marginBottom: '20px' }}>
//                 <button
//                     onClick={checkHealth}
//                     style={{
//                         padding: '8px 16px',
//                         backgroundColor: '#007bff',
//                         color: 'white',
//                         border: 'none',
//                         borderRadius: '4px',
//                         cursor: 'pointer',
//                         marginRight: '10px'
//                     }}
//                 >
//                     Check Health
//                 </button>
//                 <button
//                     onClick={clearChat}
//                     style={{
//                         padding: '8px 16px',
//                         backgroundColor: '#dc3545',
//                         color: 'white',
//                         border: 'none',
//                         borderRadius: '4px',
//                         cursor: 'pointer'
//                     }}
//                 >
//                     Clear Chat
//                 </button>
//             </div>

//             {/* Error Display */}
//             {error && (
//                 <div
//                     style={{
//                         backgroundColor: '#f8d7da',
//                         color: '#721c24',
//                         padding: '10px',
//                         borderRadius: '4px',
//                         marginBottom: '20px',
//                         border: '1px solid #f5c6cb'
//                     }}
//                 >
//                     {error}
//                 </div>
//             )}

//             {/* Chat Messages */}
//             <div
//                 style={{
//                     height: '400px',
//                     border: '1px solid #ddd',
//                     borderRadius: '4px',
//                     padding: '10px',
//                     overflowY: 'auto',
//                     marginBottom: '20px',
//                     backgroundColor: '#f8f9fa'
//                 }}
//             >
//                 {messages.length === 0 ? (
//                     <p style={{ color: '#6c757d', fontStyle: 'italic' }}>
//                         No messages yet. Start a conversation!
//                     </p>
//                 ) : (
//                     messages.map((msg, index) => (
//                         <div
//                             key={index}
//                             style={{
//                                 marginBottom: '10px',
//                                 padding: '8px',
//                                 borderRadius: '4px',
//                                 backgroundColor:
//                                     msg.role === 'user'
//                                         ? '#e3f2fd'
//                                         : msg.role === 'error'
//                                         ? '#ffebee'
//                                         : '#f3e5f5',
//                                 borderLeft: `4px solid ${
//                                     msg.role === 'user'
//                                         ? '#2196f3'
//                                         : msg.role === 'error'
//                                         ? '#f44336'
//                                         : '#9c27b0'
//                                 }`
//                             }}
//                         >
//                             <div
//                                 style={{
//                                     fontSize: '12px',
//                                     color: '#666',
//                                     marginBottom: '4px',
//                                     fontWeight: 'bold'
//                                 }}
//                             >
//                                 {msg.role === 'user'
//                                     ? 'You'
//                                     : msg.role === 'error'
//                                     ? 'Error'
//                                     : 'Assistant'}{' '}
//                                 - {msg.timestamp}
//                             </div>
//                             <div style={{ whiteSpace: 'pre-wrap' }}>
//                                 {msg.content}
//                             </div>
//                         </div>
//                     ))
//                 )}
//             </div>

//             {/* Input Section */}
//             <div style={{ display: 'flex', gap: '10px' }}>
//                 <textarea
//                     value={message}
//                     onChange={(e) => setMessage(e.target.value)}
//                     onKeyPress={handleKeyPress}
//                     placeholder='Type your message here... (Press Enter to send)'
//                     style={{
//                         flex: 1,
//                         padding: '10px',
//                         border: '1px solid #ddd',
//                         borderRadius: '4px',
//                         resize: 'vertical',
//                         minHeight: '60px',
//                         fontSize: '14px'
//                     }}
//                     disabled={loading}
//                 />
//                 <button
//                     onClick={sendMessage}
//                     disabled={loading || !message.trim()}
//                     style={{
//                         padding: '10px 20px',
//                         backgroundColor: loading ? '#ccc' : '#28a745',
//                         color: 'white',
//                         border: 'none',
//                         borderRadius: '4px',
//                         cursor: loading ? 'not-allowed' : 'pointer',
//                         fontSize: '14px',
//                         minWidth: '80px'
//                     }}
//                 >
//                     {loading ? 'Sending...' : 'Send'}
//                 </button>
//             </div>

//             {/* Instructions */}
//             <div
//                 style={{
//                     marginTop: '20px',
//                     padding: '15px',
//                     backgroundColor: '#f8f9fa',
//                     borderRadius: '4px',
//                     fontSize: '14px'
//                 }}
//             >
//                 <h4>Instructions:</h4>
//                 <ul>
//                     <li>Type your question in the text area above</li>
//                     <li>Click "Send" or press Enter to submit</li>
//                     <li>
//                         The chatbot will search your document and provide
//                         relevant answers
//                     </li>
//                     <li>Use "Check Health" to verify the service is running</li>
//                     <li>Use "Clear Chat" to start a fresh conversation</li>
//                 </ul>
//                 <p>
//                     <strong>API Endpoints:</strong>
//                 </p>
//                 <ul>
//                     <li>Chat: POST {API_BASE_URL}/chat/</li>
//                     <li>Health: GET {API_BASE_URL}/health/</li>
//                     <li>History: GET {API_BASE_URL}/history/</li>
//                 </ul>
//             </div>
//         </div>
//     );
// };

// Modified React Chatbot component to handle streaming
// Changes:
// - Uses fetch with response.body.getReader() to read chunks
// - Parses SSE 'data:' events
// - Appends chunks incrementally to a pending assistant message
// - Handles [DONE] to stop, and errors
// - Shows 'Thinking...' while streaming starts

import { useRef, useState } from 'react';

export const Chatbot = () => {
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const API_BASE_URL = 'http://localhost:8000/api/chatbot'; // Adjust this to your Django server URL
    const assistantMessageRef = useRef('');

    const sendMessage = async () => {
        if (!message.trim()) {
            setError('Please enter a message');
            return;
        }

        setLoading(true);
        setError('');

        // Add user message to chat
        const userMessage = {
            role: 'user',
            content: message,
            timestamp: new Date().toLocaleTimeString()
        };
        setMessages((prev) => [...prev, userMessage]);

        // Start a pending assistant message
        const pendingAiMessage = {
            role: 'assistant',
            content: '',
            timestamp: new Date().toLocaleTimeString()
        };
        setMessages((prev) => [...prev, pendingAiMessage]);

        assistantMessageRef.current = '';
        let response;
        try {
            response = await fetch(`${API_BASE_URL}/chat/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message
                })
            });

            if (!response.ok) {
                const error = await response.json()
                throw new Error(`${error.detail}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = ''; // Buffer for partial lines

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });

                // Process complete lines (SSE events are \n\n separated)
                let lines;
                while ((lines = buffer.split('\n\n')).length > 1) {
                    const event = lines.shift().trim();
                    buffer = lines.join('\n\n'); // Remaining partial

                    // Parse 'data:' lines (ignore other event types for simplicity)
                    if (event.startsWith('data:')) {
                        const dataStr = event.slice(5).trim();
                        let data;
                        try {
                            data = JSON.parse(dataStr);
                        } catch (parseErr) {
                            console.error('Invalid JSON in SSE:', parseErr);
                            continue;
                        }

                        if (data.chunk === '[DONE]') {
                            // Streaming complete
                            break;
                        } else if (data.error) {
                            // Handle error chunk
                            setError(data.error);
                            setMessages((prev) => {
                                const updated = [...prev];
                                const last = updated[updated.length - 1];
                                last.content += `\nError: ${data.error}`;
                                last.role = 'error';
                                return updated;
                            });
                            break;
                        } else if (data.chunk) {
                            assistantMessageRef.current += data.chunk;
                            
                            setMessages((prev) => {
                                const updated = [...prev];
                                const last = { ...updated[updated.length - 1] }; // copy
                                last.content = assistantMessageRef.current;
                                updated[updated.length - 1] = last;
                                return updated;
                            });
                        }
                    }
                }
            }
        } catch (error) {
            const errorMsg = error.message;
            
            setError(errorMsg);
            setMessages((prev) => {
                const updated = [...prev];
                const last = { ...updated[updated.length - 1] }; // copy
                last.content = `\n${errorMsg}`;
                updated[updated.length - 1] = last;
                return updated;
            });
        }

        setMessage('');
        setLoading(false);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    const clearChat = () => {
        setMessages([]);
        setError('');
    };

    return (
        <div
            style={{
                maxWidth: '800px',
                margin: '20px auto',
                padding: '20px',
                border: '1px solid #ddd',
                borderRadius: '8px',
                fontFamily: 'Arial, sans-serif'
            }}
        >
            <h2>Chatbot Test Interface</h2>

            {/* Health Check Button */}
            <div style={{ marginBottom: '20px' }}>
                <button
                    onClick={clearChat}
                    style={{
                        padding: '8px 16px',
                        backgroundColor: '#dc3545',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer'
                    }}
                >
                    Clear Chat
                </button>
            </div>

            {/* Error Display */}
            {error && (
                <div
                    style={{
                        backgroundColor: '#f8d7da',
                        color: '#721c24',
                        padding: '10px',
                        borderRadius: '4px',
                        marginBottom: '20px',
                        border: '1px solid #f5c6cb'
                    }}
                >
                    {error}
                </div>
            )}

            {/* Chat Messages */}
            <div
                style={{
                    height: '400px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    padding: '10px',
                    overflowY: 'auto',
                    marginBottom: '20px',
                    backgroundColor: '#f8f9fa'
                }}
            >
                {messages.length === 0 ? (
                    <p style={{ color: '#6c757d', fontStyle: 'italic' }}>
                        No messages yet. Start a conversation!
                    </p>
                ) : (
                    messages.map((msg, index) => (
                        <div
                            key={index}
                            style={{
                                marginBottom: '10px',
                                padding: '8px',
                                borderRadius: '4px',
                                backgroundColor:
                                    msg.role === 'user'
                                        ? '#e3f2fd'
                                        : msg.role === 'error'
                                        ? '#ffebee'
                                        : '#f3e5f5',
                                borderLeft: `4px solid ${
                                    msg.role === 'user'
                                        ? '#2196f3'
                                        : msg.role === 'error'
                                        ? '#f44336'
                                        : '#9c27b0'
                                }`
                            }}
                        >
                            <div
                                style={{
                                    fontSize: '12px',
                                    color: '#666',
                                    marginBottom: '4px',
                                    fontWeight: 'bold'
                                }}
                            >
                                {msg.role === 'user'
                                    ? 'You'
                                    : msg.role === 'error'
                                    ? 'Error'
                                    : 'Assistant'}{' '}
                                - {msg.timestamp}
                            </div>
                            <div style={{ whiteSpace: 'pre-wrap' }}>
                                {msg.content ||
                                    (loading && msg.role === 'assistant'
                                        ? 'Thinking...'
                                        : '')}
                            </div>
                        </div>
                    ))
                )}
            </div>

            {/* Input Section */}
            <div style={{ display: 'flex', gap: '10px' }}>
                <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder='Type your message here... (Press Enter to send)'
                    style={{
                        flex: 1,
                        padding: '10px',
                        border: '1px solid #ddd',
                        borderRadius: '4px',
                        resize: 'vertical',
                        minHeight: '60px',
                        fontSize: '14px'
                    }}
                    disabled={loading}
                />
                <button
                    onClick={sendMessage}
                    disabled={loading || !message.trim()}
                    style={{
                        padding: '10px 20px',
                        backgroundColor: loading ? '#ccc' : '#28a745',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: loading ? 'not-allowed' : 'pointer',
                        fontSize: '14px',
                        minWidth: '80px'
                    }}
                >
                    {loading ? 'Sending...' : 'Send'}
                </button>
            </div>

            {/* Instructions */}
            <div
                style={{
                    marginTop: '20px',
                    padding: '15px',
                    backgroundColor: '#f8f9fa',
                    borderRadius: '4px',
                    fontSize: '14px'
                }}
            >
                <h4>Instructions:</h4>
                <ul>
                    <li>Type your question in the text area above</li>
                    <li>Click "Send" or press Enter to submit</li>
                    <li>
                        The chatbot will search your document and provide
                        relevant answers
                    </li>
                    <li>Use "Check Health" to verify the service is running</li>
                    <li>Use "Clear Chat" to start a fresh conversation</li>
                </ul>
                <p>
                    <strong>API Endpoints:</strong>
                </p>
                <ul>
                    <li>Chat: POST {API_BASE_URL}/chat/</li>
                    <li>History: GET {API_BASE_URL}/history/</li>
                </ul>
            </div>
        </div>
    );
};
