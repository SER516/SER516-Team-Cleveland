import React from 'react';
import { Button, Form } from "react-bootstrap";
import './ProjectSlug.css';

function ProjectSlug() {
    return (
      <div className='projectSlugContainer'>
        <Form style={{ width: '100%' }}>
          <Form.Label>Enter Project Slug</Form.Label>
          <Form.Control as="textarea" className="customTextarea" placeholder="Enter Project Slug" />
          <Button variant="info" className="SubmitButton">Submit</Button>
        </Form>
      </div>
    );
  }
  
  export default ProjectSlug;