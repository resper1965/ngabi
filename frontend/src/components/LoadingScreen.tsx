import { Loader2 } from 'lucide-react'

export const LoadingScreen = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="text-center">
        <Loader2 className="h-12 w-12 animate-spin text-[#00ade8] mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-white mb-2">Carregando...</h2>
        <p className="text-gray-400">Inicializando n.Gabi</p>
      </div>
    </div>
  )
} 