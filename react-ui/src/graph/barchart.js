import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from 'recharts';

// For dummy Test
const CustomBarChart = ({ title }) => {
    const dummyData = [
        { name: 'User A', counts: 5},
        { name: 'User B', counts: 3},
        { name: 'User C', counts: 2},
        { name: 'User D', counts: 1},
        { name: 'User E', counts: 2},
        { name: 'User F', counts: 3},
    ];
// const CustomBarChart = ({ apiData, title }) => {
    // const CustomToolTip = ({ active, payload }) => {
    //     if (active && payload && payload.length) {
    //         return (
    //             <div className="custom-tooltip" style={{ backgroundColor: '#ffd7b5', padding: '5px', border: '1px solid #ccc', borderRadius: "5px"}}>
    //                 <b>Date:</b> {payload[0].value}<br/>
    //                 <b>Days:</b> {payload[1].value}<br/>
    //                 <b>Task ID:</b> {payload[1].payload.taskRef}<br/>
    //                 <b>Task Description:</b> {payload[1].payload.taskDesc}<br/>
    //             </div>
    //         );
    //     }
    //     return null;
    // };

    return (
        <div>
            <div>
                <h4 style={{ textAlign: 'center' }}>{title}</h4>
                <ResponsiveContainer height={600}>
                    <BarChart
                        data={dummyData}  // For dummy Test
                        margin={{ top: 20, right: 40, bottom: 70, left: 30 }}
                    >    
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="category" dataKey="name" label={{
                            value: 'User',
                            position: 'insideBottom', offset: -50, style: { fontSize: '20px' }
                        }}
                            tick={{ fontSize: 12 }} allowDuplicatedCategory={false} />
                        <YAxis type="number" dataKey="" label={{
                            value: 'Counts', angle: -90, position: 'insideLeft', style: { fontSize: '20px' }
                        }} />
                        {/* <Tooltip content={<CustomToolTip />} /> */}
                        <BarChart name={title} data={dummyData} fill="#8884d8" />
                        <Bar dataKey="counts" fill="#8884d8" />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

export default CustomBarChart;
