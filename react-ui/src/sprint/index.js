import axios from "axios";
import { useEffect, useState } from "react";
import { Dropdown, Spinner, Stack } from "react-bootstrap";
import Areachart from "../areachart";
import Graph from "../graph";

const SprintDetail = ({ sprintDetails, attributes, token, projectName }) => {
    const [selectedValue, setSelectedValue] = useState(null);
    const [bvAttribute, setBvAttribute] = useState(null);
    const [data, setData] = useState(null);
    const [error, setError] = useState(false);
    const [spinner, setSpinner] = useState(false);

    useEffect(() => {
        const attribute = attributes.map(attribute => {
            if (attribute.name.toLowerCase() === "bv" || attribute.name.toLowerCase()=== "business value") {
                return attribute.id;
            }
            else {
                return null;
            }
        });
        setBvAttribute(attribute.length !== 0 ? attribute[0].toString() : null);
    }, [attributes]);

    const handleSelect = (eventKey) => {
        const splitEventKey = eventKey.split(',');
        setSelectedValue(splitEventKey[1]);
        setError(false);
        setSpinner(true);

        const formData = {
            milestoneId: splitEventKey[0]
        }

        if (bvAttribute !== null) {
            formData.attributeKey = bvAttribute
        }

        axios({
            url: "http://localhost:8000/metric/Burndown",
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
            <div>
                <Stack gap={4}>
                    <h3 className="projectName">{projectName}</h3>
                    <div className="d-flex justify-content-center backgroundWhite">
                        <br />
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

                    {spinner ? (
                        <div>
                            <Spinner variant="primary" animation="border" style={{ justifyContent: "center", alignItems: "center", display:"flex", marginLeft: "49%" }} />
                        </div>
                    ) : null}

                    {error ? (
                        <p className="errorMessage">Unable to fetch Sprint Detail</p>
                    ) : null}
                    
                    {data ? (
                        <div>
                            <br />
                            <Areachart apiData={data.total_burndown.total_burndown_data} chartFor={"Story Points"} title={"Total Burndown Chart"} />
                            <Areachart apiData={data.partial_burndown.partial_burndown_data} chartFor={"Story Points"} title={"Partial Burndown Chart"} />
                            <Areachart apiData={data.bv_burndown.bv_burndown_data} chartFor={"Business Value"} title={"Business Value Burndown Chart"} />
                            <Graph apiData={data.combined_burndown.data} type="Burndown Chart" />
                        </div>
                    ) : null}
                </Stack>
            </div>
        </div>
    )
}

export default SprintDetail;