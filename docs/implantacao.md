# Demonstração pública gratuita

## Como a versão pública funciona

O arquivo `render.yaml` configura o Manager School no plano gratuito do Render. A aplicação usa o modo `DEMO_MODE=1`: apresenta alunos e notas fictícios, permite consultar históricos e relatórios, mas bloqueia qualquer alteração. Ela não usa contas de usuário, então não há senha de demonstração para compartilhar.

O modo gratuito do Render coloca o serviço em repouso depois de 15 minutos sem acessos. A próxima visita pode levar cerca de um minuto para iniciar o aplicativo. O sistema de arquivos é temporário; por isso, o banco é criado e preenchido com dados de exemplo quando o serviço inicia. Os cadastros da demonstração não são persistentes. Consulte as [limitações oficiais do plano gratuito](https://render.com/docs/free).

## Publicar

1. Envie as alterações do projeto para o GitHub. O repositório pode permanecer privado se a conta Render tiver autorização para acessá-lo; para mostrar o código no portfólio, deixe-o público somente depois de revisar o conteúdo e confirmar que não há segredos ou dados reais.
2. Entre no Render e conecte sua conta GitHub.
3. Escolha **New → Blueprint** e selecione o repositório e a branch do Manager School.
4. Confira que o serviço está no plano **Free**. O `render.yaml` não cria disco persistente, banco pago nem senha compartilhada.
5. O Render gera `SECRET_KEY` automaticamente. Não copie seu `.env` para o painel nem para o GitHub.
6. Aguarde o primeiro deploy e abra o endereço `onrender.com` fornecido pelo Render. Esse será o link para incluir na apresentação do portfólio.
7. Confira o aviso de demonstração, abra um histórico, teste os filtros e baixe um relatório. Tente enviar uma alteração; o sistema deve recusá-la.

Render oferece URL `onrender.com` para serviços web, mas o plano gratuito tem limites de uso e pode dormir quando não recebe tráfego. A plataforma pode suspender serviços se os limites mensais forem atingidos. Não adicione discos ou serviços pagos se a exigência for custo zero.

## Segurança para esta demonstração

- `.env` e bancos locais estão no `.gitignore`; `.env.example` contém somente valores ilustrativos.
- O serviço público não habilita `APP_PASSWORD` nem contas. O `DEMO_MODE` desabilita autenticação compartilhada e bloqueia todos os envios `POST`.
- Todas as rotas têm limite básico de solicitações por IP; o formulário de login também tem um limite mais rigoroso quando o login local está ativo.
- Os contadores ficam em memória e reiniciam junto com o serviço; isso é uma proteção simples para o protótipo, não uma defesa completa contra ataques.
- Use exclusivamente os dados fictícios de `demo_data.py`. Não cadastre nomes, notas ou qualquer informação de alunos reais.

## Versão local completa

Para usar os formulários de cadastro, edição e exclusão, execute a aplicação localmente com `DEMO_MODE=0` (padrão). Se quiser ativar o login compartilhado local, configure `APP_USERNAME`, `APP_PASSWORD` e `SECRET_KEY` no seu `.env`. Essas variáveis não criam contas individuais; qualquer pessoa com o mesmo login acessa os mesmos dados locais.

Se o projeto evoluir para contas reais, antes será necessário criar usuários individuais, armazenar senhas com hash adequado, separar o acesso aos registros e planejar backup e recuperação. Um segundo fator não se aplica à demonstração pública sem login; ele pode ser avaliado quando houver contas pessoais.

