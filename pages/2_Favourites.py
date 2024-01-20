import streamlit as st

# st.set_page_config(layout="wide") 

# Header
# st.header("A *chronological* list of things I like.")
header_text = 'A chronological list of things I find, I see, I like.'
s = f"<p style='font-size:32px; font-weight:normal; font-family:IBM Plex Sans'>{header_text}</p>"
st.markdown(s, unsafe_allow_html=True)

#######

st.divider()
st.markdown(
    "<p style='font-size:14px; font-weight:normal; font-family:IBM Plex Sans'>20/01/2024</p>",
    unsafe_allow_html=True
    )
s = f"<p style='font-size:18px; font-weight:bold; font-family:IBM Plex Sans'>SOFA (Start Often Finish rArely)</p>"
st.markdown(s, unsafe_allow_html=True)
input_text = """
Nothing is fixed, nothing is permanent, and nothing lasts.
This is true of all things, including your ideas of self and identity.
Want to be somebody who knows how to cook, or code in Lisp?
Or somebody who knows how to rollerblade, or only eats plants, or worships the moon?
Just start doing those things and then, poof! Now you are that person.
If you find out your new self doesn't suit you, just stop being that person and be someone else.
Be as many different people and do as many different things as you want.
Start often. You don't have to commit your entire life to any one thing. Finish rarely.
"""
s = f"<p style='font-size:12px; font-weight:normal; font-family:IBM Plex Sans'>{input_text}</p>"
st.markdown(s, unsafe_allow_html=True)
st.markdown('[source URL](https://tilde.town/~dozens/sofa/?utm_source=substack&utm_medium=email)')

st.divider()
st.markdown(
    "<p style='font-size:14px; font-weight:normal; font-family:IBM Plex Sans'>19/01/2024</p>",
    unsafe_allow_html=True
    )
s = f"<p style='font-size:18px; font-weight:bold; font-family:IBM Plex Sans'>Lentamente muore (Martha Medeiros)</p>"
st.markdown(s, unsafe_allow_html=True)
poesia = """
    Lentamente muore chi diventa schiavo dell’abitudine,
    ripetendo ogni giorno gli stessi percorsi,
    chi non cambia la marcia,
    chi non rischia e cambia colore dei vestiti,
    chi non parla a chi non conosce.

    Muore lentamente
    chi evita una passione,
    chi preferisce il nero al bianco
    e i puntini sulle “i”
    piuttosto che un insieme di emozioni,
    proprio quelle che fanno brillare gli occhi,
    quelle che fanno di uno sbadiglio un sorriso,
    quelle che fanno battere il cuore
    davanti all’errore e ai sentimenti.
    
    Lentamente muore
    chi non capovolge il tavolo
    quando è infelice sul lavoro,
    chi non rischia la certezza per l’incertezza
    per inseguire un sogno,
    chi non si permette almeno una volta nella vita,
    di fuggire ai consigli sensati.
    
    Lentamente muore
    chi non viaggia,
    chi non legge,
    chi non ascolta musica,
    chi non trova grazia in se stesso.
    
    Muore lentamente
    chi distrugge l’amor proprio,
    chi non si lascia aiutare
    chi passa i giorni a lamentarsi
    della propria sfortuna o della pioggia incessante.
    
    Lentamente muore
    chi abbandona un progetto prima di iniziarlo,
    chi non fa domande sugli argomenti che non conosce
    o non risponde quando gli chiedono qualcosa che conosce.
    
    Evitiamo la morte a piccole dosi,
    ricordando sempre che essere vivo
    richiede uno sforzo di gran lunga maggiore
    del semplice fatto di respirare.
    
    Soltanto l’ardente pazienza
    porterà al raggiungimento di una splendida felicità.
"""
st.code(poesia, language='c')


st.divider()
st.markdown("- [Data Memos](https://medium.com/@giorgialupi/data-memos-3927ab7e822a) by Giorgia Lupi and Paolo Ciuccarelli")
st.markdown("- Consequently, the person who is most likely to get new ideas is a person of good background in the field of interest and one who is unconventional in his habits. (To be a crackpot is not, however, enough in itself.) *– From a 1959 [Essay](https://www.technologyreview.com/2014/10/20/169899/isaac-asimov-asks-how-do-people-get-new-ideas/) by Isaac Asimov on Creativity*")
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown('- Flatlandia (IT)')
    st.video("https://youtu.be/tNDhjYQKWt4?si=Nz_P00ESET4IoX-z")
    st.markdown('- Visualization of PI being irrational')
    st.video("https://www.youtube.com/watch?v=S32sIhukA9E&t=2s")
with col2:
    st.markdown('- About popcorn and creativity (IT)')
    st.video("https://www.youtube.com/watch?v=Vv-cFqfM8GQ")
    st.markdown('- Same stats different graphs')
    st.video("https://www.youtube.com/watch?v=It4UA75z_KQ")

