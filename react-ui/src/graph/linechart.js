import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const CustomLineChart = ({ data }) => {

    return (
        <div style={{ textAlign: 'center' }}>
            <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
                <div style={{ width: '90%' }}>
                    <h4 style={{ textAlign: 'center' }}>Burndown Chart</h4>
                    <ResponsiveContainer width="105%" height={600}>
                        <LineChart
                            width={500}
                            height={300}
                            data={data}
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
                            <Line dataKey="total" stroke="#8884d8" strokeWidth={2} />
                            <Line dataKey="partial" stroke="#82ca9d" strokeWidth={2} />
                            <Line dataKey="bv" stroke="#ffc658" strokeWidth={2} />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default CustomLineChart;
