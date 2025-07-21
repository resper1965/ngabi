# Testes - Chat Multi-Agente

Este diretório contém todos os testes do backend, incluindo fixtures, exemplos e configurações.

## 📁 Estrutura

```
tests/
├── conftest.py          # Fixtures globais do PyTest
├── test_example.py      # Exemplos de testes
└── README.md           # Esta documentação
```

## 🚀 Como Executar os Testes

### Instalação das Dependências

```bash
# Instalar dependências de teste
pip install -r requirements.txt
```

### Execução Básica

```bash
# Executar todos os testes
pytest

# Executar com verbose
pytest -v

# Executar com cobertura
pytest --cov=app --cov-report=html
```

### Execução Específica

```bash
# Executar apenas testes unitários
pytest -m unit

# Executar apenas testes de integração
pytest -m integration

# Executar testes lentos
pytest -m slow

# Executar testes específicos
pytest tests/test_example.py::TestDatabaseFixtures

# Executar com paralelização
pytest -n auto
```

## 🔧 Fixtures Disponíveis

### Fixtures de Banco de Dados

#### `postgres_container`
Container PostgreSQL usando Testcontainers.
- **Scope**: session
- **Uso**: Fornece PostgreSQL isolado para testes

#### `test_engine`
Engine SQLAlchemy para banco de teste.
- **Scope**: session
- **Uso**: Conexão com banco de teste

#### `test_session`
Sessão de teste com rollback automático.
- **Scope**: function
- **Uso**: Sessão isolada para cada teste

#### `db_session`
Alias para `test_session`.
- **Scope**: function
- **Uso**: Compatibilidade com código existente

### Fixtures de Dados de Exemplo

#### `sample_tenant`
Tenant de exemplo para testes.
```python
def test_tenant(sample_tenant):
    assert sample_tenant.name == "Test Company"
```

#### `sample_user`
Usuário de exemplo para testes.
```python
def test_user(sample_user, sample_tenant):
    assert sample_user.tenant_id == sample_tenant.id
```

#### `sample_agent`
Agente de exemplo para testes.
```python
def test_agent(sample_agent):
    assert sample_agent.name == "TestAgent"
```

#### `sample_tenant_settings`
Configurações de tenant de exemplo.
```python
def test_settings(sample_tenant_settings):
    assert sample_tenant_settings.orchestrator_name == "Test Orchestrator"
```

### Fixtures de Dados de Seed

#### `seeded_database`
Banco populado com dados de seed para testes de integração.
```python
def test_seeded_data(seeded_database):
    tenants = seeded_database["tenants"]
    users = seeded_database["users"]
    agents = seeded_database["agents"]
    
    assert len(tenants) == 2
    assert len(users) == 3
    assert len(agents) == 2
```

### Fixtures de Aplicação

#### `test_app`
Aplicação FastAPI para testes.
```python
def test_health_endpoint(test_app):
    response = test_app.get("/health")
    assert response.status_code == 200
```

#### `auth_headers`
Headers de autenticação para testes.
```python
def test_protected_endpoint(test_app, auth_headers):
    response = test_app.get("/protected", headers=auth_headers)
    assert response.status_code == 200
```

#### `tenant_headers`
Headers com tenant específico.
```python
def test_tenant_endpoint(test_app, tenant_headers):
    response = test_app.get("/tenant-data", headers=tenant_headers)
    assert response.status_code == 200
```

### Factories

#### `tenant_factory`
Factory para criar tenants.
```python
def test_custom_tenant(tenant_factory):
    tenant = tenant_factory(name="Custom", subdomain="custom")
    assert tenant.name == "Custom"
```

#### `user_factory`
Factory para criar usuários.
```python
def test_custom_user(user_factory, tenant_factory):
    tenant = tenant_factory()
    user = user_factory(tenant_id=tenant.id, role="admin")
    assert user.role == "admin"
```

#### `agent_factory`
Factory para criar agentes.
```python
def test_custom_agent(agent_factory, tenant_factory):
    tenant = tenant_factory()
    agent = agent_factory(tenant_id=tenant.id, name="CustomAgent")
    assert agent.name == "CustomAgent"
```

## 📊 Markers Personalizados

### Markers Disponíveis

- `@pytest.mark.unit` - Testes unitários (rápidos, isolados)
- `@pytest.mark.integration` - Testes de integração (requerem banco)
- `@pytest.mark.slow` - Testes lentos
- `@pytest.mark.api` - Testes de endpoints da API
- `@pytest.mark.database` - Testes específicos de banco
- `@pytest.mark.auth` - Testes de autenticação

