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
                            <defs>
                                <linearGradient id="colorExpected" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#D04848" stopOpacity={0.8}/>
                                    <stop offset="95%" stopColor="#D04848" stopOpacity={0.1}/>
                                </linearGradient>
                                <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#6895D2" stopOpacity={0.8}/>
                                    <stop offset="95%" stopColor="#6895D2" stopOpacity={0.1}/>
                                </linearGradient>
                            </defs>
                            <CartesianGrid />
                            <XAxis type="category" dataKey="date" name="Date" label={{ value: 'Date',
                                    position: 'insideBottom', offset: -50, style: {fontSize: '20px'}}}
                                    tick={{ angle: -45, textAnchor: 'end', fontSize: 12}} allowDuplicatedCategory={false} />

                            <YAxis type="number" label={{ value: `${chartFor}`,
                                    angle: -90, position: 'insideLeft', style: {fontSize: '20px'}}} />
                            <Tooltip />
                            <Area dataKey="remaining" stroke="#6895D2" fillOpacity={1} fill="url(#colorActual)" />
                            <Area dataKey="expected_remaining" stroke="#D04848" fillOpacity={1} fill="url(#colorExpected)"/>
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}

export default Areachart;