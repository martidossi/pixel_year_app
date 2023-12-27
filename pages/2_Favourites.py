import streamlit as st

st.markdown("📌  **A general collection of links, pages, projects that I like:**")
st.markdown("- [Data Memos](https://medium.com/@giorgialupi/data-memos-3927ab7e822a) by Giorgia Lupi and Paolo Ciuccarelli")
st.markdown("- Consequently, the person who is most likely to get new ideas is a person of good background in the field of interest and one who is unconventional in his habits. (To be a crackpot is not, however, enough in itself.) *– From a 1959 [Essay](https://www.technologyreview.com/2014/10/20/169899/isaac-asimov-asks-how-do-people-get-new-ideas/) by Isaac Asimov on Creativity*")
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown('- Flatlandia (IT)')
    st.video("https://youtu.be/tNDhjYQKWt4?si=Nz_P00ESET4IoX-z")
with col2:
    st.markdown('- About popcorn and creativity (IT)')
    st.video("https://www.youtube.com/watch?v=Vv-cFqfM8GQ")