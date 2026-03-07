import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { motion } from 'framer-motion'

const ProbabilityChart = ({ probabilities }) => {
  const data = Object.entries(probabilities).map(([name, value]) => ({
    name,
    probability: (value * 100).toFixed(2),
    value: parseFloat((value * 100).toFixed(2))
  }))

  const colors = {
    'Normal': '#10b981',
    'Pneumonia': '#ef4444',
    'Tuberculosis': '#f59e0b',
    'COVID-19': '#8b5cf6',
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="card p-6"
    >
      <h3 className="text-xl font-bold text-gray-900 mb-6">Probability Distribution</h3>
      
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="name" 
            tick={{ fill: '#6b7280', fontSize: 12 }}
            angle={-15}
            textAnchor="end"
            height={80}
          />
          <YAxis 
            tick={{ fill: '#6b7280', fontSize: 12 }}
            label={{ value: 'Probability (%)', angle: -90, position: 'insideLeft', fill: '#6b7280' }}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#fff', 
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
            }}
            formatter={(value) => [`${value}%`, 'Probability']}
          />
          <Bar dataKey="value" radius={[8, 8, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[entry.name] || '#3b82f6'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      <div className="mt-6 grid grid-cols-2 gap-4">
        {data.map((item) => (
          <div key={item.name} className="flex items-center space-x-3">
            <div 
              className="w-4 h-4 rounded"
              style={{ backgroundColor: colors[item.name] || '#3b82f6' }}
            />
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">{item.name}</p>
              <p className="text-xs text-gray-500">{item.probability}%</p>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  )
}

export default ProbabilityChart
