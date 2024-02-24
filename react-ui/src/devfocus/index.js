import { useState } from "react";
import { Button, Dropdown, FloatingLabel, Form, InputGroup } from "react-bootstrap";

const DateSelector = ({ onDateSubmit }) => {
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [selectedValue, setSelectedValue] = useState(null);
    const [threshold, setThreshold] = useState(null);

    const handleSelect = (eventKey) => {
        console.log(eventKey);
        setSelectedValue(eventKey);
    };

    // Temporary code for submit button
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Selected Start Date: ", startDate, "Selected End Date: ", endDate, threshold);
        onDateSubmit(startDate, endDate);
    };

    const handleThresholdChange = (event) => {
        event.preventDefault();
        setThreshold(event.target.value);
    };
    
    return (
        <div>
            <Form onSubmit={handleSubmit}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '20px' }}>
                    <div style={{ display: 'flex', justifyContent: 'center', gap: '20px'}}>
                        <Form.Group controlId="dateFrom" style={{ width: '15%' }}>
                            <Form.Label>From</Form.Label>
                            <Form.Control type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
                        </Form.Group>
                        <Form.Group controlId="dateTo" style={{ width: '15%' }}>
                            <Form.Label>To</Form.Label>
                            <Form.Control type="date" value={endDate} onChange={e => setEndDate(e.target.value)} />
                        </Form.Group>
                    </div>
                    <div className="d-flex justify-content-center col-sm-8 offset-sm-2">
                        <InputGroup>
                            <FloatingLabel
                                controlId="threshold"
                                label="Threshold"
                            >
                                <Form.Control type="text" placeholder="Threshold" onChange={handleThresholdChange} />
                            </FloatingLabel>
                            <Dropdown onSelect={handleSelect}>
                                <Dropdown.Toggle variant="outline-secondary" className="backgroundButton">
                                    {selectedValue ? selectedValue : 'Select Member'}
                                </Dropdown.Toggle>
                                <Dropdown.Menu>
                                    <Dropdown.Item eventKey="Member 1">Member 1</Dropdown.Item>
                                    <Dropdown.Item eventKey="Member 2">Member 2</Dropdown.Item>
                                    <Dropdown.Item eventKey="Member 3">Member 3</Dropdown.Item>
                                </Dropdown.Menu>
                            </Dropdown>
                        </InputGroup>
                    </div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'center' }}>
                    <Button variant="primary" type="submit" className="submitButton backgroundButton">Submit</Button>
                </div>
            </Form>
        </div>
    );
};
      

export default DateSelector;
