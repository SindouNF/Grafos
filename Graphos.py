from math import sqrt

import argparse, time

########################################################################

class heap:

    def __init__(self, vet):

        self.h = vet

        for i in range(int((len(vet) - 1) / 2), -1, -1):

            self.heapify(i)



    def pai(self, i):

        return int((i - 1) / 2)

    def esq(self, i):

        return 2 * i + 1

    def dir(self, i):

        return 2 * i + 2



    def pop(self):

        self.h[0], self.h[-1] = self.h[-1], self.h[0]

        ret = self.h.pop()

        self.heapify(0)



        return ret



    def heapify(self, i):

        esq = self.esq(i)

        dir = self.dir(i)

        maior = i

        if (esq < len(self.h) and (self.h[esq] > self.h[i])):

            maior = esq

        if (dir < len(self.h) and (self.h[dir] > self.h[maior])):

            maior = dir

        if maior != i:

            self.h[i], self.h[maior] = self.h[maior], self.h[i]

            self.heapify(maior)

    

    def empty(self):

        return len(self.h) == 0



def heapsort(lista):

    lista_ord = []

    h = heap(lista)

    while not h.empty():

        lista_ord.append(h.pop())

    return lista_ord

########################################################################

class regiao:

    def __init__(self, vertices): # vertices = posicao do vertice no grafo

        self.vertices = vertices

        self.demanda = 0

    def __gt__(self, other):

        return self.demanda > other.demanda

    def set_demanda(self, demanda):

        self.demanda = demanda

########################################################################

class vertice:

    def __init__(self, x, y):

        self.x, self.y = x, y

        self.indice = None

    def get_coord(self):

        return self.x, self.y

    def set_ind(self, ind):

        self.indice = ind

########################################################################

class grafo:

    def __init__(self):

        # criando lista e adicionando origem no vertice 0

        # vertice 0 nao sera utilizado

        self.vertices = [vertice(0, 0)]

        self.vertices[0].set_ind(0)

        # criando matriz de incidencia, sem inicializar

        self.inc = []

        self.regioes = []

    

    def add_vertice(self, x, y):

        v = vertice(x, y)

        v.set_ind(len(self.vertices))

        self.vertices.append(v)



    def ajustar_arestas(self):

        for i in range(len(self.vertices)):

            incid = [0] * len(self.vertices)

            for j in range(len(incid)):

                if i != j:

                    x1, y1 = self.vertices[i].get_coord()

                    x2, y2 = self.vertices[j].get_coord()

                    incid[j] = calc_distancia(x1, x2, y1, y2)

            self.inc.append(incid)



    def add_regiao(self, lista):

        reg = regiao(lista)

        self.regioes.append(reg) 

            

    def exibir_incid(self):

        for i in self.inc:

            for j in i:

                print("%.2f" %j, end = '\t')

            print()



    def size(self):

        return len(self.vertices)



def first_fit_decrescente(g, capacidade, num_veiculos):

    # p/ escolher regioes

    # p/ cada carro, escolhe as regioes de g que melhor

    # se encaixam de acordo com a capacidade do carro

    # cada carro vai ter uma lista de regioes

    # exemplo

    # carro 1 - passa regiao 1 6

    # carro 2 - passa regiao 3 5

    # carro 3 - passa regiao 4 2

    # retorna uma lista de lista de regioes

    # p cada lista de regioes, aplicar prim p/ gerar agm

    # e ter um conjunto de arestas

    g.regioes = [regiao for regiao in g.regioes if regiao.demanda != 0]

    g.regioes = heapsort(g.regioes)

    

    veiculos = []

    for _ in range(num_veiculos):

        # posicao 0 eh a capacidade do veiculo

        # posicao 1 eh a lista de regioes que ele visitara

        veiculos.append([capacidade, []])

    

    while g.regioes:

        regiao = g.regioes[0]

        for i in range(len(veiculos)):

            if regiao.demanda < veiculos[i][0]:

                veiculos[i][0] -= regiao.demanda

                veiculos[i][1].append(regiao)

                break

        g.regioes.pop(0)

    # no final, retorna uma lista de listas com as regioes que cada veiculo visitara

    return [veiculos[i][1] for i in range(num_veiculos)]



