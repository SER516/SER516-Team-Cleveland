import axios from "axios";
import { useEffect, useState } from "react";
import Select from 'react-select';
import { Spinner, Stack } from "react-bootstrap";
import Areachart from "../areachart";
import Graph from "../graph";

const SprintDetail = ({ sprintDetails, attributes, token, projectName }) => {
    const [selectedValues, setSelectedValues] = useState([]);
    const [bvAttribute, setBvAttribute] = useState(null);
    const [data, setData] = useState({});
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

    const handleSelect = (selectedOptions) => {
        setSelectedValues(selectedOptions);
        setError(false);
        setSpinner(true);

        const fetchDataForSelectedValues = selectedOptions.map(option => {
            const formData = {
                milestoneId: option.value,
                ...(bvAttribute && { attributeKey: bvAttribute })
            };

            return axios({
                url: "http://localhost:8000/metric/Burndown",
                method: "post",
                data: formData,
                headers: {
                    "token": token,
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "http://localhost:3000/project"
                }
            })
            .then(res => ({ [option.value]: res.data }))
            .catch(ex => {
                console.error(ex);
                setError(true);
            });
        });

        Promise.all(fetchDataForSelectedValues).then(results => {
            const newData = results.reduce((acc, result) => ({
                ...acc,
                ...result
            }), {});

            setData(newData);
            setSpinner(false);
        });
    };

    const options = sprintDetails.map(detail => ({
        value: detail.id,
        label: detail.name
    }));

    return (
        <div>
            <Stack gap={4}>
                <h3 className="projectName">{projectName}</h3>
                <div className="d-flex justify-content-center backgroundWhite">
                    <Select
                        isMulti
                        options={options}
                        className="basic-multi-select"
                        classNamePrefix="select"
                        onChange={handleSelect}
                        placeholder="Select Metrics"
                    />
                </div>

                {spinner && (
                    <Spinner animation="border" variant="primary" style={{ display: "block", marginLeft: "auto", marginRight: "auto" }} />
                )}

                {error && <p className="errorMessage">Unable to fetch Sprint Detail</p>}
                
                {Object.keys(data).length > 0 && Object.entries(data).map(([key, value]) => (
                    <div key={key}>
                        <br />
                        <Areachart apiData={data.total_burndown.total_burndown_data} chartFor={"Story Points"} title={`Total Burndown Chart for ${key}`} />
                        <Areachart apiData={data.partial_burndown.partial_burndown_data} chartFor={"Story Points"} title={`Partial Burndown Chart for ${key}`} />
                        <Areachart apiData={data.bv_burndown.bv_burndown_data} chartFor={"Business Value"} title={`Business Value Burndown Chart for ${key}`} />
                        <Graph apiData={data.combined_burndown.data} type={`Burndown Chart for ${key}`} />
                    </div>
                ))}
            </Stack>
        </div>
    );
};

export default SprintDetail;