import React from 'react';
import './ProjectSelection.css';

function ProjectSelection() {
    return (
      <div className="projectSelection">
        <header className="projectSelection-header">
          <input
            type="text"
            className="projectSelection-input"
            placeholder="Enter Project slug"
          />
          <button className="projectSelection-button">
            Submit
          </button>
        </header>
      </div>
    );
  }
  
  export default ProjectSelection;