import React from 'react';
import {
  AreaChart,
  ResponsiveContainer,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
const Areachart = ({ apiData, chartFor, title }) => {
    return (
        <div style={{ textAlign: 'center' }}>
            <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
                <div style={{ width: '90%' }}>
                    <h4 style={{ textAlign: 'center' }}>{title}</h4>
                    <ResponsiveContainer height={600}>
                        <AreaChart
                            margin={{top: 20, right: 40, bottom: 70, left: 30}}
                            data = {apiData}
                        >
                            <CartesianGrid />
                            <XAxis type="category" dataKey="date" name="Date" label={{ value: 'Date',
                                    position: 'insideBottom', offset: -50, style: {fontSize: '20px'}}}
                                    tick={{ angle: -45, textAnchor: 'end', fontSize: 12}} allowDuplicatedCategory={false} />

                            <YAxis type="number" label={{ value: `${chartFor}`,
                                    angle: -90, position: 'insideLeft', style: {fontSize: '20px'}}} />
                            <Tooltip />
                            <Area dataKey="remaining" stackId="1" stroke="#CCFEFF" fill="#CCFEFF" />
                            <Area dataKey="expected_remaining" stackId="1" stroke="#FFCCCB" fill="#FFCCCB"/>
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}

export default Areachart;