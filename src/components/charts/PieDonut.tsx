"use client";

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";
import { chartTheme, fmtCurrency } from "./theme";

interface PieDonutProps {
  data: any[];
  dataKey: string;
  nameKey: string;
  title?: string;
  className?: string;
}

export default function PieDonut({ data, dataKey, nameKey, title, className = "" }: PieDonutProps) {
  return (
    <div className={`bg-surface border border-border rounded-[12px] shadow-sm p-4 ${className}`}>
      {title && (
        <div className="text-base font-medium text-text mb-4">{title}</div>
      )}
      
      <div className="h-[220px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={100}
              paddingAngle={2}
              dataKey={dataKey}
              nameKey={nameKey}
            >
              {data.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={chartTheme.chart.pie[index % chartTheme.chart.pie.length]} 
                />
              ))}
            </Pie>
            <Tooltip 
              formatter={(value: number) => [fmtCurrency(value), dataKey]}
              contentStyle={{
                background: "var(--surface)",
                border: `1px solid var(--border)`,
                borderRadius: "8px",
                boxShadow: "var(--shadow-md)",
                fontFamily: chartTheme.typography.fontFamily
              }}
              labelStyle={{
                color: "var(--text)",
                fontSize: "var(--text-sm)"
              }}
            />
            <Legend 
              verticalAlign="bottom" 
              height={36}
              iconType="circle"
              wrapperStyle={{
                fontFamily: chartTheme.typography.fontFamily,
                fontSize: "var(--text-xs)",
                color: "var(--text)"
              }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}



