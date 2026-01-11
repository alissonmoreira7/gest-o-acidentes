import streamlit as st
import plotly.express as px
import pandas as pd
from data.database import init_db, salvar_dados, excluir_registro, carregar_dados

st.set_page_config(page_title="+Segur - Gestão de Riscos", layout="wide")

init_db()

if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    vazio_esq, col_central, vazio_dir = st.columns([1, 1, 1])
    with col_central:
        st.write("\n" * 5)
        if not st.session_state.logado:
            with st.form('user_login'):
                st.title("+Segur Login")
                st.caption('AQUI A SEGURANÇA SE FAZ PRESENTE')
                st.divider()
                user = st.text_input('Usuário')
                senha = st.text_input('Senha', 
                                    type='password')
                login_btn = st.form_submit_button("Acessar Sistema",
                                                type="primary",
                                                use_container_width=True)

                if login_btn:
                    if user == "Analista TST" and senha == "12345":
                        st.session_state.logado = True
                        st.session_state.perfil = "Analista TST"
                        st.session_state.user = user
                        st.success("Acesso autorizado! Bem-vindo, Analista.")
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos.")
else:
    st.sidebar.title(f'Bem-vindo, {st.session_state.user}')
    st.sidebar.write(f"Perfil: **{st.session_state.perfil}**")
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    if st.session_state.perfil == "Analista TST":
        st.header('Registro de Inspeção de Campo')

        with st.form('form_incidente', clear_on_submit=True):
            col1, col2 = st.columns(2)
        
            data_evento = st.date_input("Data do Ocorrido")
            hora_evento = st.time_input("Hora do Ocorrido")

            setor = col1.selectbox("Setor da Obra", 
                                   ["Civil", "Elétrica", "Mecânica", "Administrativo", "Escavação"])
            
            gravidade = col2.select_slider("Gravidade do Risco", 
                                             options=[1, 2, 3],
                                             format_func=lambda x: "1 - Leve" if x == 1 else ("2 - Médio" if x == 2 else "3 - Grave"))
                         
            descricao = st.text_area("Descrição da Não Conformidade")
            if st.form_submit_button("Registrar Incidente"):
                salvar_dados(data_evento, hora_evento, setor, gravidade, st.session_state.user, descricao)
                st.success("Incidente registrado com sucesso no Banco de Dados!")

        st.divider()

        st.header("Dashboard de Inteligência Preventiva")
        df = carregar_dados()

        if not df.empty:
            criticos = df[df['gravidade'] >= 2].shape[0]
            total = df.shape[0]
            
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Total de Registros", total)
            kpi2.metric("Riscos Críticos", criticos, delta_color="inverse")
            kpi3.metric("Setor mais Crítico", df.groupby('setor')['gravidade'].mean().idxmax())

            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                fig_bar = px.bar(df, x='setor', y='gravidade', color='setor', title="Gravidade por Setor")
                st.plotly_chart(fig_bar, use_container_width=True)
                
            with col_chart2:
                fig_pie = px.pie(df, names='setor', title="Distribuição de Incidentes por Área")
                st.plotly_chart(fig_pie, use_container_width=True)

            st.subheader("Evolução dos Incidentes no Tempo")
            df_linha = df.groupby(df['data_evento'].dt.date).size().reset_index(name='Quantidade')
            fig_linha = px.line(
                df_linha, 
                x='data_evento', 
                y='Quantidade', 
                markers=True,
                title="Frequência Diária de Ocorrências"
            )
            fig_linha.update_layout(xaxis_title="Data", yaxis_title="Nº de Incidentes")
            st.plotly_chart(fig_linha, use_container_width=True)
            
            st.subheader("Histórico Completo de Incidentes")
            st.dataframe(df, use_container_width=True)

            st.divider()
        
        else:
            st.info("Aguardando registros para gerar estatísticas.")

        with st.expander("Excluir Registros"):
            lista_ids = df['id'].tolist()
            
            id_para_deletar = st.selectbox("Selecione o ID do registro que deseja remover:", lista_ids)
            
            if st.button("Confirmar Exclusão Permanente", type="secondary", use_container_width=True):
                excluir_registro(id_para_deletar)
                
                st.warning(f"Registro ID {id_para_deletar} foi excluído!")
                
                st.rerun()