import { Loader2, Bot, Sparkles } from 'lucide-react'

export const LoadingScreen = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <div className="text-center">
        {/* Logo animado */}
        <div className="flex justify-center mb-8">
          <div className="relative">
            <div className="w-20 h-20 bg-[#00ade8] rounded-2xl flex items-center justify-center shadow-lg animate-pulse">
              <Bot className="w-10 h-10 text-white" />
            </div>
            <div className="absolute -top-2 -right-2">
              <Sparkles className="w-6 h-6 text-yellow-400 animate-bounce" />
            </div>
          </div>
        </div>

        {/* Título */}
        <h2 className="text-3xl font-bold text-white mb-4">
          n.Gabi
        </h2>
        <p className="text-lg text-gray-300 mb-8">
          Chat Multi-Agent
        </p>

        {/* Loading spinner */}
        <div className="flex items-center justify-center space-x-2 mb-6">
          <Loader2 className="h-6 w-6 animate-spin text-[#00ade8]" />
          <span className="text-gray-400">Carregando...</span>
        </div>

        {/* Progress dots */}
        <div className="flex justify-center space-x-2">
          <div className="w-2 h-2 bg-[#00ade8] rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-[#00ade8] rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-2 h-2 bg-[#00ade8] rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>

        {/* Status */}
        <p className="text-sm text-gray-500 mt-6">
          Inicializando aplicação...
        </p>
      </div>
    </div>
  )
} 