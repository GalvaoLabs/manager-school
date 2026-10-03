<div align="center">

# Manager School

**Aplicação web para registrar notas e acompanhar o desempenho de alunos por turma, disciplina e bimestre.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Banco_de_dados-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

</div>

---

## Sobre o projeto

O Manager School permite organizar informações escolares e consultar o desempenho de alunos e turmas. A aplicação reúne cadastros, notas, médias, gráficos e exportação de relatórios.

O projeto começou como uma proposta de estudo e possível TCC durante o curso de **Programação em Python da Fábrica de Programadores**. O curso é realizado em parceria entre o [SENAI-SP](https://www.sp.senai.br/) e a [Prefeitura de Santana de Parnaíba](https://prefeitura.santanadeparnaiba.sp.gov.br/), com aulas ministradas por professores do SENAI e certificado emitido pelo SENAI.

A formação contou com os professores [msousa07](https://github.com/msousa07) e **Hebert Félix**, que ministrou o primeiro módulo. Eles são mencionados aqui como parte do contexto do curso, não como orientadores ou colaboradores deste projeto.

Meu objetivo principal com o Manager School é revisar conceitos aprendidos no curso, praticar novas tecnologias e construir um projeto para meu portfólio. A ideia de TCC foi o ponto de partida, mas o projeto não foi apresentado como trabalho oficial de conclusão de curso.

Ferramentas de inteligência artificial foram utilizadas como apoio durante a análise, implementação e documentação. O desenvolvimento é acompanhado pelo autor, que também estuda e revisa as soluções aplicadas.

> **Aviso:** este projeto é um protótipo de estudo. Utilize dados fictícios; ele não substitui um diário escolar oficial.

## Funcionalidades

- Cadastrar alunos, turmas, disciplinas, professores, avaliações e notas.
- Consultar o histórico e as médias de um aluno.
- Editar ou excluir notas e remover um cadastro de aluno.
- Filtrar relatórios por turma e aluno.
- Visualizar gráficos de médias por disciplina e bimestre.
- Exportar relatórios em Excel, PDF ou CSV.
- Usar tema claro ou escuro em telas adaptáveis a computador e celular.
- Ativar login compartilhado no modo local; a demonstração pública não exige login.
- Acessar uma demonstração pública em modo somente leitura, com dados fictícios.

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python e Flask | Rotas e funcionamento da aplicação web |
| SQLite e SQL | Armazenamento e consulta dos dados |
| Jinja, HTML e CSS | Estrutura e apresentação das páginas |
| JavaScript | Interações da interface |
| pandas | Organização e análise dos dados dos relatórios |
| Matplotlib | Geração dos gráficos |
| openpyxl | Criação de planilhas Excel |

## Estrutura do repositório

```text
.
├── app.py                 aplicação Flask e geração dos relatórios
├── database.py            criação das tabelas e operações SQLite
├── notas.py               versão de terminal para registrar e analisar notas
├── exemplo.py             exemplo de leitura dos dados
├── demo_data.py           dados fictícios usados na demonstração pública
├── templates/             páginas HTML renderizadas pelo Jinja
├── static/                estilos CSS e JavaScript
├── docs/                  documentação e materiais do projeto
├── requirements.txt       dependências Python
└── render.yaml            configuração preparada para o Render
```

## Como executar localmente

É necessário ter Python 3.10 ou mais recente.

Crie um ambiente virtual:

```bash
python -m venv .venv
```

No Windows, ative o ambiente, instale as dependências e inicie a aplicação:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Depois, acesse [http://127.0.0.1:5000](http://127.0.0.1:5000).

O banco `manager_school.db` é criado automaticamente na primeira execução. Para ativar o login local, copie `.env.example` para `.env` e substitua os valores de exemplo. O arquivo `.env` está no `.gitignore` e não deve ser enviado ao GitHub. Sem `APP_PASSWORD`, o login fica desativado localmente.

## Banco de dados e privacidade

O SQLite relaciona turmas, alunos, disciplinas, professores, ofertas de disciplinas, avaliações e notas. Cada nota está associada a um aluno e a uma avaliação.

O banco local é ignorado pelo Git porque pode conter dados pessoais. Use apenas nomes, turmas e notas fictícios nas demonstrações. O login atual usa uma credencial compartilhada e não possui contas ou permissões individuais.

## Documentação

- [Documentação técnica](docs/documentacao.md)
- [Instruções de implantação](docs/implantacao.md)
- [Apresentação do projeto](docs/Apresentacao_Manager_School.pptx)
- [Relatório do projeto](docs/Relatorio_Manager_School.docx)

## Hospedagem

A configuração gratuita para uma demonstração no Render está em `render.yaml`. O modo público usa dados fictícios, bloqueia alterações e recria os registros quando o serviço inicia. Como a hospedagem gratuita não oferece disco persistente, a demonstração pode dormir e levar cerca de um minuto para abrir após um período sem acessos; consulte as [instruções de implantação](docs/implantacao.md). **O projeto ainda não está publicado na web.**

## Limitações conhecidas

- As médias são aritméticas simples.
- Os critérios de aprovação e recuperação são provisórios e devem ser ajustados conforme as regras da escola.
- O sistema ainda não possui perfis diferentes de usuário, trilha de auditoria nem rotina automática de backup.
- É um protótipo acadêmico e de portfólio, não um sistema escolar oficial.


