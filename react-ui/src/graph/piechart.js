import React from 'react';
import { PieChart, Pie, Tooltip, ResponsiveContainer, Cell } from 'recharts';

// For dummy Test
const CustomPieChart = ({ title }) => {
    const firstPieData = [
        { name: 'Total stories with BV', value: 120 },
        { name: 'Number of 0 BV stories', value: 30 },
        { name: 'Number of Issues', value: 20 },
    ];  

const secondPieData = [
    { name: 'Story points with BV', value: 200 },
    { name: 'Story points without BV', value: 50 },
];

const firstPieColors = ['#A7C7E7', '#F3A683', '#B8B5FF'];
const secondPieColors = ['#63CDD7', '#C3BED4'];

return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <h4 style={{ textAlign: 'center' }}>{title}</h4>
            <ResponsiveContainer width="50%" height={300}>
                <PieChart>
                    <Pie
                        data={firstPieData}
                        cx="50%"
                        cy="50%"
                        outerRadius={130}
                        dataKey="value"
                        nameKey="name"
                        label={({ name }) => name}
                    >
                        {firstPieData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={firstPieColors[index % firstPieColors.length]} />
                        ))}
                    </Pie>
                    <Tooltip />
                </PieChart>
            </ResponsiveContainer>
            <div style={{ textAlign: 'center', marginBottom: '50px' }}>Counts</div>
            <ResponsiveContainer width="50%" height={300}>
                <PieChart>
                    <Pie
                        data={secondPieData}
                        cx="50%"
                        cy="50%"
                        outerRadius={130}
                        dataKey="value"
                        nameKey="name"
                        label={({ name }) => name}
                    >
                        {secondPieData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={secondPieColors[index % firstPieColors.length]} />
                        ))}
                    </Pie>
                    <Tooltip />
                </PieChart>
            </ResponsiveContainer>
            <div style={{ textAlign: 'center' }}>Counts</div>
        </div>
    );
}          

export default CustomPieChart;