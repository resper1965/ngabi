#!/usr/bin/env python3
"""
Script para executar migrations do Alembic.
Executa: python scripts/run_migrations.py
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
    """Função principal para executar migrations"""
    print("🚀 Iniciando execução de migrations...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("alembic.ini"):
        print("❌ Erro: alembic.ini não encontrado. Execute este script do diretório backend/")
        sys.exit(1)
    
    # Executar migrations
    success = True
    
    # Verificar status atual
    success &= run_command("alembic current", "Verificando status atual das migrations")
    
    # Executar upgrade para a versão mais recente
    success &= run_command("alembic upgrade head", "Executando migrations")
    
    # Verificar status final
    success &= run_command("alembic current", "Verificando status final das migrations")
    
    if success:
        print("\n🎉 Migrations executadas com sucesso!")
        print("💡 Próximo passo: execute python scripts/seed_data.py para inserir dados de teste")
    else:
        print("\n❌ Erro ao executar migrations")
        sys.exit(1)

if __name__ == "__main__":
    main() 