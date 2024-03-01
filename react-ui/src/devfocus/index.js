import axios from "axios";
import { useEffect, useState } from "react";
import { Button, Dropdown, FloatingLabel, Form, InputGroup } from "react-bootstrap";
import CustomBarChart from "../graph/barchart";
import CustomCard from "../cards";

const DateSelector = ({ onDateSubmit, memberDetails, token, projectId }) => {
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [selectedValue, setSelectedValue] = useState(null);
    const [selectedMemeberId, setSelectedMemberId] = useState(null);
    const [threshold, setThreshold] = useState(null);
    const [data, setData] = useState(null);
    const [totalViolations, setTotalViolations] = useState(0);
    const [members, setMembers] = useState([]);
    const [teamMembers, setTeamMembers] = useState([]);
    const [title, setTitle] = useState(null);
    const [isDevFocus, setIsDevFocus] = useState(false);

    useEffect(() => {
        let allMembers = [];
        for (let member of memberDetails) {
            allMembers.push(member.id);
        }
        setTeamMembers(allMembers);
    }, [memberDetails]);

    const handleSelect = (eventKey) => {
        const splitEventKey = eventKey.split(',');
        setSelectedValue(splitEventKey[1]);
        setIsDevFocus(false);
        if (splitEventKey[0] !== "All") {
            setSelectedMemberId([splitEventKey[0]]);
            setTitle(`${splitEventKey[1]} Violations`);
        }
        else {
            setSelectedMemberId(teamMembers);
            setTitle("Team Violations");
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Selected Start Date: ", startDate, "Selected End Date: ", endDate, projectId, threshold, selectedMemeberId);
        onDateSubmit(startDate, endDate);

        axios({
            method: "post",
            url: `http://localhost:8000/metric/Devfocus2`,
            data: {
                members: selectedMemeberId,
                from_date: startDate,
                to_date: endDate,
                project_id: projectId.toString(),
                threshold: threshold
            },
            headers: {
                "Content-Type": "application/json",
                "token": token
            }
        })
        .then(res => {
            setData(res.data);
            let totalViolations = 0;
            for (let name in res.data) {
                totalViolations += Object.values(res.data[name]).length
            }
            setTotalViolations(totalViolations);
            setMembers(Object.keys(res.data));
            setIsDevFocus(true);
        })
        .catch(ex => {
            setIsDevFocus(false);
        });
    }

    const handleThresholdChange = (event) => {
        event.preventDefault();
        setThreshold(event.target.value);
        setIsDevFocus(false);
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
                                    <Dropdown.Item key="all" eventKey={["All", "All"]}>All</Dropdown.Item>
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

            {isDevFocus ? (
                <div>
                    <br />
                    <CustomCard num={totalViolations} from={startDate} to={endDate} members={members} title={title} />
                    <br />
                    <CustomBarChart title={"Charts"} data={data} threshold={threshold} />
                </div>
            ) : null}
        </div>
    );
};
      

export default DateSelector;
