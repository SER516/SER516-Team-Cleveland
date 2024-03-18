import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const CustomLineChart = ( ) => {
    const dummyData = [
        { date: '2024-03-01', 'Total Burndown Chart': 40, 'Partial Burndown Chart': 40, 'Business Value Burndown Chart': 30 },
        { date: '2024-03-02', 'Total Burndown Chart': 37, 'Partial Burndown Chart': 37, 'Business Value Burndown Chart': 27 },
        { date: '2024-03-03', 'Total Burndown Chart': 35, 'Partial Burndown Chart': 35, 'Business Value Burndown Chart': 25 },
        { date: '2024-03-04', 'Total Burndown Chart': 30, 'Partial Burndown Chart': 30, 'Business Value Burndown Chart': 22 },
        { date: '2024-03-05', 'Total Burndown Chart': 25, 'Partial Burndown Chart': 25, 'Business Value Burndown Chart': 20 },
        { date: '2024-03-06', 'Total Burndown Chart': 25, 'Partial Burndown Chart': 23, 'Business Value Burndown Chart': 20 },
        { date: '2024-03-07', 'Total Burndown Chart': 20, 'Partial Burndown Chart': 20, 'Business Value Burndown Chart': 15 },
    ];

    return (
        <div style={{ textAlign: 'center' }}>
            <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
                <div style={{ width: '90%' }}>
                    <h4 style={{ textAlign: 'center' }}>Total Burndown Chart</h4>
                    <ResponsiveContainer width="105%" height={600}>
                        <LineChart
                            width={500}
                            height={300}
                            data={dummyData}
                            margin={{top: 20, right: 40, left: 30, bottom: 70,}}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis type="category" dataKey="date" name="Date" label={{ value: 'Date',
                                    position: 'insideBottom', offset: -50, style: {fontSize: '20px'}}}
                                    tick={{ angle: -45, textAnchor: 'end', fontSize: 12}} allowDuplicatedCategory={false} />
                            <YAxis type="number" dateKey="" name="Percent" label={{ value: `Percent`, 
                                    angle: -90, position: 'insideLeft', style: {fontSize: '20px'}}} />
                            <Tooltip />
                            <Legend align="right" verticalAlign="top" layout="vertical" />
                            <Line type="monotone" dataKey="Total Burndown Chart" stroke="#8884d8" activeDot={{ r: 8 }} />
                            <Line type="monotone" dataKey="Partial Burndown Chart" stroke="#82ca9d" />
                            <Line type="monotone" dataKey="Business Value Burndown Chart" stroke="#ffc658" />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default CustomLineChart;
