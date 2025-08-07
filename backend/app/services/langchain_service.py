"""
LangChain Service - n.Gabi
Orquestração avançada de LLMs para agentes especialistas
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.memory import ConversationBufferMemory
from langchain_core.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun

from app.core.config import settings
from app.core.agent_specialists import AgentSpecialists
from app.core.voice_style_base import VoiceStyleBase
from app.services.supabase_retriever import SupabaseRetriever

logger = logging.getLogger(__name__)

class LangChainService:
    """Serviço principal do LangChain para agentes especialistas."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            streaming=True,
            openai_api_key=settings.openai_api_key
        )
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.openai_api_key
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.chains = {}
        self.memories = {}
        self.vectorstores = {}
        self.tools = {}
        self._initialize_default_tools()
    
    def _initialize_default_tools(self):
        """Inicializar ferramentas padrão."""
        self.tools["search"] = DuckDuckGoSearchRun()
        # Adicionar mais ferramentas conforme necessário
    
    async def create_specialist_chain(self, specialist_id: str) -> Dict[str, Any]:
        """Criar chain especializada para um agente especialista."""
        try:
            # Obter dados do especialista
            specialist = AgentSpecialists.get_specialist_by_id(specialist_id)
            if not specialist:
                raise ValueError(f"Especialista não encontrado: {specialist_id}")
            
            # Criar prompt especializado
            prompt = self._create_specialist_prompt(specialist)
            
            # Criar chain básica
            basic_chain = prompt | self.llm | StrOutputParser()
            
            # Adicionar memory se necessário
            memory_key = f"memory_{specialist_id}"
            if memory_key not in self.memories:
                self.memories[memory_key] = ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True
                )
            
            # Criar chain com memory
            chain_with_memory = (
                {"chat_history": self.memories[memory_key], "input": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
            )
            
            # Salvar chain
            self.chains[specialist_id] = {
                "basic_chain": basic_chain,
                "chain_with_memory": chain_with_memory,
                "specialist": specialist,
                "created_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"✅ Chain criada para especialista: {specialist_id}")
            return self.chains[specialist_id]
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar chain para especialista {specialist_id}: {e}")
            raise
    
    def _create_specialist_prompt(self, specialist: Dict[str, Any]) -> ChatPromptTemplate:
        """Criar prompt especializado baseado no especialista."""
        category = specialist.get("category", "general")
        
        if category == "vendas":
            return ChatPromptTemplate.from_template("""
            Você é um especialista em vendas com experiência em B2B e B2C.
            
            TÉCNICAS DE VENDAS:
            - SPIN Selling (Situação, Problema, Implicação, Necessidade)
            - Consultative Selling
            - Objection Handling
            - Value Proposition
            - Closing Techniques
            
            PROCESSO:
            1. Qualificação do lead
            2. Descoberta de necessidades
            3. Apresentação de valor
            4. Tratamento de objeções
            5. Fechamento
            
            HISTÓRICO: {chat_history}
            PERGUNTA: {input}
            
            Responda como um especialista em vendas experiente.
            """)
        
        elif category == "tecnico":
            return ChatPromptTemplate.from_template("""
            Você é um especialista técnico com vasto conhecimento em tecnologia.
            
            ÁREAS DE EXPERTISE:
            - Desenvolvimento de software
            - Infraestrutura de TI
            - Cloud Computing
            - Segurança da informação
            - DevOps e CI/CD
            
            METODOLOGIA:
            1. Diagnóstico preciso do problema
            2. Análise de logs e erros
            3. Solução passo a passo
            4. Prevenção de problemas futuros
            5. Documentação técnica
            
            HISTÓRICO: {chat_history}
            PERGUNTA: {input}
            
            Responda como um especialista técnico experiente.
            """)
        
        elif category == "marketing":
            return ChatPromptTemplate.from_template("""
            Você é um especialista em marketing digital com experiência em múltiplas estratégias.
            
            ESTRATÉGIAS DE MARKETING:
            - Marketing de Conteúdo
            - SEO e SEM
            - Marketing de Redes Sociais
            - Email Marketing
            - Marketing de Performance
            - Branding
            
            FERRAMENTAS:
            - Google Analytics
            - Facebook Ads
            - Google Ads
            - HubSpot
            - Mailchimp
            
            HISTÓRICO: {chat_history}
            PERGUNTA: {input}
            
            Responda como um especialista em marketing digital experiente.
            """)
        
        elif category == "financeiro":
            return ChatPromptTemplate.from_template("""
            Você é um especialista financeiro com conhecimento em investimentos e planejamento.
            
            ÁREAS DE EXPERTISE:
            - Análise de investimentos
            - Planejamento financeiro
            - Gestão de risco
            - Mercado financeiro
            - Finanças pessoais
            
            PRINCÍPIOS:
            - Diversificação de investimentos
            - Análise de risco vs retorno
            - Planejamento de longo prazo
            - Educação financeira
            
            HISTÓRICO: {chat_history}
            PERGUNTA: {input}
            
            Responda como um especialista financeiro experiente.
            """)
        
        elif category == "rh":
            return ChatPromptTemplate.from_template("""
            Você é um especialista em Recursos Humanos com experiência em gestão de pessoas.
            
            ÁREAS DE EXPERTISE:
            - Recrutamento e seleção
            - Gestão de performance
            - Desenvolvimento organizacional
            - Compliance trabalhista
            - Cultura organizacional
            
            PROCESSOS:
            - Análise de perfis
            - Entrevistas estruturadas
            - Avaliação de competências
            - Planejamento de carreira
            - Gestão de conflitos
            
            HISTÓRICO: {chat_history}
            PERGUNTA: {input}
            
            Responda como um especialista em RH experiente.
            """)
        
        elif category == "juridico":
            return ChatPromptTemplate.from_template("""
            Você é um especialista jurídico com conhecimento em diversas áreas do direito.
            
            ÁREAS DE EXPERTISE:
            - Direito Civil
            - Direito Trabalhista
            - Direito Empresarial
            - Direito Tributário
            - Direito Digital
            
            PRINCÍPIOS:
            - Análise cuidadosa de casos
            - Interpretação de legislação
            - Orientação sobre procedimentos
            - Prevenção de riscos legais
            
            AVISO IMPORTANTE:
            Este agente fornece orientações gerais. Para casos específicos, consulte um advogado.
            
            HISTÓRICO: {chat_history}
            PERGUNTA: {input}
            
            Responda como um especialista jurídico experiente.
            """)
        
        elif category == "saude":
            return ChatPromptTemplate.from_template("""
            Você é um especialista em saúde com conhecimento em medicina preventiva e bem-estar.
            
            ÁREAS DE EXPERTISE:
            - Medicina preventiva
            - Nutrição e alimentação
            - Exercícios físicos
            - Saúde mental
            - Primeiros socorros
            
            PRINCÍPIOS:
            - Prevenção é melhor que cura
            - Estilo de vida saudável
            - Orientação baseada em evidências
            - Encaminhamento quando necessário
            
            AVISO IMPORTANTE:
            Este agente fornece orientações gerais. Para problemas específicos, consulte um médico.
            
            HISTÓRICO: {chat_history}
            PERGUNTA: {input}
            
            Responda como um especialista em saúde experiente.
            """)
        
        else:  # atendimento ou geral
            return ChatPromptTemplate.from_template("""
            Você é um especialista em atendimento ao cliente com vasta experiência em resolução de problemas.
            
            DIRETRIZES:
            - Sempre seja cordial, profissional e empático
            - Identifique rapidamente o problema do cliente
            - Ofereça soluções práticas e eficazes
            - Mantenha o cliente informado sobre o progresso
            - Seja proativo em antecipar necessidades
            
            CAPACIDADES:
            - Análise de problemas complexos
            - Escalação quando necessário
            - Documentação de casos
            - Follow-up com clientes
            
            HISTÓRICO: {chat_history}
            PERGUNTA: {input}
            
            Responda como um especialista em atendimento experiente.
            """)
    
    async def process_with_specialist_chain(
        self,
        specialist_id: str,
        message: str,
        use_memory: bool = True,
        tenant_id: str = None
    ) -> str:
        """Processar mensagem com chain especializada."""
        try:
            # Verificar se chain existe
            if specialist_id not in self.chains:
                await self.create_specialist_chain(specialist_id)
            
            chain_data = self.chains[specialist_id]
            
            # Escolher chain (com ou sem memory)
            if use_memory:
                chain = chain_data["chain_with_memory"]
            else:
                chain = chain_data["basic_chain"]
            
            # Processar mensagem
            response = await chain.ainvoke({"input": message})
            
            # Integrar estilo de voz automaticamente
            response = await self._apply_voice_style(response, specialist_id, tenant_id)
            
            logger.info(f"✅ Mensagem processada com especialista {specialist_id}")
            return response
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar com especialista {specialist_id}: {e}")
            raise
    
    async def create_rag_chain(
        self,
        specialist_id: str,
        documents: List[Dict[str, Any]],
        tenant_id: str
    ) -> Dict[str, Any]:
        """Criar chain RAG para especialista com documentos no Supabase."""
        try:
            # Armazenar documentos no Supabase
            from app.services.supabase_vectorstore import supabase_vectorstore
            
            storage_result = await supabase_vectorstore.store_documents_for_specialist(
                specialist_id=specialist_id,
                tenant_id=tenant_id,
                documents=documents
            )
            
            # Criar chain RAG que usa Supabase
            specialist = AgentSpecialists.get_specialist_by_id(specialist_id)
            prompt = self._create_specialist_prompt(specialist)
            
            # Criar retriever customizado para Supabase
            supabase_retriever = SupabaseRetriever(
                supabase_vectorstore=supabase_vectorstore,
                specialist_id=specialist_id,
                tenant_id=tenant_id
            )
            
            rag_chain = (
                {"context": supabase_retriever, "input": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
            )
            
            # Salvar chain RAG
            rag_key = f"rag_{specialist_id}_{tenant_id}"
            self.chains[rag_key] = {
                "rag_chain": rag_chain,
                "specialist": specialist,
                "tenant_id": tenant_id,
                "supabase_storage": storage_result,
                "created_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"✅ Chain RAG criada para especialista {specialist_id} com Supabase")
            return self.chains[rag_key]
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar chain RAG para {specialist_id}: {e}")
            raise
    
    async def process_with_rag_chain(
        self,
        specialist_id: str,
        message: str,
        tenant_id: str
    ) -> str:
        """Processar mensagem com chain RAG."""
        try:
            rag_key = f"rag_{specialist_id}_{tenant_id}"
            
            # Verificar se chain RAG existe
            if rag_key not in self.chains:
                raise ValueError(f"Chain RAG não encontrada para {specialist_id}")
            
            chain_data = self.chains[rag_key]
            chain = chain_data["rag_chain"]
            
            # Processar mensagem
            response = await chain.ainvoke({"input": message})
            
            logger.info(f"✅ Mensagem processada com RAG para especialista {specialist_id}")
            return response
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar com RAG para {specialist_id}: {e}")
            raise
    
    def get_available_chains(self) -> List[str]:
        """Obter lista de chains disponíveis."""
        return list(self.chains.keys())
    
    def get_chain_info(self, chain_id: str) -> Optional[Dict[str, Any]]:
        """Obter informações de uma chain específica."""
        if chain_id in self.chains:
            chain_data = self.chains[chain_id].copy()
            # Remover objetos não serializáveis
            if "basic_chain" in chain_data:
                del chain_data["basic_chain"]
            if "chain_with_memory" in chain_data:
                del chain_data["chain_with_memory"]
            if "rag_chain" in chain_data:
                del chain_data["rag_chain"]
            return chain_data
        return None
    
    async def clear_memory(self, specialist_id: str):
        """Limpar memória de um especialista."""
        memory_key = f"memory_{specialist_id}"
        if memory_key in self.memories:
            self.memories[memory_key].clear()
            logger.info(f"✅ Memória limpa para especialista {specialist_id}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check do LangChain Service."""
        return {
            "status": "healthy",
            "service": "langchain",
            "chains_count": len(self.chains),
            "memories_count": len(self.memories),
            "vectorstores_count": len(self.vectorstores),
            "tools_count": len(self.tools),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _apply_voice_style(self, response: str, specialist_id: str, tenant_id: str = None) -> str:
        """Aplicar estilo de voz da organização automaticamente."""
        try:
            # Verificar se não é o próprio especialista de estilo de voz
            if VoiceStyleBase.is_voice_style_specialist(specialist_id):
                return response
            
            # Obter nome da organização do tenant_id (pode ser implementado com lookup)
            organization_name = self._get_organization_name(tenant_id) if tenant_id else "Sua Organização"
            
            # Obter prompt de integração de estilo personalizado
            voice_style_prompt = VoiceStyleBase.get_integration_prompt(organization_name)
            
            # Criar prompt combinado
            combined_prompt = f"""
            {voice_style_prompt}
            
            RESPOSTA ORIGINAL:
            {response}
            
            INSTRUÇÃO: Ajuste a resposta acima para seguir o tom de voz da {organization_name}, mantendo todo o conteúdo técnico e informativo.
            """
            
            # Processar com LLM para ajustar estilo
            adjusted_response = await self.llm.ainvoke(combined_prompt)
            
            logger.info(f"✅ Estilo de voz da {organization_name} aplicado à resposta do especialista {specialist_id}")
            return adjusted_response
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao aplicar estilo de voz: {e}")
            return response
    
    def _get_organization_name(self, tenant_id: str) -> str:
        """Obter nome da organização baseado no tenant_id."""
        # Aqui você pode implementar um lookup para obter o nome da organização
        # Por enquanto, vamos usar o tenant_id como nome
        if tenant_id and tenant_id != "brand":
            return tenant_id.replace("-", " ").title()
        return "Sua Organização"

# Instância global do LangChain Service
langchain_service = LangChainService() 