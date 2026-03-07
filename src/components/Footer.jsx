import React from 'react'
import { Link } from 'react-router-dom'
import { Activity, Mail, Github, Linkedin, AlertTriangle } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1">
            <div className="flex items-center space-x-2 mb-4">
              <div className="bg-gradient-to-br from-primary-500 to-primary-700 p-2 rounded-lg">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-white">LungAI</span>
            </div>
            <p className="text-sm text-gray-400">
              AI-powered lung disorder detection using advanced machine learning technology.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-sm hover:text-primary-400 transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/diagnosis" className="text-sm hover:text-primary-400 transition-colors">
                  Diagnosis
                </Link>
              </li>
              <li>
                <Link to="/chatbot" className="text-sm hover:text-primary-400 transition-colors">
                  AI Assistant
                </Link>
              </li>
            </ul>
          </div>

          {/* Project Info */}
          <div>
            <h3 className="text-white font-semibold mb-4">Research</h3>
            <ul className="space-y-2 text-sm">
              <li className="text-gray-400">MobileNet Architecture</li>
              <li className="text-gray-400">Vision Transformer (ViT)</li>
              <li className="text-gray-400">Hybrid CNN-Transformer</li>
              <li className="text-gray-400">Medical AI Research</li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-white font-semibold mb-4">Contact</h3>
            <ul className="space-y-3">
              <li>
                <a href="mailto:research@lungai.com" className="flex items-center space-x-2 text-sm hover:text-primary-400 transition-colors">
                  <Mail className="w-4 h-4" />
                  <span>research@lungai.com</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center space-x-2 text-sm hover:text-primary-400 transition-colors">
                  <Github className="w-4 h-4" />
                  <span>GitHub</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center space-x-2 text-sm hover:text-primary-400 transition-colors">
                  <Linkedin className="w-4 h-4" />
                  <span>LinkedIn</span>
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Disclaimer */}
        <div className="mt-8 pt-8 border-t border-gray-800">
          <div className="flex items-start space-x-2 bg-yellow-900/20 border border-yellow-700/30 rounded-lg p-4 mb-6">
            <AlertTriangle className="w-5 h-5 text-yellow-500 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm text-yellow-200 font-semibold mb-1">Medical Disclaimer</p>
              <p className="text-xs text-yellow-300/80">
                This tool is for research and educational purposes only. It is NOT intended for actual medical diagnosis. 
                Always consult qualified healthcare professionals for medical advice and diagnosis.
              </p>
            </div>
          </div>
          
          <div className="text-center text-sm text-gray-500">
            <p>© 2026 Lung Disorder Detection Research Project. All rights reserved.</p>
            <p className="mt-1">Built with React, FastAPI, and TensorFlow | Academic Research Prototype</p>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
