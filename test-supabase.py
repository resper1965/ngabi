#!/usr/bin/env python3
"""
Script para testar conexão com Supabase
"""

import os
from supabase import create_client, Client

def test_supabase_connection():
    """Testa a conexão com o Supabase"""
    
    # Configurar variáveis de ambiente para teste
    os.environ['SUPABASE_URL'] = 'https://api.ngabi.ness.tec.br'
    os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE'
    
    try:
        # Criar cliente Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        print(f"🔗 Tentando conectar ao Supabase...")
        print(f"   URL: {supabase_url}")
        print(f"   Key: {supabase_key[:20]}...")
        
        if not supabase_url or not supabase_key:
            print("❌ Variáveis SUPABASE_URL ou SUPABASE_ANON_KEY não configuradas")
            return False
        
        # Criar cliente
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Testar conexão fazendo uma query simples
        print("🔍 Testando query na tabela 'tenants'...")
        response = supabase.table('tenants').select('id').limit(1).execute()
        
        print("✅ Conexão com Supabase estabelecida com sucesso!")
        print(f"   Resposta: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao conectar com Supabase: {e}")
        return False

def test_backend_integration():
    """Testa a integração do backend com Supabase"""
    
    try:
        print("\n🔧 Testando integração do backend...")
        
        # Importar módulos do backend
        import sys
        sys.path.append('./backend')
        
        from app.database import get_supabase
        
        # Testar função get_supabase
        supabase = get_supabase()
        print("✅ Função get_supabase() funcionando")
        
        # Testar query
        response = supabase.table('tenants').select('id').limit(1).execute()
        print("✅ Query através do backend funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na integração do backend: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testando configuração do Supabase para n.Gabi")
    print("=" * 50)
    
    # Teste 1: Conexão direta
    success1 = test_supabase_connection()
    
    # Teste 2: Integração com backend
    success2 = test_backend_integration()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Supabase configurado corretamente")
        print("✅ Backend integrado com Supabase")
    else:
        print("⚠️ Alguns testes falharam")
        print("🔧 Verifique a configuração do Supabase no Easypanel") 