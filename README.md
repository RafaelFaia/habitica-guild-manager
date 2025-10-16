<div align="center">
  <h1>🧩 Habitica Guild Manager</h1>
  <p>Automação para gerenciamento de grupos no <a href="https://habitica.com/">Habitica</a></p>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
</div>

- 🤖 Convite automático de usuários procurando grupo  
- 🗑️ Remoção automática de membros inativos (+7 dias)  
- 📊 Logs detalhados de todas as operações  

---

## ⚙️ Configuração

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

2. Edite o .env com suas credenciais da API Habitica:

- **HABITICA_API_USER**: Seu User ID (encontre em: Settings → Site Data → User ID)
- **HABITICA_API_KEY**: Seu API Token (encontre em: Settings → Site Data → API Token)  
- **MIN_LEVEL**: Nível mínimo para convites
- **WANTED_LANGUAGE**: Idioma desejado

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🚀 Uso

🔹 Convidar novos usuários
```bash
python invite_users.py
```
Envia convites automáticos para até dois usuários que estão procurando grupo.

🔹 Remover membros inativos
```bash
python remove_inactive_members.py
```
Remove automaticamente membros que estão inativos há mais de 7 dias.

---

## 🧾 Logs
Todos os eventos são registrados em:
- `logs/habitica_guild_manager.log` — histórico detalhado das ações
- `logs/invited_uuids.json` — rastreamento de usuários já convidados

---

## 📁 Estrutura
```arduino
habitica-guild-manager/
├── config.py
├── invite_users.py
├── remove_inactive_members.py
├── log_manager.py
├── logger.py
├── .env.example
├── .gitignore
└── logs/
```

---

## 🧠 Observação
O `.env` nunca deve ser commitado.  
As variáveis sensíveis são carregadas automaticamente via [`python-dotenv`](https://pypi.org/project/python-dotenv/).