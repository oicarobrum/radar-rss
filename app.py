import streamlit as st
import feedparser
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

SITES = {
    "CartaCapital": "https://www.cartacapital.com.br/feed/",
    "Folha de S.Paulo": "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml"
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

def gerar_nuvem_bigrama(titulos):
    if not titulos:
        st.warning("Nenhum título encontrado para gerar nuvem de palavras.")
        return [], None
    # Gera bigramas
    vectorizer = CountVectorizer(ngram_range=(2, 2), stop_words='portuguese')
    X = vectorizer.fit_transform(titulos)
    sum_words = X.sum(axis=0)
    bigram_freq = {word: sum_words[0, idx] for word, idx in vectorizer.vocabulary_.items()}
    if not bigram_freq:
        st.warning("Nenhum bigrama relevante encontrado para nuvem.")
        return [], None
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(bigram_freq)
    st.subheader("☁️ Nuvem de temas (bigramas)")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

    bigramas_ordenados = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)
    return bigramas_ordenados

st.title("📰 Radar de Notícias via RSS")

if st.button("🔄 Atualizar feed e nuvem"):
    st.experimental_rerun()

todos_titulos = []
todos_posts = []

# Lê os feeds e junta os dados
for nome, url in SITES.items():
    posts = ler_feed(url)
    todos_posts.extend(posts)
    todos_titulos.extend([p["title"] for p in posts])

# Nuvem logo no início
bigrams_list = gerar_nuvem_bigrama(todos_titulos)

# Botões para bigramas
if bigrams_list:
    st.subheader("🔎 Pesquisar por tema")
    for bigrama, freq in bigrams_list[:10]:  # mostra top 10 bigramas como botões
        if st.button(bigrama):
            st.subheader(f"Posts sobre: {bigrama}")
            encontrou = False
            for p in todos_posts:
                if bigrama.lower() in p["title"].lower():
                    st.markdown(f"- **{p['published']}** — [{p['title']}]({p['link']})")
                    encontrou = True
            if not encontrou:
                st.info("Nenhum post encontrado com esse tema.")

# Lista dos posts abaixo
for nome in SITES.keys():
    st.header(f"🌐 {nome}")
    posts_site = [p for p in todos_posts if nome in p["link"]]
    limite = 5
    for p in posts_site[:limite]:
        st.markdown(f"- **{p['published']}** — [{p['title']}]({p['link']})")
