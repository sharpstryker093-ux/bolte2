# Site Bolte — Versão com Banco de Dados e Login

## O que mudou nessa versão

- **Banco de dados** (SQLite, arquivo `site.db`, criado automaticamente)
- **Cadastro e login de usuários** — o **primeiro usuário que se cadastrar se torna administrador** automaticamente
- **Painel (`/dashboard`)**:
  - Administrador vê as mensagens recebidas pelo formulário de contato e pode adicionar/remover serviços
  - Outros usuários veem uma tela simples de boas-vindas
- **Formulário de contato** salva as mensagens no banco
- **Lista de serviços dinâmica** — o admin edita pelo painel, sem precisar tocar no código
- **Visual novo**: tema escuro com destaque amarelo-elétrico, inspirado no nome "Bolte" (energia/raio)

## Como rodar localmente

1. Extraia esse zip
2. No terminal, dentro da pasta:
   ```
   pip install flask gunicorn
   python app.py
   ```
3. Acesse http://127.0.0.1:5000

## Como criar seu usuário administrador

1. Acesse `/cadastro` e crie sua conta — como será a primeira, ela já nasce administradora
2. Faça login em `/login`
3. Acesse `/dashboard` para ver mensagens e gerenciar serviços

⚠️ Se você já tinha testado e quer recomeçar o banco do zero, basta apagar o arquivo `site.db` antes de rodar de novo.

## Como editar o conteúdo

- **Dados da empresa** (nome, telefone, e-mail, endereço) → `app.py`, dicionário `EMPRESA`
- **Serviços** → pelo painel administrativo (`/dashboard`), não precisa editar código
- **Textos institucionais** (Sobre) → `templates/sobre.html`
- **Cores e visual** → `static/css/style.css` (as cores principais estão no topo, em `:root`)

## Publicando no Render (atualização do mesmo site já no ar)

1. Suba estes arquivos pro mesmo repositório do GitHub que você já criou (pode substituir os arquivos antigos)
2. O Render detecta a mudança automaticamente e republica o site
3. Pronto — seu domínio `bolte.com.br` já vai mostrar a nova versão

## Próximos passos possíveis

- Adicionar upload de imagens para cada serviço
- Enviar e-mail de notificação quando alguém preenche o contato
- Página "Sobre" com a história real da empresa
- Mais campos no cadastro de clientes (telefone, empresa, etc.)

Qualquer coisa, só perguntar!
