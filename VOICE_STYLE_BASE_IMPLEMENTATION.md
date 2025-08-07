# 🎨 Base Vetorial de Estilo de Voz por Organização - n.Gabi

## 📋 **Visão Geral**

A **Base Vetorial de Estilo de Voz por Organização** é uma funcionalidade especial que garante consistência na comunicação de cada organização/tenant. Ela funciona como uma base RAG separada que é automaticamente integrada ao chat final para prover características de estilo, tom de voz e personalidade específicas de cada organização.

## 🎯 **Características Principais**

### **Badge Especial**
- **🎨 Estilo de Voz** - Badge único para identificar o especialista
- **Integração Automática** - Aplicada automaticamente em todas as respostas
- **Base Separada por Organização** - Armazenada independentemente no Supabase por tenant
- **Personalização por Organização** - Cada organização tem seu próprio tom de voz

### **Funcionalidades**
- ✅ **Tom de voz personalizado** por organização
- ✅ **Personalidade da organização** mantida
- ✅ **Adaptação contextual** por situação
- ✅ **Integração automática** com outros especialistas
- ✅ **Armazenamento vetorial** no Supabase por tenant
- ✅ **Multi-tenancy** completo

## 🏗️ **Arquitetura**

### **Componentes Principais**

#### **1. VoiceStyleBase (`backend/app/core/voice_style_base.py`)**
```python
class VoiceStyleBase:
    VOICE_STYLE_SPECIALIST_ID = "voice-style-brand"
    
    # Documentos base de estilo personalizados por organização
    # Especialista de estilo de voz por tenant
    # Badge e identificação
    # Prompt de integração personalizado
```

#### **2. LangChainService Integration**
```python
async def _apply_voice_style(self, response: str, specialist_id: str, tenant_id: str) -> str:
    # Aplica estilo da organização automaticamente
    # Mantém conteúdo técnico
    # Garante consistência da organização
```

#### **3. Supabase Vector Store por Tenant**
```python
# Armazenamento separado por organização
specialist_id: "voice-style-brand"
tenant_id: "minha-empresa"  # Cada organização tem seu tenant
# Documentos vetorizados de estilo por organização
```

## 📚 **Documentos Base de Estilo por Organização**

### **1. Personalidade da Organização**
```
TOM DE VOZ DA ORGANIZAÇÃO MINHA EMPRESA:
- Amigável e acolhedora, mas profissional
- Confiável e transparente
- Inovadora e orientada a soluções
- Empática e atenta às necessidades
```

### **2. Diretrizes de Linguagem**
```
PRONOMES E TRATAMENTO:
- Use "você" para criar proximidade
- Evite "senhor/senhora"
- Use "nós" quando se referir à empresa
```

### **3. Situações Específicas**
```
SAUDAÇÕES:
- "Olá! Como posso ajudar você hoje?"
- "Oi! Que bom ter você por aqui!"

RESPOSTAS POSITIVAS:
- "Perfeito! Vou te ajudar com isso."
- "Ótimo! Aqui está a solução..."
```

## 🔧 **Endpoints Disponíveis**

### **Inicialização e Configuração por Organização**
```bash
# Inicializar base de estilo de voz para uma organização
POST /api/v1/agents/voice-style/initialize
{
    "organization_name": "Minha Empresa",
    "tenant_id": "minha-empresa"
}

# Obter especialista de estilo de voz da organização
GET /api/v1/agents/voice-style/specialist?organization_name=Minha Empresa

# Obter documentos de estilo da organização
GET /api/v1/agents/voice-style/documents?tenant_id=minha-empresa

# Testar integração da organização
POST /api/v1/agents/voice-style/test
{
    "test_message": "Olá, como posso ajudar?",
    "organization_name": "Minha Empresa",
    "tenant_id": "minha-empresa"
}
```

### **Integração Automática por Tenant**
```bash
# Testar qualquer agente (estilo da organização aplicado automaticamente)
POST /api/v1/agents/{agent_id}/test?tenant_id=minha-empresa

# Resposta inclui:
{
    "badge": "🎨 Estilo de Voz",
    "tenant_id": "minha-empresa",
    "voice_style_applied": true,
    "response": "Resposta com estilo da organização..."
}
```

