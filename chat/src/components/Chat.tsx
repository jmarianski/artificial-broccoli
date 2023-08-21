import { useState } from 'react';
import axios from 'axios';

function Chat() {
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState('');

    const sendMessage = async () => {
        try {
            const response = await axios.post(
                'http://localhost:5000/chat',
                { message }
            );
            setResponse(response.data.response);
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    return (
        <div>
            <h1>Chat with Flask API</h1>
            <div>
                <textarea
                    rows={4}
                    cols={50}
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                ></textarea>
            </div>
            <div>
                <button onClick={sendMessage}>Send</button>
            </div>
            <div>
                <h2>Response:</h2>
                <p>{response}</p>
            </div>
        </div>
    );
}

export default Chat;
