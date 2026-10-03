# Manager School

Aplicação web acadêmica para registrar notas e acompanhar o desempenho de alunos por disciplina e bimestre. O projeto foi desenvolvido com Flask e SQLite, com relatórios em tabela e gráfico.

> Protótipo para demonstração. Use dados fictícios; o sistema não substitui um diário escolar oficial.

## Funcionalidades

- Cadastrar alunos, turmas, disciplinas, professores, avaliações e notas.
- Consultar o histórico e as médias de um aluno.
- Editar ou excluir uma nota e remover um cadastro de aluno.
- Filtrar relatórios por turma e aluno.
- Visualizar um gráfico de médias por disciplina e bimestre.
- Baixar relatórios em Excel, PDF ou CSV.
- Usar tema claro ou escuro e telas adaptáveis a celular e computador.
- Proteger a aplicação com senha quando `APP_PASSWORD` estiver configurada.

## Tecnologias

- Python e Flask para as rotas e páginas web.
- SQLite para armazenar os dados.
- Jinja para montar as páginas HTML.
- pandas para agrupar e calcular os dados dos relatórios.
- Matplotlib para gerar gráficos.
- openpyxl para gerar arquivos Excel.

## Executar localmente

É necessário ter Python 3.10 ou mais recente.

```bash
python -m venv .venv
```

No Windows, ative o ambiente e instale as bibliotecas:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000`. O banco `manager_school.db` é criado na pasta do projeto na primeira execução.

Para habilitar senha local, copie `.env.example` para `.env` e substitua os valores de `SECRET_KEY`, `APP_USERNAME` e `APP_PASSWORD`. Sem `APP_PASSWORD`, o login fica desativado no ambiente local.

## Estrutura

```text
app.py                 rotas Flask, validações e geração dos relatórios
database.py            criação das tabelas e operações SQLite
templates/             páginas Jinja
static/                estilos e JavaScript
templates/login.html  tela de acesso usada na hospedagem
docs/                  documentação e instruções de implantação
notas.py               versão de terminal do projeto
exemplo.py             exemplo de leitura dos dados
requirements.txt       dependências Python
render.yaml            configuração do serviço no Render
```

## Banco de dados

O SQLite relaciona turmas, alunos, disciplinas, professores, ofertas de disciplinas, avaliações e notas. Cada nota aponta para um aluno e uma avaliação. O código cria as tabelas automaticamente ao iniciar a aplicação.

O arquivo local do banco é ignorado pelo Git porque pode conter informações de alunos. Para publicar uma demonstração, cadastre apenas dados fictícios.

## Implantação

Consulte [docs/implantacao.md](docs/implantacao.md). A configuração `render.yaml` usa um serviço web com disco persistente porque o banco SQLite precisa sobreviver a reinícios e novas versões.

## Documentação do TCC

- [Documento do projeto](docs/documentacao.md) — escopo, requisitos, arquitetura, banco de dados e limitações.
- [Apresentação em PowerPoint](docs/Apresentacao_Manager_School.pptx)
- [Relatório em Word](docs/Relatorio_Manager_School.docx)

Preencha os campos de instituição, curso, autores, orientação e data com os dados oficiais antes de entregar o relatório à escola.

## Regras e limitações conhecidas

- As médias são aritméticas simples.
- As faixas de aprovação no histórico são provisórias: aprovado a partir de 6; recuperação a partir de 5; abaixo de 5 aparece como reprovado. Ajuste-as aos critérios definidos pela escola.
- O projeto é um protótipo acadêmico; não possui perfis diferentes de usuário, trilha de auditoria nem rotina de backup.
- A tela de login é uma proteção básica para demonstração e não substitui um sistema completo de gestão de identidade.

## Versão de terminal

O projeto também mantém uma interface de terminal:

```bash
python notas.py
```
