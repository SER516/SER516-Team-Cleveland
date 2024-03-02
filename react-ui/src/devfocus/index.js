import { useState } from "react";
import { Button, Dropdown, FloatingLabel, Form, InputGroup } from "react-bootstrap";

const DateSelector = ({ onDateSubmit, memberDetails }) => {
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [selectedValue, setSelectedValue] = useState(null);
    const [threshold, setThreshold] = useState(null);

    const handleSelect = (eventKey) => {
        const splitEventKey = eventKey.split(',');
        setSelectedValue(splitEventKey[1]);
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
                                    {
                                        memberDetails.map((item) => <Dropdown.Item key={item.id} eventKey={[item.id,
                                        item.name]}>{item.name}</Dropdown.Item>)
                                    }
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
