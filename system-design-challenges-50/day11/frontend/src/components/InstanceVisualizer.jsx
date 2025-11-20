import React from 'react';

const InstanceVisualizer = ({ instances }) => {
  const renderInstances = () => {
    return Array.from({ length: instances }, (_, i) => (
      <div key={i} className="instance">
        <div className="instance-icon">🖥️</div>
        <div className="instance-label">Instance {i + 1}</div>
      </div>
    ));
  };

  return (
    <div className="instance-visualizer">
      <h2>Instance Visualization</h2>
      <div className="instances-container">
        {renderInstances()}
      </div>
    </div>
  );
};

export default InstanceVisualizer;