import React from 'react'

export const LoadingScreen = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="text-center">
        <div className="animate-spin rounded-full h-16 w-16 border-4 border-[#00ade8] border-t-transparent mx-auto"></div>
        <h2 className="mt-6 text-xl font-semibold text-white">n.Gabi</h2>
        <p className="mt-2 text-gray-300">Carregando aplicação...</p>
        <div className="mt-4 flex justify-center space-x-2">
          <div className="w-2 h-2 bg-[#00ade8] rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-[#00ade8] rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-2 h-2 bg-[#00ade8] rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>
      </div>
    </div>
  )
} 