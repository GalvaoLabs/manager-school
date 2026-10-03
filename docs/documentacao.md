# Manager School — documentação do projeto

> Documento de apoio para o TCC. Os campos de identificação institucional devem ser preenchidos com os dados oficiais da escola.

**Instituição:** [preencher]  
**Curso/turma:** [preencher]  
**Integrantes:** [preencher]  
**Orientador(a):** [preencher]  
**Local e ano:** [preencher]

## 1. Apresentação

O Manager School é um protótipo de aplicação web para registrar notas e consultar o desempenho de alunos. A pessoa usuária cadastra ou seleciona um aluno, informa a disciplina, o professor, a avaliação, o bimestre e a nota. Depois pode consultar o histórico individual e gerar relatórios para uma turma ou aluno.

O projeto foi desenvolvido como exercício acadêmico para praticar programação em Python, organização de dados relacionais, criação de páginas web e geração de relatórios.

## 2. Problema e objetivo

Registros de avaliações podem ficar dispersos em planilhas e anotações. O sistema reúne esses registros em um banco SQLite e permite consultar os resultados por aluno, disciplina e bimestre.

**Objetivo geral:** desenvolver uma aplicação web didática que permita cadastrar, consultar e resumir notas escolares.

**Objetivos específicos:**

- organizar turmas, alunos, disciplinas, professores e avaliações;
- validar notas e os dados básicos enviados pelos formulários;
- apresentar o histórico e as médias de um aluno;
- resumir notas por disciplina e bimestre;
- exportar recortes do relatório em formatos comuns.

## 3. Escopo

O sistema oferece cadastro de alunos junto com turma e ano letivo, registro de avaliações e notas, consulta do histórico individual, edição e exclusão de notas, remoção de aluno, filtros de relatórios, gráfico de médias e exportação para Excel, PDF e CSV. A interface tem tema claro e escuro e adapta o layout para telas menores.

O sistema não possui perfis distintos de usuário, trilha de auditoria, sincronização entre várias escolas ou política automática de cópias de segurança. É um protótipo de demonstração, não um diário escolar oficial.

## 4. Requisitos funcionais

| Código | Requisito |
|---|---|
| RF01 | Cadastrar um aluno associado a uma turma e ano letivo. |
| RF02 | Registrar uma nota ligada a aluno, disciplina, professor, avaliação e bimestre. |
| RF03 | Consultar o histórico de avaliações de um aluno. |
| RF04 | Editar ou excluir uma nota cadastrada. |
| RF05 | Remover um aluno e as notas relacionadas a ele. |
| RF06 | Filtrar relatórios por turma e/ou aluno. |
| RF07 | Exibir médias por disciplina e bimestre. |
| RF08 | Exportar os dados filtrados para XLSX, PDF e CSV. |

## 5. Requisitos não funcionais

- **RNF01 — Usabilidade:** formulários e tabelas devem apresentar rótulos claros e mensagens de retorno.
- **RNF02 — Compatibilidade:** a aplicação deve funcionar em navegadores modernos e se adaptar a celular e computador.
- **RNF03 — Persistência:** o SQLite deve guardar os registros entre reinicializações no ambiente local; em nuvem, precisa de um caminho persistente.
- **RNF04 — Segurança básica:** formulários POST validam token CSRF; a aplicação pode exigir login quando `APP_PASSWORD` estiver configurada.
- **RNF05 — Privacidade:** o repositório não deve conter banco com dados pessoais ou notas reais.

## 6. Tecnologias

- **Python:** linguagem usada na lógica da aplicação.
- **Flask:** rotas HTTP, sessões, mensagens e integração com os templates.
- **Jinja/HTML:** renderização das páginas.
- **CSS e JavaScript:** estilos responsivos, tema e interações simples.
- **SQLite:** armazenamento relacional em arquivo.
- **pandas:** organização e agrupamento dos registros para relatórios.
- **Matplotlib:** geração do gráfico e da página gráfica do PDF.
- **openpyxl:** geração e formatação de arquivos Excel.

## 7. Arquitetura

O navegador envia requisições para as rotas Flask em `app.py`. As rotas validam os dados, chamam as funções de persistência de `database.py` e escolhem o template Jinja que será exibido. Para relatórios, a aplicação carrega as linhas do banco em uma tabela pandas, aplica os filtros e calcula as médias. Matplotlib produz o gráfico; pandas e openpyxl montam os arquivos de exportação.

```text
Navegador
   │ HTTP / HTML
   ▼
Flask (app.py) ─────── templates/ + static/
   │
   ├── database.py ── SQLite (manager_school.db)
   │
   └── pandas ──────── resumos e filtros
           ├───────── Matplotlib (gráfico/PDF)
           └───────── openpyxl (Excel)
```

