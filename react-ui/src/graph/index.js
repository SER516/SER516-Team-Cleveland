import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

// Tooltip for Userstory graph
const UserstoryTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
        return (
            <div className="custom-tooltip" style={{ backgroundColor: '#fff', padding: '10px', border: '1px solid #ccc' }}>
                <p>Date : {payload[0].payload.name}</p>
                <p>Userstory : {payload[1].value}</p>
            </div>
        );
    }

    return null;
};

// Tooltip for Task graph
const TaskTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
        return (
            <div className="custom-tooltip" style={{ backgroundColor: '#fff', padding: '10px', border: '1px solid #ccc' }}>
                <p>Date : {payload[0].payload.name}</p>
                <p>Task : {payload[1].value}</p>
            </div>
        );
    }

    return null;
};

const Graph = () => {
    // Sample data
    const data = [
        {name: 'Jan 8th', Userstory: 18, Task: 35},
        {name: 'Jan 15th', Userstory: 24, Task: 28},
        {name: 'Jan 22th', Userstory: 16, Task: 24},
        {name: 'Jan 29th', Userstory: 10, Task: 20},
        {name: 'Feb 5th', Userstory: 30, Task: 15},
        {name: 'Feb 12th', Userstory: 20, Task: 13},
        {name: 'Feb 19th', Userstory: 27, Task: 14},
        {name: 'Feb 26th', Userstory: 18, Task: 10},
        {name: 'Mar 4th', Userstory: 23, Task: 8},
        {name: 'Mar 11th', Userstory: 34, Task: 5},
    ];

    // Calculate Average
    const avgUserstory = data.reduce((acc, cur) => acc + cur.Userstory, 0) / data.length;
    const avgTask = data.reduce((acc, cur) => acc + cur.Task, 0) / data.length;

    return (
        <div style={{ textAlign: 'center' }}>
            <h2 style={{ marginBottom: '70px' }}>Lead Time</h2>
            <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
                <div style={{ width: '50%' }}>
                    <h3 style={{ textAlign: 'center' }}>Userstory</h3>
                    <ResponsiveContainer height={600}>
                        <ScatterChart
                            margin={{top: 20, right: 40, bottom: 70, left: 30}}
                        >
                            <CartesianGrid />
                            <XAxis type="category" dataKey="name" name="Date" label={{ value: 'Date', 
                                    position: 'insideBottom', offset: -50, style: {fontSize: '20px'}}} 
                                    tick={{ angle: -45, textAnchor: 'end', fontSize: 12}}/>
                            <YAxis type="number" dataKey="Userstory" name="Userstory" label={{ value: 'Points', 
                                    angle: -90, position: 'insideLeft', style: {fontSize: '20px'}}} />
                            <Tooltip content={<UserstoryTooltip />} />
                            <Scatter name="Userstory" data={data} fill="#8884d8" />
                            <ReferenceLine y={avgUserstory} stroke="red" strokeDasharray="3 3" strokeWidth={2}
                                            label={{ value: 'Average', position: 'bottom', fontSize: 15, offset: 10 }} />
                        </ScatterChart>
                    </ResponsiveContainer>
                </div>

                <div style={{ width: '50%' }}>
                    <h3 style={{ textAlign: 'center' }}>Task</h3>
                    <ResponsiveContainer height={600}>
                        <ScatterChart
                            margin={{top: 20, right: 30, bottom: 70, left: 40}}
                        >
                            <CartesianGrid />
                            <XAxis type="category" dataKey="name" name="Date" label={{ value: 'Date', 
                                    position: 'insideBottom', offset: -50, style: {fontSize: '20px'}}}
                                    tick={{ angle: -45, textAnchor: 'end', fontSize: 12}}/>
                            <YAxis type="number" dataKey="Task" name="Tasks" label={{ value: 'Count', 
                                    angle: -90, position: 'insideLeft', style: {fontSize: '20px'}}} />
                            <Tooltip content={<TaskTooltip />} />
                            <Scatter name="Tasks" data={data} fill="#82ca9d" />
                            <ReferenceLine y={avgTask} stroke="red" strokeDasharray="3 3" strokeWidth={2}
                                            label={{ value: 'Average', position: 'bottom', fontSize: 15, offset: 10 }} />
                        </ScatterChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}

export default Graph;
