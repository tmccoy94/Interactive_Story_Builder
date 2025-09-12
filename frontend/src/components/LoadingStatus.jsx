import React from 'react';

const LoadingStatus = ({theme}) => {
    return (
        <div className="loading-container">
            <h2>Generating Your {theme} Story</h2>
            <div className='loading-animation'>
                <div className='spinner'></div>
            </div>
            <p className='loading-info'>This may take a few moments. Please wait...</p>
        </div>
    );
};

export default LoadingStatus;