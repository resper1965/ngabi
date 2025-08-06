import React from 'react'

export const TestComponent = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-white mb-4">
          Teste de Carregamento
        </h1>
        <p className="text-gray-300 mb-4">
          Se você está vendo esta tela, o React está funcionando corretamente.
        </p>
        <div className="bg-[#00ade8] text-white px-6 py-3 rounded-lg">
          Componente de Teste Funcionando
        </div>
      </div>
    </div>
  )
} 