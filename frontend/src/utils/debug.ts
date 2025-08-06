// Utilitário de debug para capturar erros
export const setupErrorHandling = () => {
  // Capturar erros não tratados
  window.addEventListener('error', (event) => {
    console.error('Erro capturado:', event.error)
    console.error('Detalhes:', {
      message: event.message,
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno
    })
  })

  // Capturar promessas rejeitadas
  window.addEventListener('unhandledrejection', (event) => {
    console.error('Promessa rejeitada:', event.reason)
  })

  // Capturar erros de carregamento de recursos
  window.addEventListener('load', () => {
    console.log('Página carregada completamente')
  })

  // Log de inicialização
  console.log('Debug inicializado')
}

// Função para verificar se todos os componentes estão carregados
export const checkComponents = () => {
  const checks = {
    router: typeof window !== 'undefined' && 'history' in window,
    supabase: typeof window !== 'undefined' && 'supabase' in window
  }

  console.log('Verificação de componentes:', checks)
  return checks
} 