def prim_mod(g, regioes):

    # escolhe um vertice por regiao

    # e usa esse vertice pra colocar na AGM

    # retorna a AGM e o custo da AGM

    soma = 0

    conj_arestas = []

    conj_vert = [1]

    while len(regioes) > 0:

        vert = None

        aresta = None

        regiao = None

        for x in range(0, len(regioes)): # i eh o regiao

            i = regioes[x]

            min = g.inc[g.vertices[i.vertices[0]].indice][conj_vert[0]]

            vert = g.vertices[i.vertices[0]].indice

            aresta = (g.vertices[i.vertices[0]].indice, conj_vert[0])

            regiao = x

            for j in conj_vert:

                for k in range (1,len(i.vertices)):

                    if g.inc[g.vertices[i.vertices[k]].indice][j] < min:

                        min = g.inc[g.vertices[i.vertices[k]].indice][j]

                        vert = j

                        aresta = (g.vertices[i.vertices[k]].indice, j)

                        regiao = x

            

        conj_vert.append(vert)

        regioes.pop(regiao)



        conj_arestas.append(aresta)

        soma += min

    return conj_arestas, soma



def hierholzer_mod(agm):

    c_euler = []

    vert_usados = []

    for i in range(len(agm)):

        if (agm[i][0] == 1):

            c_euler.append(agm[i])

            agm.pop(i)

            break

    i = 0

    while len(agm):

        # se o vertice ja foi usado, prox iteracao

        if c_euler[i][1] in vert_usados:

            i += 1

            continue

        j = 0

        while j < len(agm):

            if (c_euler[i][1] == agm[j][0]):

                c_euler.insert(i + 1, agm[j])

                agm.pop(j)

            else:

                j += 1

        vert_usados.append(c_euler[i][1])

        i += 1

    return c_euler



def encontrar_melhor_agm_regiao(g, regioes_visitadas):

    # ideia: encontramos um padrao em que o custo da AGM que começa de um vertice X

    # depende apenas do vertice X, independente da ordem dos demais vertices e como

    # eles se apresentam

    # [0, 1, 2, 3] e [0, 3, 2, 1] então teriam o mesmo custo

    # o que essa funcao faz: calcula uma agm p/ cada variacao das regioes visitadas

    lista_agms = []

    for rota_regioes in regioes_visitadas:

        comb_rota_regioes = [rota_regioes]

        i = 0

        while len(comb_rota_regioes) != len(rota_regioes):

            ll = []

            for j in range(len(comb_rota_regioes[i])):

                ll.append(comb_rota_regioes[i][(j + 1) % len(comb_rota_regioes[i])])

            comb_rota_regioes.append(ll)

            i += 1

        agm, min_custo = prim_mod(g, comb_rota_regioes[0])

        comb_rota_regioes.pop(0)

        for rota in comb_rota_regioes:

            agm_nova, custo_novo = prim_mod(g, rota)

            if custo_novo < min_custo:

                agm, min_custo = agm_nova, custo_novo

        lista_agms.append(agm)

    return lista_agms



def eulerizar_agms(lista_agms):

    # duplica todas as arestas

    # p calcular RSL

    for agm in lista_agms: 

        size_agm = len(agm)

        for i in range(size_agm):

            agm.append((agm[i][1], agm[i][0]))

    return lista_agms



def rsl(lista_euler):

    lista_rotas = []

    for c in lista_euler:

        lista_vertices = []

        for arestas in c:

            if arestas[0] not in lista_vertices:

                lista_vertices.append(arestas[0])

        lista_rotas.append(lista_vertices)

    return lista_rotas

            

