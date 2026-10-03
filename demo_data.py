"""Dados fictícios carregados apenas no modo público de demonstração."""


def popular_dados_demo(salvar_dados_do_aluno):
    """Cria um conjunto pequeno de alunos e notas para explorar os relatórios."""
    materias = [
        ("Matemática", "Professora Exemplo"),
        ("Língua Portuguesa", "Professor Demonstração"),
        ("Ciências", "Professora Modelo"),
    ]
    alunos = [
        ("Ana Exemplo", "1º A"),
        ("Bruno Exemplo", "1º A"),
        ("Lara Exemplo", "1º A"),
        ("Caio Demonstração", "1º B"),
        ("Sofia Demonstração", "1º B"),
        ("Theo Demonstração", "1º B"),
    ]

    for indice_aluno, (nome, turma) in enumerate(alunos):
        disciplinas = []
        professores = []
        avaliacoes = []
        bimestres = []
        notas = []

        for indice_materia, (materia, professor) in enumerate(materias):
            for bimestre in range(1, 5):
                disciplinas.append(materia)
                professores.append(professor)
                avaliacoes.append(f"Atividade do {bimestre}º bimestre")
                bimestres.append(bimestre)
                nota = 5.5 + ((indice_aluno + indice_materia + bimestre) % 5) * 0.8
                notas.append(round(min(nota, 9.5), 1))

        salvar_dados_do_aluno({
            "Nome": nome,
            "Turma": turma,
            "Ano letivo": 2026,
            "Matérias": disciplinas,
            "Professores": professores,
            "Avaliações": avaliacoes,
            "Bimestres": bimestres,
            "Notas": notas,
            "Nota máxima": 10,
        })

