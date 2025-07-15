import streamlit as st
import requests
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from pyvis.network import Network
import streamlit.components.v1 as components
import os
import json


# CONFIGURAÇÃO


st.set_page_config(page_title="Ragnarok Network Analysis", layout="wide")
st.title("🔗 Ragnarok Online - Análise de Redes de Monstros e Itens")

st.markdown("""
Aplicativo para explorar a rede de monstros e itens do **Ragnarok Online** usando dados da **RagnAPI**.

**👾 Nós:** Monstros e Itens  
**🔗 Arestas:** Relação "dropa" (monstro → item)

Use os filtros para refinar a rede!

Apos refina os filtros, clique em "Gerar grafo" para montar a rede.
A primeira vez pode demorar um pouco, mas os dados serão armazenados em cache para buscas futuras.
""")


# CACHE JSON

CACHE_PATH = "monster_cache.json"

if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, "r") as f:
        monster_cache = json.load(f)
else:
    monster_cache = {}

def get_monster_with_disk_cache(monster_id):
    str_id = str(monster_id)
    if str_id in monster_cache:
        return monster_cache[str_id]

    url = f"https://ragnapi.com/api/v1/re-newal/monsters/{monster_id}"
    resp = requests.get(url)
    if resp.status_code == 200:
        try:
            raw = resp.json()
            processed = {
                "id": monster_id,
                "name": raw.get("monster_info", f"Monster {monster_id}"),
                "level": int(raw.get("main_stats", {}).get("level", 0)),
                "race": raw.get("race", "").lower(),
                "type": raw.get("type", "").lower(),
                "maps": [
                    {"name": m.get("name", "Desconhecido"), "amount": m.get("amount", 0)}
                    for m in raw.get("maps", [])
                ],
                "elementalDamage": raw.get("elementalDamage", {}),
                "drops": [d.get("name", "Item desconhecido") for d in raw.get("drops", [])]
            }
            monster_cache[str_id] = processed
            with open(CACHE_PATH, "w") as f:
                json.dump(monster_cache, f)
            return processed
        except Exception:
            return None
    return None


# PARÂMETROS

st.sidebar.header("🔍 Parâmetros de Busca")

start_id = st.sidebar.number_input("ID inicial do monstro", min_value=1000, value=1000)
end_id = st.sidebar.number_input("ID final do monstro", min_value=start_id, value=start_id + 100)

nivel_min = st.sidebar.number_input("Level mínimo", min_value=1, value=1)
nivel_max = st.sidebar.number_input("Level máximo", min_value=1, value=999)

racas = ['formless', 'undead', 'brute', 'plant', 'insect', 'fish', 'demon', 'demihuman', 'angel', 'dragon']
tipos = ['normal', 'boss', 'shadow']
elementos = ['neutral', 'poison', 'earth', 'shadow', 'water', 'undead', 'fire', 'holy', 'wind', 'ghost']

filtro_raca = st.sidebar.selectbox("Raça", [''] + racas)
filtro_tipo = st.sidebar.selectbox("Tipo", [''] + tipos)
filtro_elemento = st.sidebar.selectbox("Elemento (fraqueza)", [''] + elementos)

if "executar" not in st.session_state:
    st.session_state.executar = False

if st.sidebar.button("🔄 Gerar grafo"):
    st.session_state.executar = True

if not st.session_state.executar:
    st.stop()


# PROCESSANDO DADOS

st.subheader("🧬 Processando Dados...")

G = nx.DiGraph()
mapas = {}
ids_nao_encontrados = []

progress = st.progress(0)
total = end_id - start_id + 1

for count, monster_id in enumerate(range(start_id, end_id + 1)):
    data = get_monster_with_disk_cache(monster_id)
    progress.progress((count + 1) / total)

    if not data:
        ids_nao_encontrados.append(monster_id)
        continue

    monster_name = data["name"]
    level = data["level"]
    race = data["race"]
    tipo = data["type"]
    elementos = data["elementalDamage"]
    mapa_list = data["maps"]
    drops = data["drops"]

    if not (nivel_min <= level <= nivel_max):
        continue
    if filtro_raca and race != filtro_raca:
        continue
    if filtro_tipo and tipo != filtro_tipo:
        continue
    if filtro_elemento and filtro_elemento not in elementos:
        continue

    mapa_names = [m["name"] for m in mapa_list]
    mapa_display = ', '.join(mapa_names) if mapa_names else 'Desconhecido'

    G.add_node(monster_name, tipo='monstro', mapa=mapa_display)

    for m in mapa_names:
        mapas[m] = mapas.get(m, 0) + 1

    for item_name in drops:
        G.add_node(item_name, tipo='item')
        G.add_edge(monster_name, item_name, tipo='dropa')

