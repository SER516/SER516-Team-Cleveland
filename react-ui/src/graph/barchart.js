import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Legend, CartesianGrid, ResponsiveContainer } from 'recharts';

// For dummy Test
const CustomBarChart = ({ title }) => {
    const dummyData = [
        { name: 'User 1', counts: 5},
        { name: 'User 2', counts: 3},
        { name: 'User 3', counts: 2},
        { name: 'User 4', counts: 1},
        { name: 'User 5', counts: 2},
    ];  
    
    const stackedData = [
        { date: '2024-02-01', User1: 3, User2: 4, User3: 5, User4: 2, User5: 3 },
        { date: '2024-02-02', User1: 2, User2: 3, User3: 4, User4: 5, User5: 2  },
        { date: '2024-02-03', User1: 5, User2: 1, User3: 2, User4: 3, User5: 4  },
        { date: '2024-02-04', User1: 4, User2: 2, User3: 4, User4: 1, User5: 1  },
        { date: '2024-02-05', User1: 2, User2: 3, User3: 3, User4: 2, User5: 2  },
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
                <ResponsiveContainer height={1250}>
                    <div>
                        <BarChart
                            width={1400}
                            height={600}
                            data={dummyData}  // For dummy Test
                            margin={{ top: 20, right: 40, bottom: 70, left: 30 }}
                        >    
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis type="category" dataKey="name" label={{
                                value: 'User', position: 'insideBottom', offset: -50, style: { fontSize: '20px' }
                            }}
                                tick={{ fontSize: 12 }} allowDuplicatedCategory={false} />
                            <YAxis type="number" dataKey="" label={{
                                value: 'Counts', angle: -90, position: 'insideLeft', style: { fontSize: '20px' }
                            }} />
                            {/*<Tooltip content={<CustomToolTipTop />} />*/}
                            <BarChart name={title} data={dummyData} fill="#8884d8" />
                            <Bar dataKey="counts" fill="#8884d8" />
                        </BarChart>
                        <div style={{ height: 20}} />
                        <BarChart
                            width={1400}
                            height={600}
                            data={stackedData}
                            margin={{ top: 20, right: 40, bottom: 70, left: 30 }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis type="category" dataKey="date" label={{value: 'Date',
                                position: 'insideBottom', offset: -50, style: { fontSize: '20px' }
                            }}
                                tick={{ fontSize: 12 }} allowDuplicatedCategory={false} />
                            <YAxis type="number" dataKey="" label={{
                                value: 'Counts', angle: -90, position: 'insideLeft', style: { fontSize: '20px' }
                            }} />
                            {/*<Tooltip content={<CustomToolTipBottom />} />*/}
                            <Legend align="right" verticalAlign="top" layout="horizontal" iconType="square"/>
                            <Bar dataKey="User1" stackId="a" fill="#8884d8" />
                            <Bar dataKey="User2" stackId="a" fill="#82ca9d" />
                            <Bar dataKey="User3" stackId="a" fill="#ffc658" />
                            <Bar dataKey="User4" stackId="a" fill="#d45087" />
                            <Bar dataKey="User5" stackId="a" fill="#8e7cc3" />
                    </BarChart>
                </div>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

export default CustomBarChart;
