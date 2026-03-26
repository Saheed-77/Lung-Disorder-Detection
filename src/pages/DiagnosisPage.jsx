import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Upload, 
  X, 
  FileImage, 
  Loader2,
  CheckCircle2,
  AlertCircle,
  Download,
  RotateCcw,
  Activity,
  TrendingUp,
  Clock
} from 'lucide-react'
import toast from 'react-hot-toast'
import axios from 'axios'
import PredictionResult from '../components/PredictionResult'
import ProbabilityChart from '../components/ProbabilityChart'

const DiagnosisPage = () => {
  const [selectedFile, setSelectedFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0]
    
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        toast.error('Please upload a valid image file')
        return
      }

      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        toast.error('File size must be less than 10MB')
        return
      }

      setSelectedFile(file)
      setResult(null)

      // Create preview
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result)
      }
      reader.readAsDataURL(file)

      toast.success('Image uploaded successfully')
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.dcm']
    },
    multiple: false
  })

  const handlePredict = async () => {
    if (!selectedFile) {
      toast.error('Please upload an X-ray image first')
      return
    }

    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const response = await axios.post('/api/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      console.log('Prediction response:', response.data)
      console.log('Grad-CAM available:', !!response.data.gradcam)
      
      setResult(response.data)
      toast.success('Prediction completed!')
    } catch (error) {
      console.error('Prediction error:', error)
      toast.error(error.response?.data?.detail || 'Failed to process image. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setSelectedFile(null)
    setPreview(null)
    setResult(null)
  }

  const handleDownloadReport = () => {
    if (!result) return

    const reportData = {
      prediction: result.prediction,
      confidence: result.confidence,
      timestamp: new Date().toLocaleString(),
      probabilities: result.probabilities
    }

    const dataStr = JSON.stringify(reportData, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `diagnosis_report_${Date.now()}.json`
    link.click()

    toast.success('Report downloaded!')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center space-x-2 bg-primary-100 text-primary-700 px-4 py-2 rounded-full mb-4">
            <Activity className="w-5 h-5" />
            <span className="text-sm font-semibold">AI Diagnosis System</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Chest X-Ray Analysis
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Upload a chest X-ray image and get instant AI-powered diagnosis using our hybrid MobileNet + ViT model
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <div className="card p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Upload X-Ray Image</h2>

              {!preview ? (
                <div
                  {...getRootProps()}
                  className={`border-3 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-300 ${
                    isDragActive
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
                  }`}
                >
                  <input {...getInputProps()} />
                  <div className="flex flex-col items-center space-y-4">
                    <div className="bg-primary-100 p-6 rounded-full">
                      <Upload className="w-12 h-12 text-primary-600" />
                    </div>
                    <div>
                      <p className="text-lg font-semibold text-gray-900 mb-2">
                        {isDragActive ? 'Drop your X-ray here' : 'Drag & drop your X-ray'}
                      </p>
                      <p className="text-sm text-gray-500">
                        or click to browse files
                      </p>
                    </div>
                    <div className="text-xs text-gray-400">
                      Supported: PNG, JPG, JPEG, DICOM • Max size: 10MB
                    </div>
                  </div>
                </div>
              ) : (
                <div className="space-y-6">
                  <div className="relative group">
                    <img
                      src={preview}
                      alt="X-ray preview"
                      className="w-full rounded-xl shadow-lg"
                    />
                    <button
                      onClick={() => {
                        setPreview(null)
                        setSelectedFile(null)
                        setResult(null)
                      }}
                      className="absolute top-4 right-4 bg-red-500 text-white p-2 rounded-full hover:bg-red-600 transition-colors opacity-0 group-hover:opacity-100"
                    >
                      <X className="w-5 h-5" />
                    </button>
                    <div className="absolute bottom-4 left-4 bg-black/70 backdrop-blur-sm text-white px-4 py-2 rounded-lg">
                      <div className="flex items-center space-x-2">
                        <FileImage className="w-4 h-4" />
                        <span className="text-sm font-medium">{selectedFile?.name}</span>
                      </div>
                      <div className="text-xs text-gray-300 mt-1">
                        {(selectedFile?.size / 1024 / 1024).toFixed(2)} MB
                      </div>
                    </div>
                  </div>

                  <div className="flex gap-4">
                    <button
                      onClick={handlePredict}
                      disabled={loading}
                      className="flex-1 btn-primary flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {loading ? (
                        <>
                          <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <Activity className="w-5 h-5 mr-2" />
                          Analyze X-Ray
                        </>
                      )}
                    </button>

                    <button
                      onClick={handleReset}
                      disabled={loading}
                      className="btn-secondary flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <RotateCcw className="w-5 h-5" />
                    </button>
                  </div>

                  {result && (
                    <button
                      onClick={handleDownloadReport}
                      className="w-full py-3 px-6 border-2 border-primary-600 text-primary-600 rounded-lg font-semibold hover:bg-primary-50 transition-colors flex items-center justify-center"
                    >
                      <Download className="w-5 h-5 mr-2" />
                      Download Report
                    </button>
                  )}
                </div>
              )}
            </div>

            {/* Instructions */}
            <div className="card p-6 mt-6 bg-blue-50 border border-blue-200">
              <h3 className="font-semibold text-blue-900 mb-3 flex items-center">
                <AlertCircle className="w-5 h-5 mr-2" />
                Important Guidelines
              </h3>
              <ul className="space-y-2 text-sm text-blue-800">
                <li className="flex items-start">
                  <CheckCircle2 className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
                  <span>Upload clear, frontal chest X-ray images</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
                  <span>Ensure good image quality and proper exposure</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
                  <span>Supported formats: PNG, JPG, JPEG, DICOM</span>
                </li>
                <li className="flex items-start">
                  <AlertCircle className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0 text-yellow-600" />
                  <span className="font-semibold">This is NOT a replacement for professional medical diagnosis</span>
                </li>
              </ul>
            </div>
          </motion.div>

          {/* Results Section */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <AnimatePresence mode="wait">
              {loading ? (
                <motion.div
                  key="loading"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="card p-12 flex flex-col items-center justify-center"
                >
                  <div className="loader mb-6"></div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Analyzing X-Ray...</h3>
                  <p className="text-gray-600 text-center">
                    Our AI model is processing your image using hybrid MobileNet + ViT architecture
                  </p>
                  <div className="mt-8 w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                    <motion.div
                      className="h-full bg-primary-600"
                      initial={{ width: '0%' }}
                      animate={{ width: '100%' }}
                      transition={{ duration: 3, ease: 'easeInOut' }}
                    />
                  </div>
                </motion.div>
              ) : result ? (
                <motion.div
                  key="result"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="space-y-6"
                >
                  <PredictionResult result={result} />
                  
                  {/* Grad-CAM Heatmap Visualization */}
                  {result.gradcam && (
                    <div className="card p-6">
                      <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                        <Activity className="w-5 h-5 mr-2 text-primary-600" />
                        AI Focus Areas (Grad-CAM Visualization)
                      </h3>
                      <p className="text-sm text-gray-600 mb-4">
                        The heatmap below highlights the regions in the X-ray that the AI model focused on to make its prediction. 
                        Red/yellow areas indicate high attention, while blue/purple areas show less focus.
                      </p>
                      
                      <div className="grid md:grid-cols-2 gap-4">
                        {/* Original Image */}
                        <div className="space-y-2">
                          <p className="text-sm font-semibold text-gray-700">Original X-Ray</p>
                          <div className="relative rounded-lg overflow-hidden border-2 border-gray-200">
                            <img
                              src={preview}
                              alt="Original X-ray"
                              className="w-full h-auto"
                            />
                          </div>
                        </div>
                        
                        {/* Heatmap Overlay */}
                        <div className="space-y-2">
                          <p className="text-sm font-semibold text-gray-700">AI Attention Heatmap</p>
                          <div className="relative rounded-lg overflow-hidden border-2 border-primary-300">
                            <img
                              src={result.gradcam}
                              alt="Grad-CAM Heatmap"
                              className="w-full h-auto"
                            />
                          </div>
                        </div>
                      </div>
                      
                      {/* Heatmap Legend */}
                      <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                        <p className="text-xs font-semibold text-gray-700 mb-2">Heatmap Legend:</p>
                        <div className="flex items-center space-x-4 text-xs text-gray-600">
                          <div className="flex items-center space-x-1">
                            <div className="w-4 h-4 bg-red-500 rounded"></div>
                            <span>High attention</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <div className="w-4 h-4 bg-yellow-500 rounded"></div>
                            <span>Medium attention</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <div className="w-4 h-4 bg-blue-500 rounded"></div>
                            <span>Low attention</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                  
                  <ProbabilityChart probabilities={result.probabilities} />
                  
                  {/* Additional Info */}
                  <div className="card p-6">
                    <h3 className="text-lg font-bold text-gray-900 mb-4">Analysis Details</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <div className="flex items-center space-x-2 text-gray-600 mb-1">
                          <Clock className="w-4 h-4" />
                          <span className="text-sm">Processing Time</span>
                        </div>
                        <p className="text-xl font-bold text-gray-900">
                          {result.inference_time || '0.8'}s
                        </p>
                      </div>
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <div className="flex items-center space-x-2 text-gray-600 mb-1">
                          <TrendingUp className="w-4 h-4" />
                          <span className="text-sm">Prediction Reliability</span>
                        </div>
                        <p className="text-xl font-bold text-gray-900">
                          {((result.confidence || 0) * 100).toFixed(2)}%
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                          {result.is_reliable_prediction ? 'Reliable prediction' : 'Low reliability / inconclusive'}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Recommendations */}
                  <div className="card p-6 bg-yellow-50 border border-yellow-200">
                    <h3 className="font-semibold text-yellow-900 mb-3 flex items-center">
                      <AlertCircle className="w-5 h-5 mr-2" />
                      Next Steps
                    </h3>
                    <ul className="space-y-2 text-sm text-yellow-800">
                      <li>• Consult with a qualified healthcare professional</li>
                      <li>• Share these results with your doctor</li>
                      <li>• Do not use this as a final diagnosis</li>
                      <li>• Follow up with proper medical testing if needed</li>
                    </ul>
                  </div>
                </motion.div>
              ) : (
                <motion.div
                  key="empty"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="card p-12 flex flex-col items-center justify-center text-center"
                >
                  <div className="bg-gray-100 p-8 rounded-full mb-6">
                    <FileImage className="w-16 h-16 text-gray-400" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">No Analysis Yet</h3>
                  <p className="text-gray-600">
                    Upload an X-ray image to get started with AI-powered diagnosis
                  </p>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default DiagnosisPage