st.success(f"Grafo montado com {G.number_of_nodes()} nós e {G.number_of_edges()} arestas.")

st.session_state["grafo_final"] = G

# TABELA DETALHADA DE MAPAS

st.subheader("📍 Distribuição de Monstros por Mapa")

mapa_detalhado = []
ids_nao_encontrados_mapa = []

for monster_id in range(start_id, end_id + 1):
    data = get_monster_with_disk_cache(monster_id)
    if not data:
        ids_nao_encontrados_mapa.append(monster_id)
        continue

    monster_name = data["name"]
    for m in data["maps"]:
        mapa_detalhado.append({
            'Mapa': m["name"],
            'Monstro': monster_name,
            'Quantidade de Spawns': m["amount"]
        })

if mapa_detalhado:
    mapa_df_detalhado = pd.DataFrame(mapa_detalhado)
    st.dataframe(mapa_df_detalhado)
else:
    st.write("Nenhum dado de mapa encontrado.")


# VISUALIZAÇÃO INTERATIVA

st.subheader("🌐 Visualização Interativa da Rede")

if G.number_of_nodes() > 0:
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")

    for node, data in G.nodes(data=True):
        if data['tipo'] == 'monstro':
            net.add_node(node, label=node, color='red', shape='circle', title=f"Mapa: {data.get('mapa', 'Desconhecido')}")
        else:
            net.add_node(node, label=node, color='blue', shape='box')

    for origem, destino, data in G.edges(data=True):
        net.add_edge(origem, destino, label=data['tipo'])

    net.repulsion(node_distance=250, spring_length=200)
    components.html(net.generate_html(), height=700)
else:
    st.warning("Nenhum dado para gerar o grafo.")


# ANÁLISE DA REDE

if G.number_of_nodes() > 0:
    st.subheader("📊 Métricas Estruturais")

    densidade = nx.density(G)
    assort = nx.degree_assortativity_coefficient(G) if G.number_of_edges() > 0 else 0
    clustering = nx.average_clustering(G.to_undirected())

    fortes = nx.number_strongly_connected_components(G)
    fracos = nx.number_weakly_connected_components(G)

    st.markdown(f"""
    - **Densidade:** {densidade:.4f}  
    - **Assortatividade:** {assort:.4f}  
    - **Coeficiente de Clustering:** {clustering:.4f}  
    - **Componentes Fortemente Conectados:** {fortes}  
    - **Componentes Fracamente Conectados:** {fracos}  
    """)

    st.subheader("📊 Distribuição de Grau")
    graus = [d for n, d in G.degree()]
    fig, ax = plt.subplots()
    ax.hist(graus, bins=15, color='skyblue', edgecolor='black')
    ax.set_title('Distribuição de Grau')
    ax.set_xlabel('Grau')
    ax.set_ylabel('Frequência')
    st.pyplot(fig)


# CENTRALIDADE DOS NÓS

with st.expander("⭐ Centralidade dos Nós", expanded=False):
    # Use um form para conter sliders e botão
    with st.form(key="form_centralidade"):
        k = st.slider("Top‑k nós", min_value=3, max_value=20, value=5, key="central_k")
        opcao = st.selectbox("Centralidade:", 
                              ["Degree", "Closeness", "Betweenness", "Eigenvector"],
                              key="central_opcao")
        calcular = st.form_submit_button("🔄 Calcular Centralidade")

    if calcular:
        G_local = st.session_state.get("grafo_final", None)
        if G_local is None:
            st.warning("Grafo ainda não foi gerado. Use filtros e clique em 'Gerar grafo'.")
        else:
            try:
                if opcao == "Degree":
                    centralidade = nx.degree_centrality(G_local)
                elif opcao == "Closeness":
                    centralidade = nx.closeness_centrality(G_local)
                elif opcao == "Betweenness":
                    centralidade = nx.betweenness_centrality(G_local)
                else:  # Eigenvector
                    centralidade = nx.eigenvector_centrality(G_local)

                df_central = pd.DataFrame(centralidade.items(), columns=["Nó","Centralidade"])
                df_central = df_central.sort_values("Centralidade", ascending=False).head(k)
                st.table(df_central)
            except nx.NetworkXException:
                st.warning("❌ Eigenvector não convergiu.")
