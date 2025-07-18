#!/usr/bin/env python3
"""
Script para criar a revisão inicial do Alembic automaticamente.
Executa: python scripts/create_initial_migration.py
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Executar comando e mostrar resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} concluído")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao {description.lower()}: {e}")
        if e.stderr:
            print(f"Erro: {e.stderr}")
        return False

def main():
    """Função principal para criar migration inicial"""
    print("🚀 Criando revisão inicial do Alembic...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("alembic.ini"):
        print("❌ Erro: alembic.ini não encontrado. Execute este script do diretório backend/")
        sys.exit(1)
    
    # Verificar se .env existe
    if not os.path.exists(".env"):
        print("⚠️  Aviso: arquivo .env não encontrado. Usando configurações padrão.")
    
    # Verificar se já existe alguma migration
    versions_dir = "migrations/versions"
    if os.path.exists(versions_dir):
        existing_files = [f for f in os.listdir(versions_dir) if f.endswith('.py')]
        if existing_files:
            print(f"⚠️  Aviso: já existem {len(existing_files)} migration(s) em {versions_dir}")
            response = input("Deseja continuar e criar uma nova migration? (y/N): ")
            if response.lower() != 'y':
                print("❌ Operação cancelada pelo usuário")
                sys.exit(0)
    
    # Criar revisão inicial
    success = run_command(
        'alembic revision --autogenerate -m "init schema"',
        "Criando revisão inicial com autogenerate"
    )
    
    if success:
        print("\n🎉 Revisão inicial criada com sucesso!")
        print("💡 Próximo passo: execute python scripts/run_migrations.py para aplicar as migrations")
        
        # Mostrar arquivo criado
        if os.path.exists(versions_dir):
            files = [f for f in os.listdir(versions_dir) if f.endswith('.py')]
            if files:
                latest_file = sorted(files)[-1]
                print(f"📄 Arquivo criado: migrations/versions/{latest_file}")
    else:
        print("\n❌ Erro ao criar revisão inicial")
        sys.exit(1)

if __name__ == "__main__":
    main() 