### Uso dos Markers

```python
@pytest.mark.unit
def test_fast_function():
    assert 2 + 2 == 4

@pytest.mark.integration
def test_database_operation(test_session):
    # Teste que requer banco
    pass

@pytest.mark.slow
def test_expensive_operation():
    # Teste lento
    pass
```

## 🔄 Isolamento de Testes

### Rollback Automático

Cada teste executa em uma transação que é revertida automaticamente:

```python
def test_isolation_1(test_session):
    # Criar dados
    tenant = Tenant(name="Test", subdomain="test")
    test_session.add(tenant)
    test_session.commit()
    # Dados existem durante o teste

def test_isolation_2(test_session):
    # Dados do teste anterior não existem aqui
    tenant = test_session.query(Tenant).filter_by(subdomain="test").first()
    assert tenant is None  # Rollback removeu os dados
```

### Containers Isolados

O PostgreSQL roda em containers isolados para cada sessão de teste:

```python
def test_container_isolation(postgres_container):
    # Cada sessão de teste tem seu próprio container
    assert postgres_container.is_running()
```

## 📈 Cobertura de Código

### Configuração de Cobertura

O projeto está configurado para:
- Mínimo de 80% de cobertura
- Relatórios em HTML, XML e terminal
- Falha se cobertura estiver abaixo do mínimo

### Executar com Cobertura

```bash
# Cobertura básica
pytest --cov=app

# Cobertura detalhada
pytest --cov=app --cov-report=html --cov-report=term-missing

# Cobertura com falha se abaixo do mínimo
pytest --cov=app --cov-fail-under=80
```

## 🐛 Troubleshooting

### Erro de Container

```bash
# Verificar se Docker está rodando
docker ps

# Verificar se testcontainers está instalado
pip install testcontainers
```

### Erro de Conexão

```bash
# Verificar se PostgreSQL está disponível
docker run --rm postgres:15-alpine psql --version

# Verificar variáveis de ambiente
python -c "import os; print('DOCKER_HOST:', os.getenv('DOCKER_HOST'))"
```

### Erro de Dependências

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Verificar versões
pip list | grep -E "(pytest|testcontainers|sqlalchemy)"
```

## 📝 Exemplos de Testes

### Teste de Endpoint da API

```python
def test_create_tenant(test_app, auth_headers):
    data = {
        "name": "New Company",
        "subdomain": "new-company"
    }
    
    response = test_app.post("/tenants", json=data, headers=auth_headers)
    assert response.status_code == 201
    
    result = response.json()
    assert result["name"] == "New Company"
    assert result["subdomain"] == "new-company"
```

### Teste de Modelo

```python
def test_tenant_creation(test_session):
    tenant = Tenant(
        name="Test Company",
        subdomain="test-company"
    )
    
    test_session.add(tenant)
    test_session.commit()
    
    assert tenant.id is not None
    assert tenant.created_at is not None
```

### Teste de Relacionamentos

```python
def test_tenant_relationships(test_session):
    # Criar tenant
    tenant = Tenant(name="Test", subdomain="test")
    test_session.add(tenant)
    test_session.commit()
    
    # Criar usuário
    user = User(
        tenant_id=tenant.id,
        email="test@example.com",
        password_hash="hash",
        role="admin"
    )
    test_session.add(user)
    test_session.commit()
    
    # Verificar relacionamento
    assert user.tenant_id == tenant.id
    assert user.tenant == tenant
```

### Teste Parametrizado

```python
@pytest.mark.parametrize("name,subdomain", [
    ("Company A", "company-a"),
    ("Company B", "company-b"),
    ("Company C", "company-c"),
])
def test_tenant_names(tenant_factory, name, subdomain):
    tenant = tenant_factory(name=name, subdomain=subdomain)
    assert tenant.name == name
    assert tenant.subdomain == subdomain
```

## 🚀 Próximos Passos

1. **Criar testes específicos** para cada endpoint da API
2. **Implementar testes de autenticação** com JWT
3. **Adicionar testes de performance** para operações lentas
4. **Configurar CI/CD** com execução automática de testes
5. **Implementar testes de carga** para endpoints críticos

## 📚 Recursos Adicionais

- [Documentação do PyTest](https://docs.pytest.org/)
- [Testcontainers Python](https://testcontainers-python.readthedocs.io/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/) 