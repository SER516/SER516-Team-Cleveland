import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Legend, CartesianGrid, ResponsiveContainer } from 'recharts';

// For dummy Test
const CustomBarChart = ({ title, data, threshold }) => {
    console.log("Hello", data);
    const [memberData, setMemberData] = useState([]);
    const [totalViolations, setTotalViolations] = useState(0);
    const [dateData, setDateData] = useState({});
    const [members, setMembers] = useState([]);

    const colorGenerator = () => {
        let letters = "0123456789ABCDEF";
        let color = "#";
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    useEffect(() => {
        let temp_arr = [];
        console.log(data);
        let members = [];

        let tempDateMap = {};
        for (const name in data) {
            let count = 0;
            let obj = {}
            for (const date in data[name]) {
                if (data[name][date].length >= threshold) {
                    obj["name"] = name;
                    obj["date"] = date;
                    count = count + 1;
                    obj["tasks_size"] = data[name][date].length

                    if (date in tempDateMap) {
                        tempDateMap[date][name] = data[name][date].length;
                    }
                    else {
                        tempDateMap[date] = {}
                        tempDateMap[date]["date"] = date;
                        tempDateMap[date][name] = data[name][date].length;
                    }
                }
            }
            obj["violations"] = count;
            temp_arr.push(obj);
            members.push(name);
        }
        console.log(temp_arr);
        console.log(tempDateMap);
        setMemberData(temp_arr);
        setTotalViolations(temp_arr.length);
        setDateData(Object.values(tempDateMap));
        setMembers(members);
    }, [data, threshold]); 

    return (
        <div>
            <h4 style={{ textAlign: 'center' }}>{title}</h4>
            <ResponsiveContainer width="100%" height={600}>
                <BarChart
                    data={memberData}  // For dummy Test
                    margin={{ top: 20, right: 40, bottom: 70, left: 30 }}
                >    
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="category" dataKey="name" label={{
                        value: 'User', position: 'insideBottom', offset: -50, style: { fontSize: '20px' }
                    }}
                        tick={{ fontSize: 12 }} allowDuplicatedCategory={false} />
                    <YAxis type="number" dataKey="" label={{
                        value: 'Violations', angle: -90, position: 'insideLeft', style: { fontSize: '20px' }
                    }} />
                    <Bar dataKey="violations" fill="#8884d8" />
                </BarChart>
            </ResponsiveContainer>
            <ResponsiveContainer width="100%" height={600}>
                <BarChart
                    data={dateData}
                    margin={{ top: 20, right: 40, bottom: 70, left: 30 }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="category" dataKey="date" label={{value: 'Date',
                        position: 'insideBottom', offset: -50, style: { fontSize: '20px' }
                    }}
                        tick={{ fontSize: 12 }} allowDuplicatedCategory={false} />
                    <YAxis type="number" dataKey="" label={{
                        value: 'Violations', angle: -90, position: 'insideLeft', style: { fontSize: '20px' }
                    }} />
                    <Legend align="right" verticalAlign="top" layout="horizontal" iconType="square"/>

                    {
                        members.map(member => {
                            return <Bar key={member} dataKey={member} stackId="a" fill={colorGenerator()} />
                        })
                    }
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}

export default CustomBarChart;
