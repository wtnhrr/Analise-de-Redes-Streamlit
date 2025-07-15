# 🔗 Ragnarok Network Analysis

Uma aplicação interativa desenvolvida com [Streamlit](https://streamlit.io/) que permite analisar e visualizar redes complexas de **monstros e itens** do MMORPG **Ragnarok Online**, utilizando dados da [RagnAPI](https://ragnapi.com/).

> **👾 Nós:** Monstros e Itens  
> **🔗 Arestas:** Relação de drop (monstro → item)

---

## 🎯 Funcionalidades

- 🔎 **Filtragem interativa** por ID, nível, raça, tipo (normal/boss) e elemento
- 🌐 **Grafo interativo** com visualização Pyvis
- 📍 **Tabela de mapas e spawns** dos monstros
- 📊 **Métricas estruturais** da rede:
  - Densidade
  - Assortatividade
  - Coeficiente de clustering
  - Componentes Fortemente e Fracamente Conectados
- 📈 **Histograma da distribuição de grau**
- ⭐ **Centralidade dos nós** com ranking top-k:
  - Degree
  - Closeness
  - Betweenness
  - Eigenvector

---

## 📦 Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/Analise-de-Redes-Streamlit.git
cd Analise-de-Redes-av2
pip install -r requirements.txt
streamlit run main.py
```

---

Link Cloud:
[Streamlit Cloud](https://ragnarok-network-analysis.streamlit.app)
