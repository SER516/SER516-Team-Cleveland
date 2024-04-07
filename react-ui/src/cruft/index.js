import axios from "axios";
import { useEffect, useState } from "react";
import { Button, Form, Spinner, Stack } from "react-bootstrap";
import CustomPieChart from "../graph/piechart";

const DateSelectorCruft = ({ attributes, token, projectId, onDateSubmit }) => {
    const [bvAttribute, setBvAttribute] = useState(null);
    const [data, setData] = useState(null);
    const [error, setError] = useState(false);
    const [spinner, setSpinner] = useState(false);
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');

    useEffect(() => {
        const attribute = attributes.map(attribute => {
            if (attribute.name.toLowerCase() === "bv" || attribute.name.toLowerCase() === "business value") {
                return attribute.id;
            }
            else {
                return null;
            }
        });
        setBvAttribute(attribute.length !== 0 ? attribute[0].toString() : null);
    }, [attributes]);

    const handleSubmit = (eventKey) => {
        eventKey.preventDefault();
        setError(false);
        setSpinner(true);

        const formData = {
            "projectId": projectId,
            "startDate": startDate,
            "endDate": endDate
        }

        if (bvAttribute !== null) {
            formData.attributeKey = bvAttribute
        }

        console.log(formData)

        axios({
            url: "http://localhost:8005/metric/Cruft",
            method: "post",
            data: formData,
            headers: {
                "token": token,
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "http://localhost:3000/project"
            }
        })
            .then(res => {
                setData(res.data);
                console.log(res.data);
                setError(false);
                setSpinner(false);
            })
            .catch(ex => {
                console.log(ex);
                setError(true);
                setSpinner(false);
            });
    }

    return (
        <div>
            <Form onSubmit={handleSubmit}>
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
                <Button variant="primary" type="submit" className="submitButton backgroundButton">Submit</Button>
            </Form>
            <div>
                <br />
                {spinner ? (
                    <div>
                        <Spinner variant="primary" animation="border" style={{ justifyContent: "center", alignItems: "center", display: "flex", marginLeft: "49%" }} />
                    </div>
                ) : null}

                {error ? (
                    <p className="errorMessage">Unable to fetch Sprint Detail</p>
                ) : null}

                {data ? (
                    <div>
                        <br />
                        <CustomPieChart apidata={data} title={"Zero Business Value Pie Chart"} />
                    </div>
                ) : null}
                <br />
            </div>
        </div>
    );
};


export default DateSelectorCruft;