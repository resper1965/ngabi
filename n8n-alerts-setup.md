# No UI do n8n:

- Em cada workflow, insira um nó "Slack" ou "Webhook":
  • Trigger on Error → canal #alerts  
  • Trigger on Success → canal #ops  
- Configure credenciais Slack em Settings → Slack Credentials.  
- Teste um disparo de erro para confirmar notificação. 