import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
    const [sites, setSites] = useState([]);

    useEffect(() => {
        const fetchStatus = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/status');
                setSites(response.data);
            } catch (error) {
                console.error("Error fetching status:", error);
            }
        };

        fetchStatus();
        const interval = setInterval(fetchStatus, 30000); // Refresh every 30 seconds

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Site Status Dashboard</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {sites.map(site => (
                    <div key={site.url} className={`p-4 rounded-lg shadow-md ${site.status === 'Up' ? 'bg-green-100' : 'bg-red-100'}`}>
                        <h2 className="font-bold text-lg">{site.url}</h2>
                        <p>Status: <span className={`font-semibold ${site.status === 'Up' ? 'text-green-700' : 'text-red-700'}`}>{site.status}</span></p>
                        <p>HTTP Code: {site.status_code}</p>
                        <p>Response Time: {site.response_time ? `${(site.response_time * 1000).toFixed(2)} ms` : 'N/A'}</p>
                        <p>Last Checked: {site.checked_at ? new Date(site.checked_at).toLocaleString() : 'N/A'}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;
