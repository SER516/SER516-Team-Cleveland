import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const CustomLineChart = ( ) => {
    const dummyData = [
        { date: '03-01-2024', 'Total Burndown Chart': 100, 'Partial Burndown Chart': 100, 'Business Value Burndown Chart': 80 },
        { date: '03-02-2024', 'Total Burndown Chart': 80, 'Partial Burndown Chart': 80, 'Business Value Burndown Chart': 60 },
        { date: '03-03-2024', 'Total Burndown Chart': 60, 'Partial Burndown Chart': 60, 'Business Value Burndown Chart': 40 },
        { date: '03-04-2024', 'Total Burndown Chart': 60, 'Partial Burndown Chart': 40, 'Business Value Burndown Chart': 40 },
        { date: '03-05-2024', 'Total Burndown Chart': 30, 'Partial Burndown Chart': 30, 'Business Value Burndown Chart': 20 },
        { date: '03-06-2024', 'Total Burndown Chart': 30, 'Partial Burndown Chart': 15, 'Business Value Burndown Chart': 20 },
        { date: '03-07-2024', 'Total Burndown Chart': 0, 'Partial Burndown Chart': 0, 'Business Value Burndown Chart': 0 },
    ];

    return (
        <div style={{ textAlign: 'center' }}>
            <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
                <div style={{ width: '90%' }}>
                    <h4 style={{ textAlign: 'center' }}>Burndown Chart</h4>
                    <ResponsiveContainer width="105%" height={600}>
                        <LineChart
                            width={500}
                            height={300}
                            data={dummyData}
                            margin={{top: 20, right: 40, left: 30, bottom: 70 }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis type="category" dataKey="date" name="Date" label={{ value: 'Date',
                                    position: 'insideBottom', offset: -50, style: {fontSize: '20px'}}}
                                    tick={{ angle: -45, textAnchor: 'end', fontSize: 12}} allowDuplicatedCategory={false} />
                            <YAxis type="number" dateKey="" name="Percent" label={{ value: `Percent`, 
                                    angle: -90, position: 'insideLeft', style: {fontSize: '20px'}}} />
                            <Tooltip />
                            <Legend align="right" verticalAlign="top" wrapperStyle={{ top: 0, right: 0, marginTop: '20px' }} />
                            <Line type="monotone" dataKey="Total Burndown Chart" stroke="#8884d8" />
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
