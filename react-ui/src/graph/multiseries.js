import { Tooltip } from "react-bootstrap";
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, XAxis, YAxis } from "recharts";

const CustomMultiSeriesLineChart = ({ apiData, title, chartType, dataKey }) => {
    const colorGenerator = () => {
        let letters = "0123456789ABCDEF";
        let color = "#";
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    return (
        <div style={{ textAlign: 'center' }}>
            <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
                <div style={{ width: '90%' }}>
                    <h4 style={{ textAlign: 'center' }}>{title}</h4>
                    <ResponsiveContainer width="105%" height={600}>
                        <LineChart
                            width={500}
                            height={300}
                            margin={{top: 20, right: 40, left: 30, bottom: 70 }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />

                            <XAxis type="number" dataKey="day" name="Day" label={{ value: 'Day',
                                    position: 'insideBottom', offset: -50, style: {fontSize: '20px'}}}
                                    tick={{ textAnchor: 'end', fontSize: 12}} allowDuplicatedCategory={true} />
                            <YAxis dateKey="" name={chartType} label={{ value: `${chartType}`, 
                                    angle: -90, position: 'insideLeft', style: {fontSize: '20px'}}} />
                            <Tooltip />

                            <Legend align="right" verticalAlign="top" wrapperStyle={{ top: 0, right: 40, marginTop: '20px' }} />

                            {
                                apiData.map((s) => (
                                    <Line dataKey={dataKey} data={s.combined_burndown.data} name={s.sprint} key={s.sprint} stroke={colorGenerator()} strokeWidth={2} />
                                ))
                            }
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}

export default CustomMultiSeriesLineChart;
