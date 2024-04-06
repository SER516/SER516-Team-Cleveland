import React, { useState, useEffect } from "react";
import { Button, FloatingLabel, Form, Stack, Image, Dropdown, InputGroup, Spinner, Nav, Navbar, Accordion, ListGroup } from "react-bootstrap";
import { Link, useLocation } from "react-router-dom";
import CustomModal from "../modal";
import axios from "axios";
import Name from "./Name.png";
import Graph from "../graph";
import SprintDetail from "../sprint";
import DateSelector from '../devfocus';
import DateSelectorCruft from '../cruft';


const Project = () => {
    const location = useLocation();
    const [auth, setAuth] = useState("");
    const [project, setProject] = useState("");
    const [error, setError] = useState(false);
    const [data, setData] = useState(null);
    const [selectedValue, setSelectedValue] = useState(null);
    const [metric, setMetric] = useState(null);
    const [spinnerFlag, setSpinnerFlag] = useState(false);
    const [isBurndown, setIsBurndown] = useState(false);
    const [isLeadTime, setIsLeadTime] = useState(false);
    const [isCycleTime, setIsCycleTime] = useState(false);
    const [isDevFocus, setIsDevFocus] = useState(false);
    const [isCruft, setIsCruft] = useState(false);
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');

    const handleSelect = (eventKey) => {
        setSelectedValue(eventKey);
        if (eventKey === "Lead Time") {
            setMetric("8001/metric/LeadTime");
            setIsBurndown(false);
            setIsCycleTime(false);
            setIsDevFocus(false);
            setIsCruft(false);
            setIsLeadTime(true);
        }
        else if (eventKey === "Cycle Time") {
            setMetric("8000/metric/CycleTime");
            setIsBurndown(false);
            setIsCycleTime(true);
            setIsDevFocus(false);
            setIsCruft(false);
            setIsLeadTime(false);
        }
        else if (eventKey === "Burndown Chart") {
            setMetric("8000/Sprints");
            setIsCycleTime(false);
            setIsDevFocus(false);
            setIsLeadTime(false);
            setIsCruft(false);
        }
        else if (eventKey === "Dev Focus") {
            setIsBurndown(false);
            setIsLeadTime(false);
            setIsCycleTime(false);
            setIsCruft(false);
            setMetric("8000/Project");
        }
        else if (eventKey === "Cruft") {
            setMetric("8000/Sprints");
            setIsBurndown(false);
            setIsCycleTime(false);
            setIsDevFocus(false);
            setIsLeadTime(false);
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
            url: `http://localhost:${metric}`,
            data: {
                projectslug: project,
                from_date: startDate,
                to_date: endDate
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
                selectedValue === "Dev Focus" ? setIsDevFocus(true) : setIsDevFocus(false);
                selectedValue === "Burndown Chart" ? setIsBurndown(true) : setIsBurndown(false);
                selectedValue === "Cruft" ? setIsCruft(true) : setIsCruft(false);
            })
            .catch(ex => {
                setError(true);
                setSpinnerFlag(false);
                setIsBurndown(false);
                setIsDevFocus(false);
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
        <div className="backgroundOrange fontUniform" style={{ display: "flex", minWidth: "100vh", minHeight: "100vh", justifyContent: 'center', alignItems: 'center' }}>
            <div className="backgroundWhite" style={{ minWidth: "95%", minHeight: "95%", width: "95%", height: "95%", maxHeight: "95vh", overflow: "auto", borderRadius: "15px" }}>
                <div style={{ position: "fixed", width: "25vh" }}>
                    <div className="backgroundWhite" style={{ minHeight: "10vh", borderTopLeftRadius: "15px", overflow: "hidden", borderRight: "1px solid #750E21"  }}>
                        <Image src={Name} style={{ width: "100%", height: "100%", marginTop: "10px" }} />
                    </div>
                    <div className="backgroundWhite" style={{ minHeight: "85vh", borderBottomLeftRadius: "15px", borderTop: "1px solid #750E21", borderRight: "1px solid #750E21" }}>
                        <Nav defaultActiveKey="/home" className="flex-column">
                            <ListGroup defaultActiveKey={['0']} alwaysOpen>
                                <ListGroup.Item as="li"><a href="/">Home</a></ListGroup.Item>
                            </ListGroup>
                            <ListGroup defaultActiveKey={['0']} alwaysOpen>
                                <ListGroup.Item  as={Link} to="/project" state={{token: auth}}><b>Dashboard</b></ListGroup.Item>
                            </ListGroup>
                            <Accordion defaultActiveKey={['0']} alwaysOpen>
                                <Accordion.Item eventKey="0">
                                    <ListGroup defaultActiveKey={['0']} alwaysOpen>
                                        <ListGroup.Item  as={Link} to="/metricwiki" state={{token: auth}}>Metric Wiki</ListGroup.Item>
                                    </ListGroup>
                                    <Accordion.Body style={{ paddingTop: "5px" }}>
                                        <Nav.Link style={{ borderBottom: "1px solid #750E21" }} as={Link} to="/metricwiki" state={{token: auth}}>Lead Time</Nav.Link>
                                        <Nav.Link style={{ borderBottom: "1px solid #750E21" }} as={Link} to="/metricwiki" state={{token: auth}}>Cycle Time</Nav.Link>
                                        <Nav.Link style={{ borderBottom: "1px solid #750E21" }} as={Link} to="/metricwiki" state={{token: auth}}>Burndown Chart</Nav.Link>
                                        <Nav.Link style={{ borderBottom: "1px solid #750E21" }} as={Link} to="/metricwiki" state={{token: auth}}>Dev Focus</Nav.Link>
                                        <Nav.Link style={{ borderBottom: "1px solid #750E21" }} as={Link} to="/metricwiki" state={{token: auth}}>Cruft</Nav.Link>
                                    </Accordion.Body>
                                </Accordion.Item>
                            </Accordion>
                            <ListGroup defaultActiveKey={['0']} alwaysOpen>
                                <ListGroup.Item as={Link} to="/aboutus" state={{token: auth}}>About Us</ListGroup.Item>
                            </ListGroup>
                        </Nav>
                    </div>
                </div>
                <div style={{ marginLeft: "25vh" }}>
                    <div className="backgroundLightOrange" style={{ minHeight: "10vh", borderBottom: "1px solid #750E21" }}>
                        <Navbar>
                            <div style={{ marginLeft: "40px", marginTop: "10px", fontFamily: "Cascadia Mono SemiLight" }}><h2><b>DASHBOARD</b></h2></div>
                            <div className="ms-auto" style={{ marginRight: "45px", marginTop: "5px" }}>
                                <a href="/" style={{ fontSize: "20px" }}><u>Logout</u></a>
                            </div>
                        </Navbar>
                    </div>
                    <div className="backgroundWhite" style={{ minHeight: "85vh" }}>
                        <Stack>
                            <div>
                                <br />
                                <Form>
                                    <div style={{padding: "45px"}}>Welcome to Team Cleveland's SER516 Project! Metrics are important 
                                    for any developer team to characterize, evaluate, predict and improve. This dashboard will help you
                                    evaluate your sprints and projects using different metrics. Read up more about the metrics  
                                    <a href="/metricwiki"> here</a>.
                                     <br /><br />To utilize the dashboard, kindly input the project slug below and other details 
                                     as required. 
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
                                                    <Dropdown.Item eventKey="Cycle Time">Cycle Time</Dropdown.Item>
                                                    <Dropdown.Item eventKey="Burndown Chart">Burndown Chart</Dropdown.Item>
                                                    <Dropdown.Item eventKey="Dev Focus">Dev Focus</Dropdown.Item>
                                                    <Dropdown.Item eventKey="Cruft">Cruft</Dropdown.Item>
                                                </Dropdown.Menu>
                                            </Dropdown>
                                        </InputGroup>
                                    </div><br />

                            {isLeadTime || isCycleTime ? (
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '20px' }}>
                                    <div style={{ display: 'flex', justifyContent: 'center', gap: '20px' }}>
                                        <Form.Group controlId="dateFrom" style={{ width: '15%' }}>
                                            <Form.Label>From</Form.Label>
                                            <Form.Control type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
                                        </Form.Group>
                                        <Form.Group controlId="dateTo" style={{ width: '15%' }}>
                                            <Form.Label>To</Form.Label>
                                            <Form.Control type="date" value={endDate} onChange={e => setEndDate(e.target.value)} />
                                        </Form.Group>
                                    </div>
                                </div>
                            ) : null}

                                    <Button variant="info" type="submit" className="submitButton backgroundButton" onClick={handleSubmit}>
                                        Submit
                                    </Button>

                                    <br />

                                    {error ? (
                                        <p className="errorMessage">Unable to fetch project detail</p>
                                    ) : null}

                                    {spinnerFlag ? <Spinner variant="primary" animation="border" style={{ justifyContent: "center", alignItems: "center", display: "flex", marginLeft: "49%" }} /> : null}
                                </Form>
                            </div>

                            {data?.metric === "LEAD" && isLeadTime ? (
                                <div>
                                    <br />
                                    <h3 className="projectName">{data.projectInfo.name}</h3>
                                    <Graph type="Lead Time" apiData={data.leadTime.storiesLeadTime.userStory} avg={data.leadTime.storiesLeadTime.avgLeadTime} chartFor={"User Story"} title={`User Story ${selectedValue}`} />
                                    <br />
                                    <Graph type="Lead Time" apiData={data.leadTime.tasksLeadTime.task} avg={data.leadTime.tasksLeadTime.avgLeadTime} chartFor={"Task"} title={`Task ${selectedValue}`} />
                                </div>
                            ) : null}
                            {data?.metric === "CYCLE" && isCycleTime ? (
                                <div>
                                    <br />
                                    <h3 className="projectName">{data.projectInfo.name}</h3>
                                    <Graph type="Cycle Time" apiData={data.cycleTime.storyCycleTime.story} avg={data.cycleTime.storyCycleTime.avgCycleTime} chartFor={"User Story"} title={`User Story ${selectedValue}`} />
                                    <br />
                                    <Graph type="Cycle Time" apiData={data.cycleTime.taskCycleTime.task} avg={data.cycleTime.taskCycleTime.avgCycleTime} chartFor={"Task"} title={`Task ${selectedValue}`} />
                                </div>
                            ) : null}
                            {selectedValue === "Burndown Chart" && isBurndown ? (
                                <SprintDetail sprintDetails={data.sprints} attributes={data.custom_attributes} token={auth} projectName={data.name} />
                            ) : null}
                            {selectedValue === "Dev Focus" && isDevFocus ? (
                                <DateSelector memberDetails={data.members} token={auth} projectId={data.id} onDateSubmit={(startDate, endDate) => {
                                    console.log("Date range submitted:", startDate, "to", endDate);
                                }} />
                            ) : null}
                            {selectedValue === "Cruft" && isCruft ? (
                                <DateSelectorCruft attributes={data.custom_attributes} token={auth} projectId={data.id} onDateSubmit={(startDate, endDate) => {
                                    console.log("Date range submitted:", startDate, "to", endDate);
                                }} />
                            ) : null}
                            <br />
                        </Stack>
                    </div>
                </div>
            </div>
        </div >
    );
}

export default Project;