## 🚀 **Como Funciona**

### **1. Inicialização por Organização**
```python
# 1. Criar base vetorial personalizada
voice_documents = VoiceStyleBase.get_voice_style_documents("Minha Empresa")

# 2. Armazenar no Supabase com tenant específico
await supabase_vectorstore.store_documents_for_specialist(
    specialist_id="voice-style-brand",
    tenant_id="minha-empresa",
    documents=voice_documents
)
```

### **2. Integração Automática por Tenant**
```python
# 1. Processar com especialista
response = await langchain_service.process_with_specialist_chain(
    specialist_id="customer-support",
    message="Como posso ajudar?",
    tenant_id="minha-empresa"
)

# 2. Aplicar estilo da organização automaticamente
adjusted_response = await langchain_service._apply_voice_style(
    response, "customer-support", "minha-empresa"
)
```

### **3. Resultado Final Personalizado**
```
RESPOSTA ORIGINAL:
"Para resolver seu problema, siga estes passos..."

RESPOSTA COM ESTILO DA ORGANIZAÇÃO:
"Olá! Que bom ter você por aqui! 😊 Para resolver seu problema, vou te guiar pelos passos necessários. Vamos lá?"
```

## 🎨 **Badge e Identificação por Organização**

### **Badge Especial**
- **🎨 Estilo de Voz** - Identifica o especialista único
- **Auto-integração** - Aplicado automaticamente por tenant
- **Prioridade crítica** - Sempre ativo por organização

### **Metadados Especiais**
```python
metadata = {
    "special_type": "voice_style",
    "is_organization_voice": True,
    "priority": "critical",
    "auto_integrate": True,
    "badge": "🎨 Estilo de Voz",
    "organization_name": "Minha Empresa"
}
```

## 📊 **Benefícios**

### **Para a Organização**
- ✅ **Consistência** em todas as comunicações
- ✅ **Identidade** da organização mantida
- ✅ **Experiência** do usuário uniforme
- ✅ **Profissionalismo** com proximidade

### **Para o Desenvolvimento**
- ✅ **Reutilização** em todos os agentes
- ✅ **Manutenibilidade** centralizada
- ✅ **Escalabilidade** automática
- ✅ **Flexibilidade** de ajustes por tenant

### **Para o Usuário**
- ✅ **Experiência** consistente
- ✅ **Confiança** na organização
- ✅ **Clareza** na comunicação
- ✅ **Proximidade** mantida

## 🔄 **Fluxo de Integração por Tenant**

```
1. Usuário envia mensagem (tenant_id: "minha-empresa")
    ↓
2. Especialista processa (ex: customer-support)
    ↓
3. LangChain gera resposta técnica
    ↓
4. VoiceStyleBase aplica estilo da "minha-empresa" automaticamente
    ↓
5. Resposta final com tom da organização
```

## 🛠️ **Configuração por Organização**

### **1. Inicializar Base para Organização**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/voice-style/initialize" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_name": "Minha Empresa",
    "tenant_id": "minha-empresa"
  }'
```

### **2. Testar Integração da Organização**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/voice-style/test" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "test_message": "Olá, como posso ajudar?",
    "organization_name": "Minha Empresa",
    "tenant_id": "minha-empresa"
  }'
```

### **3. Testar com Outro Especialista da Organização**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/specialists/customer-support/langchain" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "test_message": "Tenho um problema técnico",
    "tenant_id": "minha-empresa"
  }'
```

## 🎯 **Resultado Esperado**

A base vetorial de estilo de voz garante que **todas as respostas** de cada organização mantenham:

- 🎨 **Tom amigável e acolhedor** da organização
- 💼 **Profissionalismo sem formalidade** da empresa
- 🎯 **Clareza e objetividade** da marca
- ❤️ **Empatia e compreensão** da cultura
- 🚀 **Consistência** da identidade organizacional

**A base está separada por organização, tem badge especial e participa automaticamente do chat final para prover as características de estilo específicas de cada organização!** 🎉

---

*Implementação concluída - Base vetorial de estilo de voz por organização integrada e funcional* 