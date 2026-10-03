# Análise e registro de notas escolares
from statistics import mean

from database import (
    criar_banco,
    salvar_dados_do_aluno,
    listar_alunos,
    consultar_notas_do_aluno,
    consultar_medias_por_materia_e_bimestre,
)


# Regras iniciais do sistema
NOTA_MINIMA = 0
NOTA_MAXIMA = 10
MEDIA_APROVACAO = 6
MEDIA_RECUPERACAO = 5
QUANT_MIN_MATERIAS = 1


def ler_texto_obrigatorio(pergunta):
    """Solicita um texto e não aceita uma resposta vazia."""
    while True:
        resposta = input(pergunta).strip()
        if resposta:
            return resposta
        print("Esse campo não pode ficar vazio.")


def ler_inteiro(pergunta, minimo, maximo=None):
    """Lê um inteiro e repete a pergunta até receber um valor válido."""
    while True:
        try:
            valor = int(input(pergunta))
            if valor < minimo or (maximo is not None and valor > maximo):
                limite = f"entre {minimo} e {maximo}" if maximo else f"maior ou igual a {minimo}"
                print(f"Digite um número {limite}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def coletar_dados():
    """Coleta dados de um aluno e uma nota por matéria."""
    aluno = ler_texto_obrigatorio("Qual o nome do aluno? ")
    turma = ler_texto_obrigatorio("Qual é a turma do aluno? ")
    ano_letivo = ler_inteiro("Qual é o ano letivo? ", 2000)
    quant_materias = ler_inteiro(
        "Digite a quantidade de matérias: ", QUANT_MIN_MATERIAS
    )

    materias = []
    professores = []
    avaliacoes = []
    bimestres = []
    notas = []

    for numero in range(1, quant_materias + 1):
        print(f"\nMatéria {numero}")
        materia = ler_texto_obrigatorio("Nome da matéria: ")
        professor = ler_texto_obrigatorio("Nome do professor: ")
        avaliacao = ler_texto_obrigatorio("Nome da avaliação: ")
        bimestre = ler_inteiro("Bimestre (1 a 4): ", 1, 4)

        while True:
            try:
                nota = float(input(f"Nota (de {NOTA_MINIMA} a {NOTA_MAXIMA}): "))
                if NOTA_MINIMA <= nota <= NOTA_MAXIMA:
                    break
                print(f"Digite uma nota de {NOTA_MINIMA} a {NOTA_MAXIMA}.")
            except ValueError:
                print("Entrada inválida. Digite uma nota numérica.")

        materias.append(materia)
        professores.append(professor)
        avaliacoes.append(avaliacao)
        bimestres.append(bimestre)
        notas.append(nota)

    return {
        "Nome": aluno,
        "Turma": turma,
        "Ano letivo": ano_letivo,
        "Quantidade de Matérias": quant_materias,
        "Matérias": materias,
        "Professores": professores,
        "Avaliações": avaliacoes,
        "Bimestres": bimestres,
        "Nota máxima": NOTA_MAXIMA,
        "Notas": notas,
    }


def analisar_notas(notas):
    """Calcula indicadores básicos para as notas informadas."""
    media = mean(notas)
    maior_nota = max(notas)
    menor_nota = min(notas)
    quant_notas_media_aprovacao = sum(nota >= MEDIA_APROVACAO for nota in notas)
    quant_notas_media_reprovacao = sum(nota < MEDIA_APROVACAO for nota in notas)

    return {
        "Média": media,
        "Maior Nota": maior_nota,
        "Menor Nota": menor_nota,
        "Quantidade de Notas Azuis": quant_notas_media_aprovacao,
        "Quantidade de Notas Vermelhas": quant_notas_media_reprovacao,
    }


def classificar_media(media):
    """Classifica uma média de período segundo os limites atuais do projeto."""
    if media >= MEDIA_APROVACAO:
        return "Aprovado"
    if media >= MEDIA_RECUPERACAO:
        return "Recuperação"
    return "Reprovado"


def exibir_medias_por_periodo(aluno_id):
    """Exibe médias e classificação separadas por matéria e bimestre."""
    medias = consultar_medias_por_materia_e_bimestre(aluno_id)
    if not medias:
        print("Não há médias para exibir.")
        return

    print("\nRESULTADO POR MATÉRIA E BIMESTRE")
    for disciplina, bimestre, media, quantidade_avaliacoes in medias:
        situacao = classificar_media(media)
        print(
            f"{disciplina} | {bimestre}º bimestre: média {media:.2f} | "
            f"{situacao} ({quantidade_avaliacoes} avaliação(ões))"
        )


def saida_dados(dados, resultados):
    """Exibe as notas, os dados escolares e a análise calculada."""
    print("=" * 50)
    print("\nANÁLISE DE NOTAS\n")
    print("=" * 50)
    print(f"\nAluno: {dados['Nome']}")
    print(f"Turma: {dados['Turma']} ({dados['Ano letivo']})")
    print("\nMatérias e avaliações:")

    for materia, professor, avaliacao, bimestre, nota in zip(
        dados["Matérias"],
        dados["Professores"],
        dados["Avaliações"],
        dados["Bimestres"],
        dados["Notas"],
    ):
        print(
            f"- {materia} | {professor} | {avaliacao} | "
            f"{bimestre}º bimestre: {nota:.2f}"
        )

    print("\n" + "-" * 50)
    print(f"Média simples de todas as notas: {resultados['Média']:.2f}")
    print(f"Maior nota: {resultados['Maior Nota']:.2f}")
    print(f"Menor nota: {resultados['Menor Nota']:.2f}")
    print(f"Quantidade de notas a partir de 6: {resultados['Quantidade de Notas Azuis']}")
    print(f"Quantidade de notas abaixo de 6: {resultados['Quantidade de Notas Vermelhas']}")
    print("A classificação final será mostrada por matéria e bimestre.")
    print("=" * 50)


def consultar_aluno_cadastrado():
    """Permite selecionar um aluno e exibe as notas já salvas no banco."""
    alunos = listar_alunos()
    if not alunos:
        print("Ainda não há alunos cadastrados.")
        return

    print("\nALUNOS CADASTRADOS")
    for aluno_id, nome, turma, ano_letivo in alunos:
        print(f"{aluno_id} - {nome} | {turma} ({ano_letivo})")

    ids_cadastrados = {aluno[0] for aluno in alunos}
    aluno_id = ler_inteiro("Digite o ID do aluno para consultar: ", 1)
    if aluno_id not in ids_cadastrados:
        print("Não encontrei um aluno com esse ID.")
        return

    aluno_selecionado = next(aluno for aluno in alunos if aluno[0] == aluno_id)
    _, nome, turma, ano_letivo = aluno_selecionado
    notas = consultar_notas_do_aluno(aluno_id)
    if not notas:
        print("Esse aluno ainda não tem notas cadastradas.")
        return

    _, materias, professores, avaliacoes, bimestres, valores, _ = zip(*notas)
    dados = {
        "Nome": nome,
        "Turma": turma,
        "Ano letivo": ano_letivo,
        "Quantidade de Matérias": len(notas),
        "Matérias": materias,
        "Professores": professores,
        "Avaliações": avaliacoes,
        "Bimestres": bimestres,
        "Notas": valores,
    }
    resultados = analisar_notas(valores)
    saida_dados(dados, resultados)
    exibir_medias_por_periodo(aluno_id)


def main():
    criar_banco()
    while True:
        print("\nMANAGER SCHOOL HUB")
        print("1 - Cadastrar notas de um aluno")
        print("2 - Consultar notas já cadastradas")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            dados = coletar_dados()
            aluno_id = salvar_dados_do_aluno(dados)
            resultados = analisar_notas(dados["Notas"])
            saida_dados(dados, resultados)
            print("\nDados salvos no banco manager_school.db.")
            exibir_medias_por_periodo(aluno_id)
        elif opcao == "2":
            consultar_aluno_cadastrado()
        elif opcao == "0":
            print("Até a próxima vez...")
            break
        else:
            print("Opção inválida. Escolha 1, 2 ou 0.")


if __name__ == "__main__":
    main()
