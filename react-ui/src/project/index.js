import React, { useState } from "react";
import { Button, FloatingLabel, Form, Stack } from "react-bootstrap";
import { useLocation, useNavigate } from "react-router-dom";  // Add useNavigate for test
import CustomModal from "../modal";

const Project = ({ auth }) => {
    let location = useLocation();
    let navigate = useNavigate(); // Add navigate for test
    const [clicked, setClicked] = useState(false);

    const handleSubmit = () => {
        console.log("handle user");
        setClicked(true);
    }

    // Add for test
    const handleNavigateToGraph = () => {
        navigate('/graph');
    };

    // if (!location?.state && !clicked) {
    //     return (
    //         <CustomModal message="User not authenticated" headerTitle="Invalid Authentication!" showModal={true} />
    //     );
    // }

    return (
        <Stack gap={4} className="col-md-5 mx-auto">
            <div className="d-flex align-items-center justify-content-center vh-100">
                <Form style={{ width: "100%" }}>
                    <FloatingLabel
                        controlId="formProjectSlug"
                        label="Project Slug"
                        className="mb-3 col-sm-8 offset-sm-2"
                    >
                        <Form.Control type="text" placeholder="Project Slug" />
                    </FloatingLabel>

                    <Button variant="info" type="submit" className="submitButton" onClick={() => handleSubmit()}>
                        Submit
                    </Button>

                    {/* Add for test*/}
                    <Button variant="primary" className="mt-2" onClick={handleNavigateToGraph}>
                        Graph
                    </Button>
                </Form>
            </div>
        </Stack>
    );
}

export default Project;