<div align="center">

# Manager School

**Aplicação web para registrar notas e acompanhar o desempenho de alunos por turma, disciplina e bimestre.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Banco_de_dados-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Licença MIT](https://img.shields.io/badge/Licen%C3%A7a-MIT-green.svg)](LICENSE)

</div>

---

## Demonstração online

[Acessar o Manager School](https://manager-school-demo.onrender.com/)

A demonstração usa dados fictícios e está disponível somente para consulta. O serviço gratuito pode entrar em repouso após um período sem acessos, então a primeira visita pode demorar. Como o armazenamento é temporário, os dados de demonstração podem ser recriados quando o serviço reiniciar.

## Sobre o projeto

O Manager School é um projeto de estudo e portfólio desenvolvido pelo aluno Miguel Henrique da Silva Galvão ([GalvaoLabs](https://github.com/GalvaoLabs/)) durante o curso de **Programação em Python da Fábrica de Programadores**, realizado em parceria entre o [SENAI-SP](https://www.sp.senai.br/) e a [Prefeitura de Santana de Parnaíba](https://prefeitura.santanadeparnaiba.sp.gov.br/).

O objetivo é revisar conceitos do curso, praticar novas tecnologias e aprender construindo uma aplicação web. Ferramentas de inteligência artificial foram usadas como apoio; as soluções foram estudadas e revisadas durante o desenvolvimento.

> **Aviso:** este é um protótipo acadêmico e de portfólio. Use somente dados fictícios; o sistema não substitui um diário escolar oficial.

## Funcionalidades

- Cadastrar alunos, turmas, disciplinas, professores, avaliações e notas.
- Consultar o histórico e as médias de um aluno.
- Editar ou excluir notas e remover cadastros de alunos.
- Filtrar relatórios por turma e aluno.
- Visualizar gráficos de médias por disciplina e bimestre.
- Exportar relatórios em Excel, PDF ou CSV.
- Usar tema claro ou escuro em uma interface adaptável a computadores e celulares.
- Ativar login compartilhado no modo local.
- Consultar a demonstração pública, que não exige login e não permite alterações.

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python e Flask | Rotas e funcionamento da aplicação web |
| SQLite e SQL | Armazenamento e consulta dos dados |
| Jinja, HTML e CSS | Páginas e apresentação da interface |
| JavaScript | Interações da interface |
| pandas | Organização e análise dos dados dos relatórios |
| Matplotlib | Geração dos gráficos |
| openpyxl | Criação de planilhas Excel |

## Estrutura do repositório

```text
.
├── app.py                 aplicação Flask e geração dos relatórios
├── database.py            criação das tabelas e operações SQLite
├── notas.py               programa de terminal complementar, mantido para consulta
├── exemplo.py             exemplo de leitura dos dados
├── templates/             páginas HTML renderizadas pelo Jinja
├── static/                estilos CSS e JavaScript
├── docs/                  documentação e materiais do projeto
├── requirements.txt       dependências Python
└── render.yaml            configuração de implantação no Render
```

## Como executar localmente

É necessário ter Python 3.10 ou mais recente.

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual.

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS ou Linux:**

```bash
source .venv/bin/activate
```

Instale as dependências e inicie a aplicação:

```bash
python -m pip install -r requirements.txt
python app.py
```

Acesse [http://127.0.0.1:5000](http://127.0.0.1:5000).

O banco SQLite é criado automaticamente na primeira execução. Para ativar o login local, copie `.env.example` para `.env` e troque os valores de exemplo por uma chave secreta e uma senha fortes. Sem `APP_PASSWORD`, o login local fica desativado. O arquivo `.env` é ignorado pelo Git e não deve ser enviado ao GitHub.

## Banco de dados e privacidade

O SQLite relaciona turmas, alunos, disciplinas, professores, ofertas de disciplinas, avaliações e notas. Cada nota está associada a um aluno e a uma avaliação.

O banco local pode conter dados pessoais e não deve ser publicado. A demonstração online usa apenas dados fictícios. O login local atual usa uma credencial compartilhada e não oferece contas ou permissões individuais.

## Documentação

- [Documentação técnica](docs/documentacao.md)
- [Instruções de implantação](docs/implantacao.md)
- [Apresentação do projeto](docs/Apresentacao_Manager_School.pptx)
- [Relatório do projeto](docs/Relatorio_Manager_School.docx)

## Hospedagem

[A demonstração online](https://manager-school-demo.onrender.com/) está hospedada gratuitamente no Render em modo somente para consulta, com dados fictícios. O serviço usa armazenamento temporário e pode entrar em repouso após um período sem acessos; por isso, a primeira visita pode demorar e os dados podem ser recriados quando o serviço reiniciar. O código e a configuração específicos da demonstração estão na branch `portfolio-demo`. Consulte as [instruções de implantação](docs/implantacao.md) para mais detalhes.

## Aprendizados e próximos passos

Durante o desenvolvimento, pratiquei aplicações web com Flask, operações em banco relacional, filtros, geração de relatórios e configuração de uma demonstração hospedada.

Como próximos passos, quero adicionar testes automatizados, estudar contas individuais de usuários e avaliar uma migração para PostgreSQL se o projeto precisar de armazenamento persistente.

## Limitações conhecidas

- As médias são aritméticas simples.
- Os critérios de aprovação e recuperação são provisórios e devem ser ajustados conforme as regras de cada escola.
- O sistema ainda não possui perfis individuais de usuário, trilha de auditoria ou rotina automática de backup.
- É um protótipo acadêmico e de portfólio, não um sistema escolar oficial.

## Licença

Este projeto está disponível sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE).
