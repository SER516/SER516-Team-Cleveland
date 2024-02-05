import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form';
import React from 'react';
import './ProjectSlug.css';

function ProjectSlug() {
    return (
      <div className='projectSlugContainer'>
        <Form>
          <Form.Control as="textarea" className="customTextarea" placeholder="Enter Project Slug" />
          <Button variant="info" className="customButton">Submit</Button>
        </Form>
      </div>
    );
  }
  
  export default ProjectSlug;