import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).with_name("manager_school.db")

conexao = sqlite3.connect(CAMINHO_BANCO)
conexao.execute("PRAGMA foreign_keys = ON")

conexao.executescript("""
    INSERT OR IGNORE INTO turmas (id, nome, ano_letivo)
    VALUES (1, '1º A', 2026);

    INSERT OR IGNORE INTO alunos (id, nome, turma_id)
    VALUES
        (1, 'João', 1),
        (2, 'Maria', 1),
        (3, 'Pedro', 1);

    INSERT OR IGNORE INTO professores (id, nome)
    VALUES (1, 'Carlos');

    INSERT OR IGNORE INTO disciplinas (id, nome)
    VALUES (1, 'Matemática');

    INSERT OR IGNORE INTO ofertas
        (id, turma_id, disciplina_id, professor_id)
    VALUES (1, 1, 1, 1);

    INSERT OR IGNORE INTO avaliacoes
        (id, oferta_id, titulo, data, bimestre, valor_maximo)
    VALUES
        (1, 1, 'Prova 1', '2026-03-10', 1, 10),
        (2, 1, 'Trabalho', '2026-04-05', 1, 10),
        (3, 1, 'Prova 2', '2026-05-12', 2, 10);

    INSERT OR IGNORE INTO notas
        (avaliacao_id, aluno_id, valor)
    VALUES
        (1, 1, 8.0),
        (2, 1, 9.0),
        (3, 1, 7.0),
        (1, 2, 9.5),
        (2, 2, 8.5),
        (3, 2, 10.0),
        (1, 3, 6.0),
        (2, 3, 5.5),
        (3, 3, 7.0);
""")

resultado = conexao.execute("""
    SELECT
        alunos.nome,
        disciplinas.nome,
        ROUND(AVG(notas.valor), 2) AS media
    FROM notas
    JOIN alunos
        ON alunos.id = notas.aluno_id
    JOIN avaliacoes
        ON avaliacoes.id = notas.avaliacao_id
    JOIN ofertas
        ON ofertas.id = avaliacoes.oferta_id
    JOIN disciplinas
        ON disciplinas.id = ofertas.disciplina_id
    GROUP BY alunos.id, disciplinas.id
    ORDER BY alunos.nome;
""")

for nome, disciplina, media in resultado:
    print(f"{nome} | {disciplina} | média: {media}")

print("\nNOTAS INDIVIDUAIS")
notas_individuais = conexao.execute("""
    SELECT
        alunos.nome AS aluno,
        turmas.nome AS turma,
        disciplinas.nome AS disciplina,
        professores.nome AS professor,
        avaliacoes.titulo AS avaliacao,
        avaliacoes.bimestre AS bimestre,
        notas.valor AS nota,
        avaliacoes.valor_maximo AS valor_maximo
    FROM notas
    JOIN alunos
        ON alunos.id = notas.aluno_id
    JOIN turmas
        ON turmas.id = alunos.turma_id
    JOIN avaliacoes
        ON avaliacoes.id = notas.avaliacao_id
    JOIN ofertas
        ON ofertas.id = avaliacoes.oferta_id
    JOIN disciplinas
        ON disciplinas.id = ofertas.disciplina_id
    JOIN professores
        ON professores.id = ofertas.professor_id
    ORDER BY turmas.nome, alunos.nome, disciplinas.nome, avaliacoes.bimestre;
""")

for linha in notas_individuais:
    aluno, turma, disciplina, professor, avaliacao, bimestre, nota, valor_maximo = linha
    print(
        f"{aluno} | {turma} | {disciplina} | {professor} | "
        f"{avaliacao} ({bimestre}º bimestre): {nota}/{valor_maximo}"
    )

conexao.close()
