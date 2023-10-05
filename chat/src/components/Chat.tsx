import { useState } from 'react';
import axios from 'axios';

function Chat() {
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState('');
    const [context, setContext] = useState('');

    const handleKeyPress = (event: React.KeyboardEvent) => {
        if (event.key === 'Enter') {
            sendMessage();
            return true;
        }
    }

    const sendMessage = async () => {
        try {
            const messageToSend = message.trim();
            setMessage('');
            const response = await axios.post(
                'http://localhost:5000/chat',
                { message: messageToSend, context }
            );
            setResponse(response.data.response);
            setContext(response.data.context);
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    return (
        <div>
            <h1>Chat with Flask API</h1>
            <div>
                <input
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyPress}
                ></input>
            </div>
            <div>
                <button onClick={sendMessage}>Send</button>
            </div>
            <div>
                <h2>Response:</h2>
                <p>{response}</p>
                <h3>Context:</h3>
                <p>{context}</p>
            </div>
        </div>
    );
}

export default Chat;
