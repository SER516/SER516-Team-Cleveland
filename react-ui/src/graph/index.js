import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

const Graph = ({ apiData, avg, chartFor, title }) => {
    const CustomToolTip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip" style={{ backgroundColor: '#fff', padding: '10px', border: '1px solid #ccc' }}>
                    <p>Date : {payload[0].value}</p>
                    <p>Days : {payload[1].value}</p>
                </div>
            );
        }
    
        return null;
    };

    return (
        <div style={{ textAlign: 'center' }}>
            <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
                <div style={{ width: '90%' }}>
                    <h4 style={{ textAlign: 'center' }}>{title}</h4>
                    <ResponsiveContainer height={600}>
                        <ScatterChart
                            margin={{top: 20, right: 40, bottom: 70, left: 30}}
                        >
                            <CartesianGrid />
                            <XAxis type="category" dataKey="endDate" name="End Date" label={{ value: 'End Date', 
                                    position: 'insideBottom', offset: -50, style: {fontSize: '20px'}}} 
                                    tick={{ angle: -45, textAnchor: 'end', fontSize: 12}} allowDuplicatedCategory={false} />
                            <YAxis type="number" dataKey="timeTaken" name="Time" label={{ value: `Days to complete ${chartFor}`, 
                                    angle: -90, position: 'insideLeft', style: {fontSize: '20px'}}} />
                            <Tooltip content={<CustomToolTip />} />
                            <Scatter name={title} data={apiData} fill="#8884d8" />
                            <ReferenceLine y={avg} stroke="red" strokeDasharray="3 3" strokeWidth={2}
                                            label={{ value: `Average ${avg} Days`, position: 'above', fontSize: 15, offset: 10, fill: "black", fontWeight: "bold" }} />
                        </ScatterChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}

export default Graph;
