import os
import sqlite3
from datetime import date
from pathlib import Path


CAMINHO_BANCO = Path(
    os.environ.get("DATABASE_PATH", Path(__file__).with_name("manager_school.db"))
)


def conectar():
    """Abre uma conexão com o banco e ativa a validação das chaves estrangeiras."""
    CAMINHO_BANCO.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_banco():
    """Cria as tabelas do sistema caso ainda não existam."""
    conexao = conectar()
    conexao.executescript("""
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            ano_letivo INTEGER NOT NULL,
            UNIQUE (nome, ano_letivo)
        );

        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            turma_id INTEGER NOT NULL,
            FOREIGN KEY (turma_id) REFERENCES turmas (id)
        );

        CREATE TABLE IF NOT EXISTS professores (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS coordenadores (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS ofertas (
            id INTEGER PRIMARY KEY,
            turma_id INTEGER NOT NULL,
            disciplina_id INTEGER NOT NULL,
            professor_id INTEGER NOT NULL,
            FOREIGN KEY (turma_id) REFERENCES turmas (id),
            FOREIGN KEY (disciplina_id) REFERENCES disciplinas (id),
            FOREIGN KEY (professor_id) REFERENCES professores (id),
            UNIQUE (turma_id, disciplina_id, professor_id)
        );

        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY,
            oferta_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            data TEXT,
            bimestre INTEGER NOT NULL CHECK (bimestre BETWEEN 1 AND 4),
            valor_maximo REAL NOT NULL CHECK (valor_maximo > 0),
            FOREIGN KEY (oferta_id) REFERENCES ofertas (id)
        );

        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY,
            avaliacao_id INTEGER NOT NULL,
            aluno_id INTEGER NOT NULL,
            valor REAL NOT NULL CHECK (valor >= 0),
            FOREIGN KEY (avaliacao_id) REFERENCES avaliacoes (id),
            FOREIGN KEY (aluno_id) REFERENCES alunos (id),
            UNIQUE (avaliacao_id, aluno_id)
        );
    """)
    conexao.close()


def obter_ou_criar_turma(nome, ano_letivo):
    conexao = conectar()
    conexao.execute(
        "INSERT OR IGNORE INTO turmas (nome, ano_letivo) VALUES (?, ?)",
        (nome, ano_letivo),
    )
    linha = conexao.execute(
        "SELECT id FROM turmas WHERE nome = ? AND ano_letivo = ?",
        (nome, ano_letivo),
    ).fetchone()
    conexao.commit()
    conexao.close()
    return linha[0]


def obter_ou_criar_aluno(nome, turma_id):
    conexao = conectar()
    linha = conexao.execute(
        "SELECT id FROM alunos WHERE nome = ? AND turma_id = ?",
        (nome, turma_id),
    ).fetchone()
    if linha is None:
        cursor = conexao.execute(
            "INSERT INTO alunos (nome, turma_id) VALUES (?, ?)",
            (nome, turma_id),
        )
        aluno_id = cursor.lastrowid
    else:
        aluno_id = linha[0]
    conexao.commit()
    conexao.close()
    return aluno_id


def cadastrar_aluno(nome, turma_id):
    """Cria um aluno novo, mesmo quando outro tem o mesmo nome."""
    conexao = conectar()
    cursor = conexao.execute(
        "INSERT INTO alunos (nome, turma_id) VALUES (?, ?)", (nome, turma_id)
    )
    aluno_id = cursor.lastrowid
    conexao.commit()
    conexao.close()
    return aluno_id


def obter_ou_criar_professor(nome):
    conexao = conectar()
    linha = conexao.execute(
        "SELECT id FROM professores WHERE nome = ?", (nome,)
    ).fetchone()
    if linha is None:
        cursor = conexao.execute(
            "INSERT INTO professores (nome) VALUES (?)", (nome,)
        )
        professor_id = cursor.lastrowid
    else:
        professor_id = linha[0]
    conexao.commit()
    conexao.close()
    return professor_id


def obter_ou_criar_disciplina(nome):
    conexao = conectar()
    conexao.execute(
        "INSERT OR IGNORE INTO disciplinas (nome) VALUES (?)", (nome,)
    )
    linha = conexao.execute(
        "SELECT id FROM disciplinas WHERE nome = ?", (nome,)
    ).fetchone()
    conexao.commit()
    conexao.close()
    return linha[0]


