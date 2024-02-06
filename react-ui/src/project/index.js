import React from "react";
import { Button, FloatingLabel, Form } from "react-bootstrap";
import { useLocation } from "react-router-dom";

const Project = ({ auth }) => {
    let location = useLocation();
    console.log(auth);
    console.log(location);

    return (
        <Form>
            <FloatingLabel
                controlId="floatingUsername"
                label="Project Slug"
                className="mb-3"
            >
                <Form.Control type="text" placeholder="Enter Project Slug" />
            </FloatingLabel>

            <Button variant="primary" type="submit">
                Submit
            </Button>
        </Form>
    );
}

export default Project;