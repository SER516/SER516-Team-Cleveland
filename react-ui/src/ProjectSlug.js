import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form';
import React from 'react';
{/*import './ProjectSlug.css';*/}


function ProjectSlug() {
    return (
      <div>
        <Form>
          <Form.Control as="textarea" />
          <Button variant="info">Submit</Button>
        </Form>
      </div>
    );
  }
  
  export default ProjectSlug;