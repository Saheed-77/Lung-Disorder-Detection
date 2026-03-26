import React from 'react'
import { motion } from 'framer-motion'
import { 
  CheckCircle2, 
  AlertTriangle, 
  Activity,
  TrendingUp
} from 'lucide-react'

const PredictionResult = ({ result }) => {
  const getResultColor = (prediction) => {
    const colors = {
      'Normal': { bg: 'bg-green-50', border: 'border-green-200', text: 'text-green-700', icon: 'text-green-500' },
      'Pneumonia': { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-700', icon: 'text-red-500' },
      'Tuberculosis': { bg: 'bg-orange-50', border: 'border-orange-200', text: 'text-orange-700', icon: 'text-orange-500' },
      'COVID-19': { bg: 'bg-purple-50', border: 'border-purple-200', text: 'text-purple-700', icon: 'text-purple-500' },
      'Inconclusive': { bg: 'bg-slate-50', border: 'border-slate-300', text: 'text-slate-700', icon: 'text-slate-500' },
    }
    return colors[prediction] || colors['Normal']
  }

  const colors = getResultColor(result.prediction)
  const confidence = (result.confidence * 100).toFixed(2)

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className={`card p-8 ${colors.bg} border-2 ${colors.border}`}
    >
      <div className="flex items-start justify-between mb-6">
        <div>
          <p className={`text-sm font-medium ${colors.text} mb-2`}>Diagnosis Result</p>
          <h2 className={`text-4xl font-bold ${colors.text}`}>
            {result.prediction}
          </h2>
        </div>
        <div className={`p-4 rounded-full ${colors.bg}`}>
          {result.prediction === 'Normal' ? (
            <CheckCircle2 className={`w-12 h-12 ${colors.icon}`} />
          ) : (
            <AlertTriangle className={`w-12 h-12 ${colors.icon}`} />
          )}
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className={`text-sm font-medium ${colors.text}`}>Confidence Level</span>
            <span className={`text-2xl font-bold ${colors.text}`}>{confidence}%</span>
          </div>
          <div className="w-full bg-white/50 rounded-full h-4 overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${confidence}%` }}
              transition={{ duration: 1, ease: 'easeOut' }}
              className={`h-full ${
                confidence > 80 ? 'bg-green-500' : 
                confidence > 60 ? 'bg-yellow-500' : 
                'bg-red-500'
              } rounded-full`}
            />
          </div>
          <p className={`text-xs ${colors.text} mt-2`}>
            {confidence > 80 ? 'High confidence - Strong prediction' : 
             confidence > 60 ? 'Moderate confidence - Consider additional testing' : 
             'Low confidence - Further examination recommended'}
          </p>
          {result.prediction === 'Inconclusive' && (
            <p className={`text-xs ${colors.text} mt-2 font-medium`}>
              Prediction marked inconclusive due to low confidence or close class probabilities.
            </p>
          )}
        </div>

        <div className={`border-t-2 ${colors.border} pt-4`}>
          <p className={`text-sm ${colors.text}`}>
            <strong>Interpretation:</strong> The AI model has analyzed the chest X-ray and
            {result.prediction === 'Inconclusive'
              ? ' found no sufficiently reliable single-class prediction. Additional clinical review and testing are recommended.'
              : ` detected patterns consistent with ${result.prediction.toLowerCase()}.`}
            {result.prediction !== 'Normal' && result.prediction !== 'Inconclusive' &&
              ' Please consult with a healthcare professional for proper diagnosis and treatment.'}
          </p>
        </div>
      </div>
    </motion.div>
  )
}

export default PredictionResult
