import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Graph = () => {
    // Sample data
    const data = [
        {name: 'Jan 29th', Userstory: 10, Task: 20},
        {name: 'Feb 5th', Userstory: 30, Task: 15},
        {name: 'Feb 12th', Userstory: 20, Task: 13},
        {name: 'Feb 19th', Userstory: 27, Task: 14},
        {name: 'Feb 26th', Userstory: 18, Task: 10},
        {name: 'Mar 4th', Userstory: 23, Task: 8},
        {name: 'Mar 11th', Userstory: 34, Task: 5},
    ];

    return (
        <div style={{ textAlign: 'center' }}>
            <h2 style={{ marginBottom: '70px' }}>Lead Time</h2>
            <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
                <div style={{ width: '50%' }}>
                    <h3 style={{ textAlign: 'center' }}>Userstory</h3>
                    <ResponsiveContainer height={600}>
                        <ScatterChart
                            margin={{top: 20, right: 20, bottom: 20, left: 20}}
                        >
                            <CartesianGrid />
                            <XAxis type="category" dataKey="name" name="Date" label={{ value: 'Date', 
                                    position: 'insideBottom', offset: -20, style: {fontSize: '20px'}}} />
                            <YAxis type="number" dataKey="Userstory" name="Userstory" label={{ value: 'Points', 
                                    angle: -90, position: 'insideLeft', style: {fontSize: '20px'}}} />
                            <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                            <Scatter name="Userstory" data={data} fill="#8884d8" />
                        </ScatterChart>
                    </ResponsiveContainer>
                </div>

                <div style={{ width: '50%' }}>
                    <h3 style={{ textAlign: 'center' }}>Task</h3>
                    <ResponsiveContainer height={600}>
                        <ScatterChart
                            margin={{top: 20, right: 20, bottom: 20, left: 20}}
                        >
                            <CartesianGrid />
                            <XAxis type="category" dataKey="name" name="Date" label={{ value: 'Date', 
                                    position: 'insideBottom', offset: -20, style: {fontSize: '20px'}}} />
                            <YAxis type="number" dataKey="Task" name="Tasks" label={{ value: 'Count', 
                                    angle: -90, position: 'insideLeft', style: {fontSize: '20px'}}} />
                            <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                            <Scatter name="Tasks" data={data} fill="#82ca9d" />
                        </ScatterChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}

export default Graph;
