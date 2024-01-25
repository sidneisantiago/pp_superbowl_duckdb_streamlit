import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import duckdb 

con = duckdb.connect(database= 'data/superbowl.duckdb' , read_only= True ) 

st.set_page_config(layout= "wide" ) 

st.title( 'Super Bowl - History 1967 - 2020' )

with st.expander( 'Sobre os dados' ): 
    st.write( 'The Super Bowl is an annual American football game that determines the champion of the National Football League (NFL).' )

st.subheader( 'Filtros' ) 

col_a1, col_a2, col_a3 = st.columns( 3 ) 

with col_a1: 
    year_df = con.execute( """ 
        SELECT 
            SB
        FROM tbl_super_bowl
    """ ).df() 
    ano = st.selectbox( 'Ano' , year_df) 

with col_a2: 
    winner_df = con.execute( """ 
        SELECT 
            winner
        FROM tbl_super_bowl
        WHERE sb = ? 
    """, [ano]).df()
    vencedor = st.selectbox( 'Vencedor' , winner_df) 
    
with col_a3:
    loser_df = con.execute("""
        SELECT 
            loser 
        FROM tbl_super_bowl 
        WHERE sb = ? 
    """, [ano]).df()
    perdedor = st.selectbox( 'Perdedor' , loser_df)
    
st.subheader('Data preview')

col_b1, col_b2, col_b3 = st.columns( 3 ) 
    
with col_b1: 
    avg_winner = con.execute("""
        SELECT winner, count(*) as titulos FROM 'data/superbowl.csv' group by winner order by titulos desc
        """).df()
    st.write('Ganhadores: ', avg_winner)
    
with col_b2:
    top_winner = con.execute("""
        SELECT winner, count(*) as titulos FROM 'data/superbowl.csv' group by winner having count(*) > 3 order by titulos desc
        """).df()
    cols = st.columns([1, 1])
    
    fig = px.pie(top_winner, values='titulos', names='Winner',
                 title=f'maiores ganhadores',
                 height=300, width=200)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    st.plotly_chart(fig, use_container_width=True)
    
with col_b3: 
    avg_loser = con.execute("""
        SELECT loser, count(*) as derrotados FROM 'data/superbowl.csv' group by loser order by derrotados desc
        """).df()
    st.write('Perdedores: ', avg_loser)
    

