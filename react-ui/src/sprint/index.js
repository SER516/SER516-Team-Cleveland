import axios from "axios";
import { useEffect, useState } from "react";
import { Dropdown } from "react-bootstrap";

const SprintDetail = ({ sprintDetails, attributes, token }) => {
    console.log("Hello");
    const [selectedValue, setSelectedValue] = useState(null);
    const [bvAttribute, setBvAttribute] = useState(null);

    useEffect(() => {
        const attribute = attributes.map(attribute => {
            if (attribute.name.toLowerCase() === "bv" || attribute.name.toLowerCase()=== "business value") {
                return attribute.id;
            }
            else {
                return null;
            }
        });
        setBvAttribute(attribute);
    }, [attributes]);

    const handleSelect = (eventKey) => {
        const splitEventKey = eventKey.split(',');
        setSelectedValue(splitEventKey[1]);

        axios({
            url: "http://localhost:8000/metric/Burndown",
            method: "post",
            data: {
                milestoneId: splitEventKey[0],
                attributeKey: bvAttribute.toString()
            },
            headers: {
                "token": token,
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "http://localhost:3000/project"
            }
        })
        .then(res => {
            console.log(res.data);
        })
        .catch(ex => {
            console.log(ex);
        });
    }

    return (
        <div style={{ justifyContent: "center", alignItems: "center" }} className="d-flex align-items-center justify-content-center vh-100 backgroundWhite">
            <Dropdown onSelect={handleSelect}>
                <Dropdown.Toggle variant="outline-secondary" className="backgroundButton">
                    {selectedValue ? selectedValue : 'Select Metric'}
                </Dropdown.Toggle>
                <Dropdown.Menu>
                    {
                        sprintDetails.map((item) => <Dropdown.Item key={item.id} eventKey={[item.id, item.name]}>{item.name}</Dropdown.Item>)
                    }
                </Dropdown.Menu>
            </Dropdown>
        </div>
    )
}

export default SprintDetail;