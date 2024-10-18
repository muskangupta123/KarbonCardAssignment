// ResultsPage.js
import React from 'react';
import { useLocation } from 'react-router-dom';

const ResultsPage = () => {
    const location = useLocation();
    const { state } = location;

    // Check if the state and summary exist
    if (!state || !state.results) {
        return <p>No data available.</p>; // Handle the missing data gracefully
    }

    const results = state.results; // Assuming results is an array

    return (
        <div>
            <h1>Results</h1>
            {results.length > 0 ? (
                results.map((item, index) => (
                    <div key={index}>{item}</div> // Adjust based on your data structure
                ))
            ) : (
                <p>No results found.</p>
            )}
        </div>
    );
};

export default ResultsPage;
