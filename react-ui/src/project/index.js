import React, { useState, useEffect } from "react";
import { Button, FloatingLabel, Form, Stack, Image, Dropdown, InputGroup, Spinner } from "react-bootstrap";
import { useLocation } from "react-router-dom";
import CustomModal from "../modal";
import axios from "axios";
import Cleveland from "./Cleveland.png"
import Graph from "../graph";

const Project = () => {
    const location = useLocation();
    const [auth, setAuth] = useState("");
    const [project, setProject] = useState("");
    const [error, setError] = useState(false);
    const [data, setData] = useState(null);
    const [selectedValue, setSelectedValue] = useState(null);
    const [metric, setMetric] = useState(null);
    const [spinnerFlag, setSpinnerFlag] = useState(false);

    const handleSelect = (eventKey) => {
        setSelectedValue(eventKey);
        if (eventKey === "Lead Time") {
            setMetric("LeadTime");
        }
        else if (eventKey === "Cycle Time") {
            setMetric("CycleTime");
        }
        else if (eventKey === "Burndown Chart") {
            setMetric("Burndown");
        }
    };

    useEffect(() => {
        setAuth(location?.state?.token);
    }, [location]);

    const handleSubmit = (event) => {
        event.preventDefault();

        setSpinnerFlag(true);

        axios({
            method: "post",
            url: `http://localhost:8000/metric/${metric}`,
            data: {
                projectslug: project
            },
            headers: {
                "Content-Type": "application/json",
                "token": auth
            }
        })
        .then(res => {
            setData(res.data);
            console.log(data);
            setSpinnerFlag(false);
            setError(false);
        })
        .catch(ex => {
            setError(true);
            setSpinnerFlag(false);
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
        <div style={{ height: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <div style={{ height: '80%', width: '90%', maxHeight: '90vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <Stack gap={4} className="col-md-5 mx-auto">
                    <div className="d-flex align-items-center justify-content-center vh-100 backgroundWhite">

                        <br />
                        <Form style={{ width: "100%" }}>
                            <Image src={Cleveland} className='col-sm-2 offset-sm-5' /><br /><br /><br /><br />
                            <div className="mb-3 col-sm-6 offset-sm-2">Welcome to our project! <br /><br />Please input your Project Slug 
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
                                            <Dropdown.Item eventKey="Burndown Chart">Burndown Chart</Dropdown.Item>
                                            <Dropdown.Item eventKey="Lead Time">Lead Time</Dropdown.Item>
                                            <Dropdown.Item eventKey="Cycle Time">Cycle Time</Dropdown.Item>
                                        </Dropdown.Menu>
                                    </Dropdown>
                                </InputGroup>
                            </div><br/> 

                            <Button variant="info" type="submit" className="submitButton backgroundButton" onClick={handleSubmit}>
                                Submit
                            </Button>

                            <br />

                            {error ? (
                                <p className="errorMessage">Unable to fetch project detail</p>
                            ) : null}

                            {spinnerFlag ? <Spinner variant="primary" animation="border" style={{ justifyContent: "center", alignItems: "center", display:"flex", marginLeft: "49%" }} /> : null}
                        </Form>
                    </div>

                    {data?.metric === "LEAD" ? (
                        <div>
                            <br />
                            <h3 className="projectName">{data.projectInfo.name}</h3>
                            <Graph apiData={data.leadTime.storiesLeadTime.userStory} avg={data.leadTime.storiesLeadTime.avgLeadTime} chartFor={"User Story"} title={`User Story ${selectedValue}`} />
                            <br />
                            <Graph apiData={data.leadTime.tasksLeadTime.task} avg={data.leadTime.tasksLeadTime.avgLeadTime} chartFor={"Task"} title={`Task ${selectedValue}`} />
                        </div>
                    ) : null}
                    {data?.metric === "CYCLE" ? (
                        <div>
                            <br />
                            <h3 className="projectName">{data.projectInfo.name}</h3>
                            <Graph apiData={data.cycleTime.storyCycleTime.story} avg={data.cycleTime.storyCycleTime.avgCycleTime} chartFor={"User Story"} title={`User Story ${selectedValue}`} />
                            <br />
                            <Graph apiData={data.cycleTime.taskCycleTime.task} avg={data.cycleTime.taskCycleTime.avgCycleTime} chartFor={"Task"} title={`Task ${selectedValue}`} />
                        </div>
                    ) : null}
                </Stack>
            </div>
        </div>
    );
}

export default Project;
