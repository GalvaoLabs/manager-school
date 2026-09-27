# Análise de Notas

# Importação da função mean
from statistics import mean

# Constantes
NOTA_MINIMA = 0
NOTA_MAXIMA = 10
MEDIA_APROVACAO = 6
MEDIA_RECUPERACAO = 5
QUANT_MIN_MATERIAS = 1

# Função de Coleta de Dados
def coletar_dados():
    aluno = input("Qual o nome do aluno? ")

    valido = False
    while not valido:
        try: 
            quant_materias = int(input("Digite a quantidade de matérias que deseja adicionar: "))
            if quant_materias >=QUANT_MIN_MATERIAS:
                valido = True

            else:
                print(f"Digite uma quantidade maior ou igual a {QUANT_MIN_MATERIAS}")

        except ValueError:
            print("Entrada inválida! Digite uma quantidade de matéria numérica.")
            valido = False


    materias = []
    notas = []

    for i in range(quant_materias):
        materia = input("Digite a matéria que deseja adicionar: ")
        valido = False
        while not valido:
            try:
                nota = float(input("Digite a nota dessa matéria: "))
                if NOTA_MINIMA <= nota <= NOTA_MAXIMA:
                    materias.append(materia)
                    notas.append(nota)
                    valido = True

                else:
                    print(f"Digite uma nota de {NOTA_MINIMA} a {NOTA_MAXIMA}")
            except ValueError:
                print("Entrada inválida! Digite uma nota numérica.")
                valido = False

    dados = {
    "Nome": aluno,
    "Quantidade de Matérias": quant_materias,
    "Matérias": materias,
    "Notas": notas
}
    return dados

# Função da Análise de Notas
def analisar_notas(notas):
    media = mean(notas)
    maior_nota = max(notas)
    menor_nota = min(notas)
    quant_notas_media_aprovacao = sum(nota >=MEDIA_APROVACAO for nota in notas)
    quant_notas_media_reprovacao = sum(nota <MEDIA_APROVACAO for nota in notas)

    # Situação Final
    if media >= MEDIA_APROVACAO:
        situacao = "Aprovado"

    elif media >= MEDIA_RECUPERACAO:
        situacao = "Recuperação"

    else:
        situacao = "Reprovado"

    resultados = {
    "Média": media,
    "Maior Nota": maior_nota,
    "Menor Nota": menor_nota,
    "Quantidade de Notas Azuis": quant_notas_media_aprovacao,
    "Quantidade de Notas Vermelhas": quant_notas_media_reprovacao,
    "Situação": situacao
}
    return resultados

# Função da Saída de Dados
def saida_dados(dados, resultados):
    print("="*50)
    print("\nANÁLISE DE NOTAS\n")
    print("="*50)
    print(f"\n\nAluno: {dados['Nome']}")
    print(f"\nQuantidade de matérias: {dados['Quantidade de Matérias']}")
    print("\n\nMatérias:")
    for materia, nota in zip(dados['Matérias'], dados["Notas"]):
        print(f"- {materia}: {nota}")
    print("\n\n","-"*50)
    print(f"\nMédia: {resultados['Média']:.2f}")
    print(f"\nMaior nota: {resultados['Maior Nota']:.2f}")
    print(f"\nMenor nota: {resultados['Menor Nota']:.2f}")
    print(f"\n\nQuantidade de Notas Azuis: {resultados['Quantidade de Notas Azuis']}")
    print(f"\nQuantidade de Notas Vermelhas: {resultados['Quantidade de Notas Vermelhas']}")
    print(f"\n\nSituação: {resultados['Situação']}\n")
    print("="*50)

def main():
    encerrar = False
    while not encerrar:
        dados = coletar_dados()
        resultados = analisar_notas(dados['Notas'])
        saida_dados(dados, resultados)
        repeticao_resposta = input("Deseja analisar outro aluno? (s/n)")
        if repeticao_resposta == "n":
            print("Até a próxima vez...")
            encerrar = True
        elif repeticao_resposta == "s":
            encerrar = False
        else:
            print("Digite apenas s ou n")
main()