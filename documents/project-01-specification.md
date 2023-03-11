# Projeto 1 - Um simulador super básico de circuitos lógicos
Nesse projeto, cada aluno deve implementar um simulador básico de circuitos lógicos. A intenção é praticar conceitos de simulação e entender como eles podem ser implementados em código, além de ter uma visão da eficiência desses algoritmos.

## Objetivos
Para completar com sucesso esse projeto, é necessário:

Ler uma representação de código de um circuito lógico
Ler uma entrada de estímulos para o circuito
Simular o circuito
Gerar a forma de onda de saída do circuito

## Requisitos
O simulador pode ser implementado na sua linguagem de preferência. É importante que ela seja executável no computador do professor. Portanto, você deve fornecer documentação suficiente para a correta execução do código e um dockerfile para resolver toda e qualquer dependência de ambiente. Veja mais detalhes abaixo.

## Especificação do circuito
Você deve suportar a execução dos seguintes componentes lógicos:

AND: Porta lógica AND
OR: Porta lógica OR
NOT: Porta lógica NOT
NAND: Porta lógica NAND
NOR: Porta lógica NOR
XOR: Porta lógica XOR
Todos os sinais de entrada são representados por uma letra do alfabeto (A-Z). Logo, seu simulador não precisa simular mais que 26 variáveis. Cada linha de entrada será sempre da forma "variável = porta variáveis" como nos exemplos abaixo:

A = AND B C
B = OR D E
C = NOT F
D = NAND G H

### Atenção

Você pode supor que as portas lógicas tenham apenas 2 entradas, exceto a NOT que tem apenas 1 entrada. Caso seja necessário uma implementação com mais entradas, múltiplas instâncias das portas lógicas devem ser utilizadas.

### Informação

Todas as portas lógicas possuem o mesmo atraso de propagação, que é o tempo necessário para que o sinal de saída seja alterado após a alteração de uma das entradas.

### Atividade

Você deve sempre simular seu circuito com atraso 0 e atraso 1, gerando duas saídas.

## Entrada de estímulos
A entrada de estímulos é uma lista de valores para cada variável e indicadores de tempo. As variáveis possuem atribuições simples como "A = 0" ou "B = 1". Os indicadores de tempo sempre começam com um sinal + seguido por um número que indica quanto tempo precisa avançar a simulação, como "+10" que indica um avanço de 10 ciclos na simulação. Atribua zero a toda variável que não tiver valor inicial definido. Por exemplo, a entrada:

E = 1
F = 0
G = 1
H = 0
+1
F = 1
+1
G = 0
H = 1
+1
F = 0
indica que as 4 variáveis (E, F, G, H) têm seu valor inicial definido como 1, 0, 1 e 0 respectivamente. Em seguida, o tempo avança 1 unidade de tempo e o valor de F é alterado para 1. Em seguida, o tempo avança mais 1 unidade de tempo e os valores de G e H são alterados para 0 e 1 respectivamente. Em seguida, o tempo avança mais 1 unidade de tempo e o valor de F é alterado para 0.

Uma simplificação da notação acima pode ser feita aglutinando variáveis tanto do lado esquerdo quanto valores do lado direito, sempre em igual quantidade. Por exemplo, a entrada:

EFGH = 1010
+1
F = 1
+1
GH = 01
+1
F = 0
é equivalente à entrada anterior.

## Saída do simulador
A saída do simulador deve ser uma lista de valores para cada variável e indicadores de tempo. Você deve gerar um arquivo no formato csv contendo uma coluna para cada variável e uma linha para cada instante de tempo. Você deve incluir tanto as variáveis de entrada quanto as de saída, em ordem alfabética, na sua resposta. Por exemplo, a saída para a entrada anterior deve ser:

Para a saída de atraso 0:

Tempo,A,B,C,D,E,F,G,H
0,1,1,1,1,1,0,1,0
1,0,1,0,1,1,1,1,0
2,0,1,0,1,1,1,1,1
3,1,1,1,0,1,0,1,1
4,1,1,1,0,1,0,1,1
Para a saída de atraso 1:

Tempo,A,B,C,D,E,F,G,H
0,0,0,0,0,1,0,1,0
1,0,1,1,1,1,1,1,0
2,1,1,0,1,1,1,1,1
3,0,1,0,1,1,0,1,1
4,0,1,1,0,1,0,1,1
5,1,1,1,0,1,0,1,1
6,1,1,1,0,1,0,1,1
Note que a saída com atraso 1 tem mais linhas pois você deve simular até que as saídas de seu circuito fiquem estáveis. Como estamos trabalhando com circuitos sem elementos de memória, você pode considerar a saída estável quando ela não mudar em relação ao ciclo anterior e não existirem novas entradas. Note que as saidas do tempo 3 e 4 da simulação sem atraso são iguais, da mesma forma que as saídas 5 e 6 da simulação com atraso também são iguais.

## Entrega
Cada aluno deve fornecer o link para um repositório git que contenha o código fonte do simulador, um arquivo README com instruções de como executar o código. Você deve implementar um dockerfile que contenha todas as especificações para gerar seu ambiente de execução e compilar seu código (se utilizar uma linguagem compilada).

Sua árvore de entrega deve ter uma pasta chamada test que contenha sub-pastas com testes para seu circuito. Você deve executar todos os testes de todas as sub-pastas que existirem (eu incluirei mais sub-pastas durante a avaliação do projeto).

Cada sub-pasta deve conter:

Um arquivo chamado circuito.hdl com a descrição do circuito
Um arquivo chamado estimulos.txt com a entrada de estímulos
Um arquivo chamado esperado0.csv com a saída esperada para atraso 0
Um arquivo chamado esperado1.csv com a saída esperada para atraso 1
Ao executar, você deve gerar o arquivo saida0.csv com a saída da simulação com atraso 0 e saida1.csv com a saída da simulação com atraso 1.

Forneça também um arquivo chamado relatorio.pdf que contenha um relatório compacto sobre o seu projeto. O relatório deve conter:

Descrição geral do seu projeto
Descrição do seu ambiente de desenvolvimento
Descrição do seu algoritmo de simulação
Descrição de como você testou seu projeto
Considerações gerais sobre seu aprendizado nesse projeto
Colocarei uma atividade no Google Classroom para entrega do link do repositório e do relatório. A entrega deve ser feita até o dia 29/03/2023.

## Avaliação
Cada teste será considerado correto se os arquivos saida0.csv e saida1.csv forem iguais aos arquivos esperado0.csv e esperado1.csv respectivamente. Para realizar essa comparação, será utilizado o comando diff entre cada par de arquivo de saída e esperado. Você ganhará 1 ponto por comparação correta, o que equivale a 2 pontos por teste correto.

Seu dockerfile deve realizar toda a compilação e execução de todos os testes que existirem na pasta test. Lembre-se que novos testes serão incluídos na pasta antes da sua execução, portanto você não deve utilizar apenas os testes de desenvolvimento.

Sua nota nessa avaliação será dada pela seguinte fórmula:

Nota = 8 * (pontos / total de pontos) + 0,2 * nota do relatório

### Atenção

Caso necessário, o aluno será chamado para apresentar o código e explicar o funcionamento do mesmo, podendo impactar na nota acima.