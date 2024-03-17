import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Legend, CartesianGrid, ResponsiveContainer, Tooltip, Rectangle } from 'recharts';

const CustomBarChart = ({ title, data, threshold, endDate }) => {
    const [memberData, setMemberData] = useState([]);
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
        let members = [];

        let tempDateMap = {};
        for (const name in data) {
            let count = 0;
            let obj = {}
            for (const date in data[name]) {
                let list = data[name][date].filter(task => task["inProgressDate"] !== null);
                let filteredTasks = filterTasks(list);
                if (filteredTasks.length >= threshold) {
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
            if (obj["violations"] !== 0) {
                temp_arr.push(obj);
                members.push(name);
            }
        }
        setMemberData(temp_arr);
        setDateData(Object.values(tempDateMap));
        setMembers(members);
    }, [data, threshold]);

    const filterTasks = (tasks) => {
        let removeTasks = [];
        for (let t1 of tasks) {
            for (let t2 of tasks) {
                if (t1["taskId"] !== t2["taskId"]) {
                    let date1 = new Date(t1["inProgressDate"]);
                    let date2 = new Date(t2["finished_date"]);
                    if (date1.getUTCDate() === date2.getUTCDate() && date1.getUTCSeconds() > date2.getUTCSeconds()) {
                        removeTasks.push(t2["taskId"]);
                    }
                }
            }
        }
        return tasks.filter(task => !removeTasks.includes(task["taskId"]));
    }

    return (
        <div>
            <h4 style={{ textAlign: 'center' }}>{title}</h4>
            <ResponsiveContainer width="100%" height={600}>
                <BarChart
                    data={memberData}
                    margin={{ top: 20, right: 40, bottom: 70, left: 30 }}
                >    
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="category" dataKey="name" label={{
                        value: 'User', position: 'insideBottom', offset: -50, style: { fontSize: '20px' }
                    }}
                        tick={{ fontSize: 12 }} allowDuplicatedCategory={true} />
                    <YAxis type="number" dataKey="" label={{
                        value: 'Violations', angle: -90, position: 'insideLeft', style: { fontSize: '20px' }
                    }} />

                    <Tooltip />
                    <Bar dataKey="violations" fill="#8884d8" activeBar={<Rectangle fill="orange" stroke="purple" />} />
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
                        tick={{ fontSize: 12 }} allowDuplicatedCategory={true} />
                    <YAxis type="number" dataKey="" label={{
                        value: 'In Progress Tasks Count', angle: -90, position: 'insideLeft', style: { fontSize: '20px' }
                    }} />

                    <Tooltip />

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
