"use client";

import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";
import { chartTheme, fmtCurrency } from "./theme";

interface BarBasicProps {
  data: any[];
  x: string;
  y: string;
  title?: string;
  className?: string;
}

export default function BarBasic({ data, x, y, title, className = "" }: BarBasicProps) {
  return (
    <div className={`bg-surface border border-border rounded-[12px] shadow-sm p-4 ${className}`}>
      {title && (
        <div className="text-base font-medium text-text mb-4">{title}</div>
      )}
      
      <div className="h-[220px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart 
            data={data} 
            margin={{ top: 8, right: 8, left: 8, bottom: 8 }}
            style={{ direction: "rtl" }}
          >
            <CartesianGrid 
              stroke={chartTheme.chart.grid} 
              strokeDasharray="3 3" 
              strokeOpacity={0.3}
            />
            <XAxis 
              dataKey={x} 
              tickLine={false} 
              axisLine={false} 
              stroke={chartTheme.chart.axisColor}
              fontSize={12}
              fontFamily={chartTheme.typography.fontFamily}
            />
            <YAxis 
              tickFormatter={fmtCurrency} 
              tickLine={false} 
              axisLine={false} 
              stroke={chartTheme.chart.axisColor}
              fontSize={12}
              fontFamily={chartTheme.typography.fontFamily}
            />
            <Tooltip 
              formatter={(value: number) => [fmtCurrency(value), y]}
              labelFormatter={(label) => `${x}: ${label}`}
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
            <Bar 
              dataKey={y} 
              fill={chartTheme.chart.bar} 
              radius={[8, 8, 0, 0]}
              stroke={chartTheme.chart.bar}
              strokeWidth={1}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}