def obter_ou_criar_oferta(turma_id, disciplina_id, professor_id):
    conexao = conectar()
    conexao.execute(
        """INSERT OR IGNORE INTO ofertas
           (turma_id, disciplina_id, professor_id) VALUES (?, ?, ?)""",
        (turma_id, disciplina_id, professor_id),
    )
    linha = conexao.execute(
        """SELECT id FROM ofertas
           WHERE turma_id = ? AND disciplina_id = ? AND professor_id = ?""",
        (turma_id, disciplina_id, professor_id),
    ).fetchone()
    conexao.commit()
    conexao.close()
    return linha[0]


def obter_ou_criar_avaliacao(oferta_id, titulo, bimestre, valor_maximo):
    conexao = conectar()
    linha = conexao.execute(
        """SELECT id FROM avaliacoes
           WHERE oferta_id = ? AND titulo = ? AND bimestre = ?""",
        (oferta_id, titulo, bimestre),
    ).fetchone()
    if linha is None:
        cursor = conexao.execute(
            """INSERT INTO avaliacoes
               (oferta_id, titulo, data, bimestre, valor_maximo)
               VALUES (?, ?, ?, ?, ?)""",
            (oferta_id, titulo, date.today().isoformat(), bimestre, valor_maximo),
        )
        avaliacao_id = cursor.lastrowid
    else:
        avaliacao_id = linha[0]
    conexao.commit()
    conexao.close()
    return avaliacao_id


def salvar_nota(avaliacao_id, aluno_id, valor, valor_maximo):
    """Insere a nota ou atualiza a nota desse aluno nessa avaliação."""
    if not 0 <= valor <= valor_maximo:
        raise ValueError(f"A nota deve estar entre 0 e {valor_maximo}.")

    conexao = conectar()
    conexao.execute(
        """INSERT INTO notas (avaliacao_id, aluno_id, valor)
           VALUES (?, ?, ?)
           ON CONFLICT (avaliacao_id, aluno_id)
           DO UPDATE SET valor = excluded.valor""",
        (avaliacao_id, aluno_id, valor),
    )
    conexao.commit()
    conexao.close()


def salvar_dados_do_aluno(dados):
    """Salva aluno, turma, matérias, avaliações e notas no banco."""
    turma_id = obter_ou_criar_turma(dados["Turma"], dados["Ano letivo"])
    aluno_id = obter_ou_criar_aluno(dados["Nome"], turma_id)

    for materia, professor, titulo, bimestre, nota in zip(
        dados["Matérias"],
        dados["Professores"],
        dados["Avaliações"],
        dados["Bimestres"],
        dados["Notas"],
    ):
        professor_id = obter_ou_criar_professor(professor)
        disciplina_id = obter_ou_criar_disciplina(materia)
        oferta_id = obter_ou_criar_oferta(turma_id, disciplina_id, professor_id)
        avaliacao_id = obter_ou_criar_avaliacao(
            oferta_id, titulo, bimestre, dados["Nota máxima"]
        )
        salvar_nota(avaliacao_id, aluno_id, nota, dados["Nota máxima"])

    return aluno_id


def listar_alunos(turma_id=None):
    """Retorna os alunos cadastrados com a turma e o ano letivo."""
    conexao = conectar()
    consulta = """
        SELECT alunos.id, alunos.nome, turmas.nome, turmas.ano_letivo
        FROM alunos
        JOIN turmas ON turmas.id = alunos.turma_id
    """
    if turma_id is not None:
        consulta += " WHERE turmas.id = ?"
        alunos = conexao.execute(
            consulta + " ORDER BY alunos.nome, turmas.ano_letivo", (turma_id,)
        ).fetchall()
    else:
        alunos = conexao.execute(
            consulta + " ORDER BY alunos.nome, turmas.ano_letivo"
        ).fetchall()
    conexao.close()
    return alunos


def listar_turmas():
    """Retorna as turmas com seus IDs e anos letivos."""
    conexao = conectar()
    turmas = conexao.execute("""
        SELECT id, nome, ano_letivo
        FROM turmas
        ORDER BY ano_letivo DESC, nome
    """).fetchall()
    conexao.close()
    return turmas


