# Colocar o Manager School no ar

## Escolha recomendada para uma demonstração estável

O projeto usa SQLite em arquivo. Para manter as notas quando o serviço reiniciar ou receber uma atualização, o arquivo precisa ficar em armazenamento persistente. O `render.yaml` prepara um serviço web Render Starter e um disco de 1 GB montado em `/var/data`; essa configuração pode gerar cobrança. O plano gratuito do Render não oferece discos persistentes, e os arquivos locais dele são apagados quando o serviço reinicia, dorme ou é implantado novamente. Consulte as [limitações do plano gratuito](https://render.com/docs/free), a documentação de [discos persistentes](https://render.com/docs/disks) e os [preços atuais](https://render.com/pricing) antes de aprovar a criação.

## Publicar pelo painel do Render

1. Garanta que o código esteja em um repositório GitHub privado ou público. Não inclua `manager_school.db`, `.env`, `.venv` ou `__pycache__`.
2. Crie/entre na conta Render e conecte a conta GitHub pelo painel.
3. Escolha **New → Blueprint** e selecione o repositório do Manager School.
4. Confira o plano `starter` e o disco persistente antes de confirmar. O arquivo `render.yaml` define os comandos de instalação e inicialização.
5. O Blueprint gera `SECRET_KEY` e `APP_PASSWORD`. No painel do serviço, confira o valor de `APP_PASSWORD`; compartilhe essa senha apenas com quem vai avaliar a demonstração. O usuário configurado é `apresentacao`.
6. Aguarde a implantação e abra o endereço `onrender.com`. A página `/healthz` é usada pela plataforma para verificar o serviço.
7. Cadastre somente nomes, turmas e notas fictícios. O banco remoto novo começa vazio e será criado em `/var/data/manager_school.db`.
8. Para atualizações, envie a nova versão ao branch conectado. O Render instala os pacotes e publica novamente o aplicativo.

O Render documenta o deploy de Flask com `pip install -r requirements.txt` e `gunicorn app:app` em seu [guia de Flask](https://render.com/docs/deploy-flask). A aplicação usa `DATABASE_PATH` para guardar o SQLite no disco persistente.

## Opção gratuita para apresentação temporária

O plano gratuito do PythonAnywhere oferece uma aplicação web Flask e armazenamento na área da conta; atualmente, contas gratuitas novas têm limite de uma aplicação, um worker e expiração após um mês. É uma opção para uma demonstração curta, mas não para deixar o projeto no ar por prazo indefinido. Confira [as condições atuais da conta gratuita](https://help.pythonanywhere.com/pages/FreeAccountsFeatures/) e o [guia oficial de Flask](https://help.pythonanywhere.com/pages/Flask).

## Verificação após a implantação

- A página `/healthz` retorna `{"status":"ok"}`.
- Sem autenticação, as páginas redirecionam para `/login` quando `APP_PASSWORD` está definida.
- O formulário de login aceita apenas o usuário e senha configurados nas variáveis do serviço.
- Uma nota fictícia continua no histórico depois de atualizar a página e reiniciar a aplicação.
- Os filtros de turma e aluno mostram apenas o recorte escolhido.
- Os downloads Excel, PDF e CSV abrem e correspondem aos mesmos filtros.
- A senha não aparece no README, no repositório ou em capturas dos slides.

## Se não quiser pagar

Use a hospedagem gratuita somente como demonstração descartável, com dados fictícios, e espere que os dados SQLite possam sumir. Para uma opção gratuita com persistência real é necessário adaptar a camada `database.py` para um banco PostgreSQL externo e rever os limites, a política de pausa e o custo do provedor escolhido. Essa migração não faz parte da configuração atual.
