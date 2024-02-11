import React, { useState } from "react";
import { Button, FloatingLabel, Form, Stack, Image, Dropdown, InputGroup } from "react-bootstrap";
import { useLocation } from "react-router-dom";
import CustomModal from "../modal";
import Cleveland from "./Cleveland.png"

const Project = ({ auth }) => {
    const [selectedValue, setSelectedValue] = useState(null);

    const handleSelect = (eventKey) => {
        setSelectedValue(eventKey);
    };
    let location = useLocation();
    const [clicked, setClicked] = useState(false);

    const handleSubmit = () => {
        console.log("handle user");
        setClicked(true);
    }

    if (!location?.state && !clicked) {
        return (
            <CustomModal message="User not authenticated" headerTitle="Invalid Authentication!" showModal={true} />
        );
    }

    return (
        <div className='background' style={{ height: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <div style={{ height: '80%', width: '90%', maxHeight: '90vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <Stack gap={4} className="col-md-5 mx-auto">
                    <div className="d-flex align-items-center justify-content-center vh-100 backgroundWhite">

                        <br /><br /><br /><br />
                        <Form style={{ width: "100%" }}>
                            <Image src={Cleveland} className='col-sm-2 offset-sm-5' /><br /><br /><br /><br />
                            <div className="mb-3 col-sm-6 offset-sm-2">Welcome to our project! <br /><br />Please input your Project Slug link in the input box given below. The Project slug link
                                can be found on your Taiga account.
                                <br /></div>
                            <div className="d-flex justify-content-center col-sm-8 offset-sm-2">
                                <InputGroup>
                                    <FloatingLabel
                                        controlId="formProjectSlug"
                                        label="Project Slug"
                                    >
                                        <Form.Control type="text" placeholder="Project Slug" />
                                    </FloatingLabel>
                                    <Dropdown onSelect={handleSelect}>
                                        <Dropdown.Toggle variant="outline-secondary" className="backgroundButton">
                                            {selectedValue ? selectedValue : 'Select Metric'}
                                        </Dropdown.Toggle>
                                        <Dropdown.Menu>
                                            <Dropdown.Item eventKey="Lead Time">Lead Time</Dropdown.Item>
                                        </Dropdown.Menu>
                                    </Dropdown>
                                </InputGroup>
                            </div><br/>

                            <Button variant="info" type="submit" className="submitButton backgroundButton" onClick={() => handleSubmit()}>
                                Submit
                            </Button>
                        </Form>
                    </div>
                </Stack>
            </div>
        </div>
    );
}

export default Project;