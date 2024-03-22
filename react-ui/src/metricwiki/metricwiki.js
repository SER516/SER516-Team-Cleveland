import Name from "./Name.png";
import React, { useState, useEffect } from "react";
import { Image, ListGroup, Accordion, Nav, Navbar } from "react-bootstrap";
import { Link, useLocation } from "react-router-dom";

const MetricWiki = () => {

    const location = useLocation();
    const [auth, setAuth] = useState("");

    useEffect(() => {
        setAuth(location?.state?.token);
    }, [location]);

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
                                <ListGroup.Item as={Link} to="/project" state={{token: auth}}>Dashboard</ListGroup.Item>
                            </ListGroup>
                            <Accordion defaultActiveKey={['0']} alwaysOpen>
                                <Accordion.Item eventKey="0">
                                    <ListGroup defaultActiveKey={['0']} alwaysOpen>
                                        <ListGroup.Item as={Link} to="/metricwiki" state={{token: auth}}><b>Metric Wiki</b></ListGroup.Item>
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
                            <div style={{ marginLeft: "40px", marginTop: "10px", fontFamily: "Cascadia Mono SemiLight"}}><h2><b>DASHBOARD</b></h2></div>
                            <div className="ms-auto" style={{ marginRight: "45px", marginTop: "5px" }}>
                                <a href="/" style={{ fontSize: "20px" }}><u>Logout</u></a>
                            </div>
                        </Navbar>
                    </div>
                    <div className="backgroundWhite" style={{ minHeight: "85vh", padding: "45px" }}>
                        <div id="LeadTimeInfo">
                            <h4><u>Lead Time</u></h4>
                            Lead Time is defined as the time duration from the creation of the process to its completion. Lead Time 
                            is an important metric because it helps a developer team estimate the time required to deliver a 
                            requirement defined by the customer.<br/>
                            <br/>
                            <b>Input:</b> <br/>
                            The Project Slug, and the Date Range between which the Lead Time is to be measured. <br/><br/>
                            <b>Output:</b> <br/>
                            (i) A Scatter Graph representing the Lead Times of user stories within the specified date range. <br/>
                            (ii) A Scatter Graph representing the Lead Times of individual tasks within the specified date range. <br/>
                            <br/><br/>
                        </div>
                        <div id="CycleTimeInfo">
                            <h4><u>Cycle Time</u></h4>
                            Cycle Time is defined as the time duration from the start of the process to its completion. Cycle Time is 
                            an important metric because it helps a developer team estimate the time required to work on a product.<br/>
                            <br/>
                            <b>Input:</b> <br/>
                            The Project Slug, and the Date Range between which the Cycle Time is to be measured. <br/><br/>
                            <b>Output:</b> <br/>
                            (i) A Scatter Graph representing the Lead Times of user stories within the specified date range. <br/>
                            (ii) A Scatter Graph representing the Lead Times of individual tasks within the specified date range. <br/>
                            <br/><br/>
                        </div>
                        <div id="BurndownChartInfo">
                            <h4><u>Burndown Chart</u></h4>
                            Burndown Chart is used to visualize the progress of a team across the sprint. It includes an
                            expected line that helps us plot expectations vs progress. Burndown charts are a great indicator for a 
                            developer team to measure their cadence over the sprint and measure progress during the sprint, as opposed 
                            to calculating the metrics at the end of the sprint. <br/>
                            <br/>
                            <b>Input:</b> <br/>
                            The Project Slug, and the Sprint for which the Burndown Chart is to be calculated for <br/><br/>
                            <b>Output:</b> <br/>
                            (i) An Area Chart for the Total Story Points (story points of completed user stories only). <br/>
                            (ii) An Area Chart for the Partial Story Points (story points of completed tasks). <br/>
                            (iii) An Area Chart for the Business Value (for Business Value of completed user stories). <br/>
                            (iv) An Area Chart combining all of the three metrics taken as a percentage of their total. <br/>
                            <br/><br/>
                        </div>
                        <div id="DevFocusInfo">
                            <h4><u>Dev Focus</u></h4>
                            Dev Focus is used to track the WIP for every member. The best practices classify Task Switching
                            or Multitasking as a waste and recommend developers to work on no more than two tasks at a time. Dev Focus
                            helps us track the users who are violating the threshold for the number of tasks one can take at a time. <br/>
                            <br/>
                            <b>Input:</b> <br/>
                            The Project Slug, the Date Range between which the Dev Focus is to be measured, and the threshold that is
                            considered a violation of the WIP for each user. <br/><br/>
                            <b>Output:</b> <br/>
                            (i) A Bar Chart representing the total number of violations per user within the specified date range. <br/>
                            (ii) A Bar Chart representing the violations per day within the specified date range. <br/>
                            <br/><br/>
                        </div>
                        <div id="CruftInfo">
                            <h4><u>Cruft</u></h4>
                            Cruft is used to measure the work of the sprint. A sprint contains issues and storyless tasks that aren't
                            formally noted by the other metrics but are work nevertheless, and need to be taken into consideration
                            when measuring the work completed by the developer team.<br/>
                            <br/>
                            <b>Input:</b> <br/>
                            The Project Slug, and the Date Range between which the Cruft is to be measured. <br/><br/>
                            <b>Output:</b> <br/>
                            (i) A Pie Chart visualizing the number of tasks that are issues, the ones with no business value and the 
                            issues.<br/>
                            (ii) A Pie Chart visualizing the story points of the tasks having business value vs the story points of
                            the tasks having no business value.
                            <br/><br/>
                        </div>
                    </div>
                </div>
            </div>
        </div >
    );
}

export default MetricWiki;