## 8. Modelo de dados

As tabelas principais são:

- **turmas:** nome e ano letivo;
- **alunos:** nome e turma à qual pertence;
- **disciplinas** e **professores:** cadastros usados nas ofertas;
- **ofertas:** combinação de turma, disciplina e professor;
- **avaliacoes:** título, bimestre, data opcional e valor máximo de uma avaliação;
- **notas:** valor obtido por um aluno em uma avaliação.

Uma turma pode ter vários alunos. Uma oferta representa a disciplina de um professor para uma turma. Uma oferta pode ter várias avaliações; uma avaliação pode ter notas de vários alunos. A combinação de avaliação e aluno é única, evitando duas notas para a mesma avaliação e pessoa.

O identificador do aluno é importante porque nomes podem se repetir. Os filtros comparam IDs; o nome serve para leitura da interface.

## 9. Fluxo de uso

1. A pessoa abre a página inicial e escolhe um aluno existente ou cadastra um novo.
2. Informa disciplina, professor, avaliação, bimestre, nota e nota máxima.
3. O servidor valida os valores e salva a nota no SQLite.
4. A página do aluno mostra as avaliações e calcula médias por disciplina e bimestre.
5. A página de relatórios filtra os registros e disponibiliza o gráfico, a tabela e os arquivos de exportação.

## 10. Validações e regras

O servidor exige disciplina, professor e título da avaliação; limita o bimestre aos valores de 1 a 4; exige nota máxima positiva e nota entre zero e o máximo informado. O relatório por aluno usa seu ID, e ao selecionar a pessoa a interface associa a turma cadastrada correspondente.

As médias são aritméticas simples. A classificação exibida no histórico (aprovado a partir de 6, recuperação a partir de 5) é provisória e precisa ser confirmada com os critérios definidos pela escola.

## 11. Segurança e privacidade

O arquivo SQLite é local e está excluído do controle de versão. Para a demonstração hospedada, o `render.yaml` gera valores para `SECRET_KEY` e `APP_PASSWORD`; o acesso é feito com o usuário `apresentacao` e a senha configurada no painel do serviço. Não publique essa senha, nem preencha o banco online com dados reais de estudantes.

O login é uma proteção simples para um protótipo. Antes de uso institucional seriam necessários, entre outros itens, contas individuais, permissões por perfil, auditoria, rotina de backup, revisão de segurança e adequação às regras de proteção de dados aplicáveis.

## 12. Como executar localmente

Com Python 3.10 ou mais recente:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000`. Para configurar login local, copie `.env.example` para `.env` e substitua as credenciais de exemplo. O arquivo `.env` não deve ser enviado ao GitHub.

## 13. Implantação

A implantação preparada usa Render com disco persistente montado em `/var/data`; `DATABASE_PATH` aponta o SQLite para esse disco. O plano Render que suporta disco persistente é pago. Não usar o serviço gratuito para guardar dados SQLite importantes, pois o sistema de arquivos gratuito é temporário. Os passos e a alternativa gratuita de demonstração estão em [implantacao.md](implantacao.md).

## 14. Limitações e melhorias futuras

- definir com a escola os critérios oficiais de aprovação;
- adicionar perfis de professor e coordenação com permissões separadas;
- permitir backups e restauração do banco;
- registrar quem alterou uma nota e quando;
- criar testes automatizados para validações, filtros e exportações;
- avaliar migração para PostgreSQL caso vários usuários precisem editar dados ao mesmo tempo;
- revisar acessibilidade e compatibilidade em aparelhos reais.

## 15. Conclusão

O Manager School reúne em uma aplicação os registros básicos de notas e oferece formas de consultar e resumir os resultados. O desenvolvimento aplica conceitos de rotas web, persistência relacional, validação, análise de dados e geração de arquivos. Como próximo passo, o projeto precisa ser comparado aos critérios oficiais do TCC e apresentado com uma base de demonstração inteiramente fictícia.

## Referências técnicas

- PALLETS PROJECT. **Flask Documentation**. Disponível em: <https://flask.palletsprojects.com/>. Acesso em: 3 out. 2026.
- SQLITE. **SQLite Documentation**. Disponível em: <https://www.sqlite.org/docs.html>. Acesso em: 3 out. 2026.
- PANDAS. **pandas Documentation**. Disponível em: <https://pandas.pydata.org/docs/>. Acesso em: 3 out. 2026.
- MATPLOTLIB. **Matplotlib Documentation**. Disponível em: <https://matplotlib.org/stable/>. Acesso em: 3 out. 2026.
- OPENPYXL. **openpyxl Documentation**. Disponível em: <https://openpyxl.readthedocs.io/>. Acesso em: 3 out. 2026.
