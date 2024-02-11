import React, { useState, useEffect } from "react";
import { Button, FloatingLabel, Form, Stack, Image, Dropdown, InputGroup } from "react-bootstrap";
import { useLocation } from "react-router-dom";
import CustomModal from "../modal";
import axios from "axios";
import Cleveland from "./Cleveland.png"

const Project = () => {
    const location = useLocation();
    const [auth, setAuth] = useState("");
    const [project, setProject] = useState("");
    const [error, setError] = useState(false);
    const [data, setData] = useState(null);
    const [selectedValue, setSelectedValue] = useState(null);

    const handleSelect = (eventKey) => {
        setSelectedValue(eventKey);
    };

    useEffect(() => {
        setAuth(location?.state?.token);
    }, [location]);

    const handleSubmit = (event) => {
        event.preventDefault();

        axios({
            method: "post",
            url: "http://localhost:8000/metric/LeadTime",
            data: {
                projectslug: project
            },
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "http://localhost:3000/project",
                "token": auth
            }
        })
        .then(res => {
            setData(res.data);
            console.log(data);
            setError(false);
        })
        .catch(ex => {
            setError(true);
        });
    }

    const handleProjectSlugField = (event) => {
        event.preventDefault();
        setProject(event.target.value);
        setError(false);
    }

    if (!location?.state) {
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
                                        <Form.Control type="text" placeholder="Project Slug" onChange={handleProjectSlugField} />
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

                            <Button variant="info" type="submit" className="submitButton backgroundButton" onClick={handleSubmit}>
                                Submit
                            </Button>

                            {error ? (
                                <p className="errorMessage">Unable to fetch project detail</p>
                            ) : null}

                            {data?.projectInfo?.name ? (
                                <h6 className="projectName">{data.projectInfo.name}</h6>
                            ) : null}
                        </Form>
                    </div>
                </Stack>
            </div>
        </div>
    );
}

export default Project;