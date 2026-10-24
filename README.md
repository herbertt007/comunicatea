# ComunicaTEA

Plataforma educacional de Comunicação Aumentativa e Alternativa para apoiar atividades do AEE. O projeto usa Django, templates HTML, CSS e JavaScript. Não utilize dados identificáveis de estudantes em demonstrações ou capturas de tela.

## Desenvolvimento local

1. Crie e ative um ambiente virtual Python.
2. Instale as dependências: `pip install -r requirements.txt`.
3. Copie `.env.example` para `.env` e defina uma `SECRET_KEY` local.
4. Gere as migrations iniciais com `python manage.py makemigrations` e aplique-as com `python manage.py migrate`.
5. Crie um usuário administrativo com `python manage.py createsuperuser`.
6. Para dados pedagógicos de demonstração, execute `python manage.py seed_data`.
7. Inicie com `python manage.py runserver`.

SQLite é usado como padrão para facilitar a avaliação local. Para MySQL, ajuste `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_PORT` no `.env`, crie previamente o banco em `utf8mb4` e instale o driver `mysqlclient` (incluído nos requisitos).

## Privacidade e segurança

- Cadastre identificadores pedagógicos, sem nomes completos ou dados de saúde desnecessários.
- Estudantes e registros associados são filtrados pelo professor responsável nas telas de acompanhamento.
- O registro de sessão usa POST com proteção CSRF do Django; a sessão só é associada a um estudante ativo do professor autenticado.
- Imagens de pictogramas devem ter origem e licença registradas. Revise o significado antes de usar com estudantes.
- O projeto não grava áudio ou vídeo. A síntese de voz é opcional e ocorre no navegador.
- Configure `DEBUG=False`, `ALLOWED_HOSTS`, HTTPS e uma chave secreta própria antes de publicar.
