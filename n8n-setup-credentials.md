# No UI do n8n (http://localhost:5678):

1. Settings → Credentials  
2. Crie credencial "Backend API" do tipo HTTP Request:
   - Base URL: http://host.docker.internal:8000
   - Authentication: Bearer Token → insira seu JWT_SECRET ou token de serviço
3. Salve e teste conexão. 