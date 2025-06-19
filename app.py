import streamlit as st
import feedparser
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Lista dos feeds
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
            "link": entry.link
        })
    return posts

def gerar_nuvem(titulos):
    if not titulos:
        st.warning("Nenhum título encontrado para gerar a nuvem de palavras.")
        return
    texto = " ".join(titulos)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto)
    st.subheader("☁️ Nuvem de palavras (todos os sites)")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

st.title("📰 Radar de Notícias via RSS")

todos_titulos = []

for nome, url in SITES.items():
    st.header(f"🌐 {nome}")
    posts = ler_feed(url)
    for p in posts:
        st.markdown(f"- [{p['title']}]({p['link']})")
        todos_titulos.append(p["title"])

gerar_nuvem(todos_titulos)
