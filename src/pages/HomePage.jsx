import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  ArrowRight, 
  Brain, 
  Zap, 
  Shield, 
  Activity,
  Stethoscope,
  Cpu,
  Eye,
  CheckCircle2,
  AlertCircle,
  TrendingUp
} from 'lucide-react'

const HomePage = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  }

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: 'spring',
        stiffness: 100
      }
    }
  }

  const diseases = [
    { name: 'Pneumonia', icon: Activity, color: 'text-red-500', bg: 'bg-red-50' },
    { name: 'Tuberculosis', icon: Stethoscope, color: 'text-orange-500', bg: 'bg-orange-50' },
    { name: 'COVID-19', icon: AlertCircle, color: 'text-purple-500', bg: 'bg-purple-50' },
    { name: 'Normal', icon: CheckCircle2, color: 'text-green-500', bg: 'bg-green-50' },
  ]

  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Diagnosis',
      description: 'Advanced deep learning model trained on thousands of chest X-ray images for accurate detection.',
      color: 'text-blue-500',
      bg: 'bg-blue-50'
    },
    {
      icon: Zap,
      title: 'Fast Prediction',
      description: 'Get results in seconds with our optimized hybrid MobileNet + ViT architecture.',
      color: 'text-yellow-500',
      bg: 'bg-yellow-50'
    },
    {
      icon: TrendingUp,
      title: 'High Confidence Score',
      description: 'Detailed probability analysis and confidence metrics for each prediction.',
      color: 'text-green-500',
      bg: 'bg-green-50'
    },
    {
      icon: Eye,
      title: 'Explainable Results',
      description: 'Visual heatmaps and attention maps showing which regions influenced the diagnosis.',
      color: 'text-purple-500',
      bg: 'bg-purple-50'
    },
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <motion.section 
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="relative bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 text-white overflow-hidden"
      >
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMzLjMxNCAwIDYgMi42ODYgNiA2cy0yLjY4NiA2LTYgNi02LTIuNjg2LTYtNiAyLjY4Ni02IDYtNiIgc3Ryb2tlPSJyZ2JhKDI1NSwgMjU1LCAyNTUsIDAuMSkiIHN0cm9rZS13aWR0aD0iMiIvPjwvZz48L3N2Zz4=')] opacity-10"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div variants={itemVariants} className="space-y-6">
              <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full">
                <Brain className="w-5 h-5" />
                <span className="text-sm font-medium">AI Medical Research Project</span>
              </div>
              
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
                Lung Disorder Detection using{' '}
                <span className="text-primary-200">Hybrid AI</span>
              </h1>
              
              <p className="text-lg md:text-xl text-primary-100">
                Advanced MobileNet + Vision Transformer architecture for detecting pneumonia, 
                tuberculosis, and COVID-19 from chest X-ray images.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <Link 
                  to="/diagnosis"
                  className="inline-flex items-center justify-center px-8 py-4 bg-white text-primary-700 rounded-lg font-semibold hover:bg-primary-50 transition-all duration-200 shadow-xl hover:shadow-2xl active:scale-95"
                >
                  Start Diagnosis
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Link>
                
                <a 
                  href="#about"
                  className="inline-flex items-center justify-center px-8 py-4 bg-transparent border-2 border-white text-white rounded-lg font-semibold hover:bg-white/10 transition-all duration-200 active:scale-95"
                >
                  Learn More
                </a>
              </div>
            </motion.div>

            <motion.div 
              variants={itemVariants}
              className="relative hidden md:block"
            >
              <div className="relative">
                <div className="absolute inset-0 bg-primary-400/30 rounded-2xl blur-3xl"></div>
                <div className="relative bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
                  <div className="grid grid-cols-2 gap-4">
                    {diseases.map((disease, index) => (
                      <motion.div
                        key={disease.name}
                        initial={{ scale: 0, rotate: -180 }}
                        animate={{ scale: 1, rotate: 0 }}
                        transition={{ delay: 0.5 + index * 0.1, type: 'spring' }}
                        className="bg-white rounded-xl p-4 text-center"
                      >
                        <disease.icon className={`w-8 h-8 ${disease.color} mx-auto mb-2`} />
                        <p className="text-sm font-semibold text-gray-800">{disease.name}</p>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </motion.section>

      {/* About Section */}
      <section id="about" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              About the Project
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              An innovative AI system combining CNN and Transformer architectures for 
              accurate lung disorder detection.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="card p-8"
            >
              <div className="bg-red-50 w-16 h-16 rounded-full flex items-center justify-center mb-6">
                <AlertCircle className="w-8 h-8 text-red-500" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Problem Statement</h3>
              <p className="text-gray-600">
                Lung disorders are among the leading causes of death globally. Early and accurate 
                detection is crucial for effective treatment and improved patient outcomes.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="card p-8"
            >
              <div className="bg-blue-50 w-16 h-16 rounded-full flex items-center justify-center mb-6">
                <Brain className="w-8 h-8 text-blue-500" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Our Solution</h3>
              <p className="text-gray-600">
                A hybrid deep learning model that leverages both convolutional neural networks 
                for feature extraction and transformers for global attention mechanisms.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
              className="card p-8"
            >
              <div className="bg-green-50 w-16 h-16 rounded-full flex items-center justify-center mb-6">
                <CheckCircle2 className="w-8 h-8 text-green-500" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Impact</h3>
              <p className="text-gray-600">
                Enabling faster screening, reducing diagnostic time, and providing healthcare 
                professionals with a powerful AI-assisted diagnostic tool.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Model Architecture */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Hybrid Model Architecture
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Combining the efficiency of MobileNet with the power of Vision Transformers
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="space-y-6"
            >
              <div className="flex items-start space-x-4">
                <div className="bg-primary-100 p-3 rounded-lg flex-shrink-0">
                  <Cpu className="w-6 h-6 text-primary-600" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">MobileNet CNN</h3>
                  <p className="text-gray-600">
                    Lightweight convolutional neural network for efficient feature extraction 
                    from X-ray images. Optimized for mobile and edge deployment.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="bg-purple-100 p-3 rounded-lg flex-shrink-0">
                  <Eye className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Vision Transformer</h3>
                  <p className="text-gray-600">
                    Self-attention mechanism to capture global context and long-range dependencies 
                    in medical images for improved diagnostic accuracy.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="bg-green-100 p-3 rounded-lg flex-shrink-0">
                  <Shield className="w-6 h-6 text-green-600" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Hybrid Fusion</h3>
                  <p className="text-gray-600">
                    Combines local features from CNN with global attention from transformers, 
                    achieving superior performance compared to individual architectures.
                  </p>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="card p-8 bg-white"
            >
              <div className="space-y-4">
                <div className="text-center py-4 bg-primary-50 rounded-lg border-2 border-primary-200">
                  <p className="text-sm font-medium text-primary-700">Input X-Ray Image</p>
                </div>
                <div className="flex items-center justify-center">
                  <div className="h-8 w-1 bg-gradient-to-b from-primary-500 to-purple-500"></div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center py-4 bg-blue-50 rounded-lg border border-blue-200">
                    <p className="text-sm font-medium text-blue-700">MobileNet</p>
                    <p className="text-xs text-blue-600 mt-1">Feature Extraction</p>
                  </div>
                  <div className="text-center py-4 bg-purple-50 rounded-lg border border-purple-200">
                    <p className="text-sm font-medium text-purple-700">ViT</p>
                    <p className="text-xs text-purple-600 mt-1">Global Attention</p>
                  </div>
                </div>
                <div className="flex items-center justify-center">
                  <div className="h-8 w-1 bg-gradient-to-b from-purple-500 to-green-500"></div>
                </div>
                <div className="text-center py-4 bg-green-50 rounded-lg border-2 border-green-200">
                  <p className="text-sm font-medium text-green-700">Fusion Layer</p>
                </div>
                <div className="flex items-center justify-center">
                  <div className="h-8 w-1 bg-gradient-to-b from-green-500 to-red-500"></div>
                </div>
                <div className="text-center py-4 bg-gradient-to-br from-primary-500 to-primary-600 text-white rounded-lg">
                  <p className="text-sm font-semibold">Classification Output</p>
                  <p className="text-xs mt-1">4 Classes + Confidence</p>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Supported Diseases */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Detectable Conditions
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our model is trained to identify four key lung conditions
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {diseases.map((disease, index) => (
              <motion.div
                key={disease.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -8, transition: { duration: 0.2 } }}
                className="card p-6 text-center cursor-pointer"
              >
                <div className={`${disease.bg} w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4`}>
                  <disease.icon className={`w-10 h-10 ${disease.color}`} />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{disease.name}</h3>
                <p className="text-sm text-gray-600">
                  {disease.name === 'Pneumonia' && 'Infection causing lung inflammation'}
                  {disease.name === 'Tuberculosis' && 'Bacterial infection affecting lungs'}
                  {disease.name === 'COVID-19' && 'Viral respiratory disease'}
                  {disease.name === 'Normal' && 'Healthy lung tissue'}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 bg-gradient-to-br from-primary-600 to-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Powerful Features
            </h2>
            <p className="text-xl text-primary-100 max-w-3xl mx-auto">
              Advanced capabilities for accurate and reliable diagnosis
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 hover:bg-white/20 transition-all duration-300"
              >
                <div className="bg-white/20 w-14 h-14 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="text-lg font-bold mb-2">{feature.title}</h3>
                <p className="text-sm text-primary-100">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="space-y-8"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900">
              Ready to Try Our AI Diagnostic System?
            </h2>
            <p className="text-xl text-gray-600">
              Upload a chest X-ray image and get instant AI-powered analysis
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                to="/diagnosis"
                className="btn-primary inline-flex items-center justify-center"
              >
                Start Free Diagnosis
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
              <Link 
                to="/chatbot"
                className="btn-secondary inline-flex items-center justify-center"
              >
                <Brain className="mr-2 w-5 h-5" />
                Ask AI Assistant
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