def consultar_notas_do_aluno(aluno_id):
    """Retorna as notas registradas do aluno, com os dados de cada avaliação."""
    conexao = conectar()
    notas = conexao.execute("""
        SELECT
            notas.id,
            disciplinas.nome,
            professores.nome,
            avaliacoes.titulo,
            avaliacoes.bimestre,
            notas.valor,
            avaliacoes.valor_maximo
        FROM notas
        JOIN alunos ON alunos.id = notas.aluno_id
        JOIN avaliacoes ON avaliacoes.id = notas.avaliacao_id
        JOIN ofertas ON ofertas.id = avaliacoes.oferta_id
        JOIN disciplinas ON disciplinas.id = ofertas.disciplina_id
        JOIN professores ON professores.id = ofertas.professor_id
        WHERE alunos.id = ?
        ORDER BY avaliacoes.bimestre, disciplinas.nome, avaliacoes.titulo;
    """, (aluno_id,)).fetchall()
    conexao.close()
    return notas


def obter_aluno(aluno_id):
    """Retorna um aluno pelo ID, junto da turma e do ano."""
    conexao = conectar()
    aluno = conexao.execute("""
        SELECT alunos.id, alunos.nome, turmas.nome, turmas.ano_letivo, alunos.turma_id
        FROM alunos JOIN turmas ON turmas.id = alunos.turma_id
        WHERE alunos.id = ?
    """, (aluno_id,)).fetchone()
    conexao.close()
    return aluno


def consultar_dados_relatorio():
    """Retorna notas e informações escolares para montar relatórios."""
    conexao = conectar()
    linhas = conexao.execute("""
        SELECT alunos.id, alunos.nome, turmas.id, turmas.nome, turmas.ano_letivo,
               disciplinas.nome, avaliacoes.bimestre, notas.valor
        FROM notas
        JOIN alunos ON alunos.id = notas.aluno_id
        JOIN turmas ON turmas.id = alunos.turma_id
        JOIN avaliacoes ON avaliacoes.id = notas.avaliacao_id
        JOIN ofertas ON ofertas.id = avaliacoes.oferta_id
        JOIN disciplinas ON disciplinas.id = ofertas.disciplina_id
        ORDER BY alunos.nome, disciplinas.nome, avaliacoes.bimestre
    """).fetchall()
    conexao.close()
    return linhas


def atualizar_nota(nota_id, valor):
    """Atualiza uma nota depois de conferir o limite da avaliação."""
    conexao = conectar()
    linha = conexao.execute("""
        SELECT avaliacoes.valor_maximo
        FROM notas JOIN avaliacoes ON avaliacoes.id = notas.avaliacao_id
        WHERE notas.id = ?
    """, (nota_id,)).fetchone()
    if linha is None:
        conexao.close()
        raise ValueError("Nota não encontrada.")
    if not 0 <= valor <= linha[0]:
        conexao.close()
        raise ValueError(f"A nota deve ficar entre 0 e {linha[0]}.")
    conexao.execute("UPDATE notas SET valor = ? WHERE id = ?", (valor, nota_id))
    conexao.commit()
    conexao.close()


def excluir_nota(nota_id):
    conexao = conectar()
    conexao.execute("DELETE FROM notas WHERE id = ?", (nota_id,))
    conexao.commit()
    conexao.close()


def excluir_aluno(aluno_id):
    """Remove as notas e o cadastro do aluno."""
    conexao = conectar()
    conexao.execute("DELETE FROM notas WHERE aluno_id = ?", (aluno_id,))
    conexao.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
    conexao.commit()
    conexao.close()


def consultar_medias_por_materia_e_bimestre(aluno_id):
    """Calcula a média simples das avaliações por matéria e bimestre."""
    conexao = conectar()
    medias = conexao.execute("""
        SELECT
            disciplinas.nome,
            avaliacoes.bimestre,
            ROUND(AVG(notas.valor), 2),
            COUNT(notas.id)
        FROM notas
        JOIN avaliacoes ON avaliacoes.id = notas.avaliacao_id
        JOIN ofertas ON ofertas.id = avaliacoes.oferta_id
        JOIN disciplinas ON disciplinas.id = ofertas.disciplina_id
        WHERE notas.aluno_id = ?
        GROUP BY disciplinas.id, avaliacoes.bimestre
        ORDER BY disciplinas.nome, avaliacoes.bimestre;
    """, (aluno_id,)).fetchall()
    conexao.close()
    return medias
