import { useState } from "react";
import { Button, Form } from "react-bootstrap";

const DateSelector = ({ onDateSubmit }) => {
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');

    // Temporary code for submit button
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Selected Start Date: ", startDate, "Selected End Date: ", endDate);
        onDateSubmit(startDate, endDate);
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
                </div>
                <div style={{ display: 'flex', justifyContent: 'center' }}>
                    <Button variant="primary" type="submit" className="submitButton backgroundButton">Submit</Button>
                </div>
            </Form>
        </div>
    );
};


export default DateSelector;