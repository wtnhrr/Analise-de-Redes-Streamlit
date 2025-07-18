# Análise de Redes em Ragnarok Online (Monstros e Itens)

Este projeto realiza uma análise exploratória e crítica de redes complexas utilizando dados do jogo **Ragnarok Online**, especificamente dos monstros e suas relações com itens dropados, mapas e outras características.

---

## Dataset

O dataset utilizado é o arquivo JSON `monster_cache.json` gerado pelo streamlit, que contém informações detalhadas sobre os monstros, incluindo:
- ID e nome do monstro
- Nível e tipo elemental
- Itens dropados
- Mapas onde aparecem

---

## Construção da Rede

- Cada **nó** representa um monstro.
- As **arestas** representam conexões baseadas em drops compartilhados entre monstros.
- Foi criado um grafo direcionado, posteriormente analisado como não direcionado para certas métricas.

---

## Análises Realizadas

### 1. Estrutura da Rede

- Número de nós: 91
- Número de arestas: 843
- Extraído o maior subgrafo fortemente conectado para análises mais confiáveis.

### 2. Métricas Estruturais

- **Densidade:** 0.20 (rede relativamente densa)
- **Diâmetro:** 4 (distância máxima curta entre nós)
- **Clusterização Média:** 0.53 (alta modularidade, presença de comunidades)
- **Distribuição de Grau:** variada, com alguns hubs muito conectados.

### 3. Centralidades

Foram calculadas e analisadas as principais centralidades, destacando os nós mais influentes:

| Métrica           | Exemplo de Top Nós              |
|-------------------|--------------------------------|
| Degree Centrality  | muka, soldier_skeleton, ghoul  |
| Closeness         | soldier_skeleton, ghoul, argos |
| Betweenness       | shining_plant, ghoul, swordfish|
| Eigenvector       | muka, soldier_skeleton, thief_bug |

### 4. Detecção de Comunidades (Algoritmo Louvain)

- Foram detectadas 6 comunidades principais.
- A maior comunidade contém 24 nós.
- As comunidades refletem agrupamentos naturais baseados nas conexões de drops e mapas.

### 5. Comparação com Modelos de Redes Clássicas

Foram criados e comparados modelos de redes sintéticas para analisar as propriedades da rede real:

| Modelo             | Clusterização | Caminho Médio | Grau Médio |
|--------------------|---------------|---------------|------------|
| Rede Real          | 0.53          | 1.95          | 18.52      |
| Erdős-Rényi (ER)   | 0.20          | 1.83          | 17.67      |
| Small-World (SW)   | 0.34          | 4.40          | 4.00       |
| Barabási-Albert(BA)| 0.18          | 2.75          | 3.91       |

A rede real apresenta características híbridas entre Small-World e Barabási-Albert, com alta densidade e forte clusterização.

### 6. Resiliência da Rede

- Remoção de 10% dos nós, aleatória ou dirigida pelos nós de maior grau, **não alterou o diâmetro da rede (permaneceu 4)**.
- Isso indica uma rede robusta, tolerante a falhas e ataques direcionados.

### 7. Link Prediction

- Foram previstas novas possíveis conexões entre monstros com scores entre ~0.49 e 0.63.
- Destacam-se pares envolvendo o monstro 1031 como potencial hub de novas conexões.
- Essas previsões podem indicar relações ocultas ou ainda não exploradas entre os monstros.

---

## Como usar

1. Clone o repositório.
2. Garanta que o dataset `monster_cache.json` esteja na pasta raiz.
3. Execute o notebook `analise_redes_ragnarok.ipynb` para acompanhar o pipeline completo.
4. Instale as dependências necessárias: