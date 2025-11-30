import React, { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard() {
    const [data, setData] = useState({});

    const load = async () => {
        const res = await axios.get("http://127.0.0.1:8000/dashboard");
        setData(res.data);
    };

    useEffect(() => {
        load();
        const interval = setInterval(load, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="p-8 text-white bg-[#0B0F1A] min-h-screen">
            <h1 className="text-3xl font-bold">NovaSecurity AI</h1>

            <div className="grid grid-cols-4 gap-4 mt-6">
                <Card title="CPU Usage" value={data.cpu + "%"} />
                <Card title="RAM" value={data.ram + "%"} />
                <Card title="Active Attacks" value={data.attacks} />
                <Card title="Blocked IPs" value={data.blocked_ips} />
            </div>

            <h2 className="text-xl mt-10">Recent Attacks</h2>
            {data.recent?.map((item, i) => (
                <div key={i} className="bg-[#111827] p-4 mt-2 rounded">
                    <p><b>IP:</b> {item.ip}</p>
                    <p><b>Type:</b> {item.type}</p>
                    <p><b>Risk:</b> {item.risk}</p>
                    <p><b>Time:</b> {item.time}</p>
                </div>
            ))}
        </div>
    );
}

function Card({ title, value }) {
    return (
        <div className="bg-[#111827] p-6 rounded-lg">
            <p className="text-gray-300">{title}</p>
            <h2 className="text-2xl font-bold">{value}</h2>
        </div>
    );
}
