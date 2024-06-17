import React from 'react';
import { Circles } from 'react-loader-spinner';

const LoadingSpinner: React.FC = () => {
  return (
    <div className="loading-spinner">
      <Circles
        height="80"
        width="80"
        color="#4fa94d"
        ariaLabel="loading"
      />
    </div>
  );
};

export default LoadingSpinner;
