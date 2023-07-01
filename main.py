ficheiro = open('C:/Users/tigol/Documents/UBI/Ai/Ficha1/dna.txt', 'r')

tabela = []
for linha in ficheiro:
    tabela.append(linha.split(','))

ficheiro.close()

novaTabela = []
novaTabela.append(['ID', 'Tamanho', 'GC'])

for i in range(len(tabela)):
    if int(tabela[i][1]) > 10:
        tamanho = 'large'
    else:
        tamanho = 'small'

    conteudo = (tabela[i][2].count('C') + tabela[i][2].count('G')) / len(tabela[i][2]) * 100

    novaTabela.append([tabela[i][0], tamanho, conteudo])

soma = 0
for i in range(1, len(novaTabela)):
    soma += novaTabela[i][2]
media = soma / (len(novaTabela) -1)
print(media)