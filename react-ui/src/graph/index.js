import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

const Graph = ({ apiData, avg, chartFor, title }) => {
    const CustomToolTip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip" style={{ backgroundColor: '#ffd7b5', padding: '5px', border: '1px solid #ccc', borderRadius: "5px"}}>
                    <b>Date:</b> {payload[0].value}<br/>
                    <b>Days:</b> {payload[1].value}<br/>
                    <b>Task ID:</b> {payload[1].payload.taskRef}<br/>
                    <b>Task Description:</b> {payload[1].payload.taskDesc}<br/>                    
                </div>
            );
        }

        return null;
    };

    return (
        <div>
            <div>
                <h4 style={{ textAlign: 'center' }}>{title}</h4>
                <ResponsiveContainer height={600}>
                    <ScatterChart
                        margin={{ top: 20, right: 40, bottom: 70, left: 30 }}
                    >
                        <CartesianGrid />
                        <XAxis type="category" dataKey="endDate" name="End Date" label={{
                            value: 'End Date',
                            position: 'insideBottom', offset: -50, style: { fontSize: '20px' }
                        }}
                            tick={{ angle: -45, textAnchor: 'end', fontSize: 12 }} allowDuplicatedCategory={false} />
                        <YAxis type="number" dataKey="timeTaken" name="Time" label={{
                            value: `Days to complete ${chartFor}`,
                            angle: -90, position: 'insideLeft', style: { fontSize: '20px' }
                        }} />
                        <Tooltip content={<CustomToolTip />} />
                        <Scatter name={title} data={apiData} fill="#8884d8" />
                        <ReferenceLine y={avg} stroke="orange" strokeWidth={2}
                            label={{ value: `${avg}`, position: 'left', fontSize: 15, offset: 5, fill: "#FF8989", fontWeight: "bold" }} />
                    </ScatterChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

export default Graph;