def calcula_rotas(g, regioes_visitadas):

    # gera uma agm pra cada carro

    # carro 1 visita as regioes 1 e 3, por exemplo

    # vai gerar uma agm que passa em um vertice da regiao 1, 3 e na origem

    # duplicar arestas p/ cada agm - codigo abaixo

    # aplicar hierholzer, pois estara eulerizada

    # e depois achar tsp pelo resultado de hierholzer

    lista_agms = encontrar_melhor_agm_regiao(g, regioes_visitadas)

    lista_agms = eulerizar_agms(lista_agms)

    lista_euler = [hierholzer_mod(agm) for agm in lista_agms]

    lista_rotas = rsl(lista_euler)



    soma = 0

    for rota in lista_rotas:

        for i in range(0, len(rota), 1):

            soma += g.inc[rota[i]][rota[(i + 1) % len(rota)]]

    return lista_rotas, soma

########################################################################

def calc_distancia(x1, x2, y1, y2):

    return sqrt((x2-x1)**2 + (y2-y1)**2)



def main():

    start = time.time()



    parser = argparse.ArgumentParser()

    parser.add_argument("-i", help="Arquivo para entrada de dados")

    parser.add_argument("-o", help="Arquivo para saida de dados")

    parser.add_argument("-sol", help="Opcao para gerar solucao")

    

    args = parser.parse_args()

    

    if args.i:

        entrada = open(args.i, "r")

    

    if args.o:

        saida = open(args.o, "a+")

    

    g = grafo()

    

    #chaves booleanas auxiliares

    vert = False

    reg = False

    dem = False

    

    if entrada:

        for linha in entrada :

            linha = list(linha.split())

            #pedido de dimensao

            if linha[0] == "DIMENSION" :

                _ = int(linha[2])

            

            #veiculos disponiveis

            elif linha[0] == "VEHICLES" :

                veiculos = int(linha[2])

            

            #quantidade de regioes

            elif linha[0] == "SETS" :

                _ = int(linha[2])

            

            #capacidade do veiculo

            elif linha[0] == "CAPACITY" :

                capacidade = int(linha[2])

            

            #da inicio a entrada de vertices

            elif linha[0] == "NODE_COORD_SECTION" :

                vert = True

            

            #interrompe entrada de vertice, ajustando arestas

            #da inicio a entrada de regioes



            elif linha[0] == "SET_SECTION" :

                vert = False

                reg = True



            #interrompe entrada de regioes

            #da inicio a entrada de demandas

            



            elif linha[0] == "DEMAND_SECTION" :

                reg = False

                dem = True

            

            elif linha[0] == "EOF":

                break



            #pede as coord dos vertices e os insere no grafo

            elif vert :

                x, y = int(linha[1]), int(linha[2])

                g.add_vertice(x,y)



            #pede regiao, armazenando numa lista de vertices

            #adiciona a lista no grafo

            elif reg :

                r = []

                

                c = 1

                

                #elimina o primeiro e o ultimo termo da lista

                while int(linha[c]) != -1 :

                    r.append(int(linha[c]))

                    c += 1

                

                g.add_regiao(r)



            #recebe a demanda e insere

            elif dem :

                g.regioes[int(linha[0]) - 1].set_demanda(int(linha[1]))

        # apos ler regioes, criar a matriz de incidencias

        g.ajustar_arestas()

        

        #lista de listas de regioes, veiculo na pos 0 visita a lista na pos 0

        regioes_visitadas = first_fit_decrescente(g, capacidade, veiculos)

        rotas, soma = calcula_rotas(g, regioes_visitadas)

        entrada.close()

    else :

         print("Erro na leitura do arquivo!")

         exit()





    end = time.time()

    if args.sol:

        saida_sol = open(args.sol, "w+")

        for i in rotas:

            s = ' '.join(map(str, i))

            saida_sol.write(s + "\n")

        saida_sol.close()

    

    """"

    bkv = int(input())

    desvio = ((soma - bkv) / bkv) * 100

    print(desvio)

    """

    

    saida.write("%s %.2f %.4f\n" %(args.i, soma, end - start))

    saida.close()



if __name__ == "__main__":

	main()
