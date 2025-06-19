import streamlit as st
import feedparser
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

SITES = {
    "UOL": "https://www.uol.com.br/feed.xml",
    "CartaCapital": "https://www.cartacapital.com.br/feed/",
    "Folha de S.Paulo": "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml",
    "G1": "https://g1.globo.com/rss/g1/",
    "El País Brasil": "https://brasil.elpais.com/rss/brasil/"
}

def ler_feed(url):
    feed = feedparser.parse(url)
    posts = []
    for entry in feed.entries:
        posts.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", "Data não disponível")
        })
    return posts

def gerar_nuvem_e_palavras(titulos):
    if not titulos:
        st.warning("Nenhum título encontrado para gerar a nuvem de palavras.")
        return [], None
    texto = " ".join(titulos)
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(width=800, height=400, background_color='white',
                          stopwords=stopwords).generate(texto)
    st.subheader("☁️ Nuvem de palavras (todos os sites)")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

    # Gera lista de palavras da nuvem para os botões
    palavras_frequentes = wordcloud.words_.keys()
    return palavras_frequentes, wordcloud

st.title("📰 Radar de Notícias via RSS")

if st.button("🔄 Atualizar feed e nuvem"):
    st.experimental_rerun()

todos_titulos = []
todos_posts = []

for nome, url in SITES.items():
    st.header(f"🌐 {nome}")
    posts = ler_feed(url)
    if not posts:
        st.warning(f"Nenhum post encontrado para {nome}.")
        continue

    mostrar_mais = st.session_state.get(f"show_more_{nome}", False)
    limite = 5 if not mostrar_mais else len(posts)

    for i, p in enumerate(posts[:limite]):
        st.markdown(f"- **{p['published']}** — [{p['title']}]({p['link']})")
        todos_titulos.append(p["title"])
        todos_posts.append(p)

    if not mostrar_mais and len(posts) > 5:
        if st.button(f"📂 Ler mais de {nome}"):
            st.session_state[f"show_more_{nome}"] = True
            st.experimental_rerun()

# Gera nuvem + lista de palavras
palavras_frequentes, _ = gerar_nuvem_e_palavras(todos_titulos)

# Botões interativos para palavras
if palavras_frequentes:
    st.subheader("🔎 Pesquisar por palavra")
    for palavra in list(palavras_frequentes)[:20]:  # Limita número de botões
        if st.button(palavra):
            st.subheader(f"Posts que contêm: {palavra}")
            encontrou = False
            for p in todos_posts:
                if palavra.lower() in p["title"].lower():
                    st.markdown(f"- **{p['published']}** — [{p['title']}]({p['link']})")
                    encontrou = True
            if not encontrou:
                st.info("Nenhum post encontrado com essa palavra.")
