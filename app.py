import streamlit as st
import plotly.express as px
from estilizacao import estilizacao
from data.database import GestaoIncidentes, GestaoInspecoes

st.set_page_config(page_title="+Segur - Gestão de Riscos", layout="wide")

estilizacao()

incidente_class = GestaoIncidentes()
inspecao_class = GestaoInspecoes()

if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    _, col_central, _ = st.columns([1, 1, 1])
    with col_central:
        st.write("\n" * 5)
        with st.form('user_login'):
            st.title("+Segur Login")
            user = st.text_input('Usuário')
            senha = st.text_input('Senha', type='password')
            if st.form_submit_button("Acessar Sistema", type="primary", use_container_width=True):
                if user == "Analista TST" and senha == "12345":
                    st.session_state.logado = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")

else:
    st.sidebar.title(f"Olá, {st.session_state.user}")
    menu = st.sidebar.radio("Navegação", ["Incidentes", "Checklists"])
    
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    if menu == "Incidentes":
        st.header('Registro de Inspeção de Campo')

        with st.form('form_incidente', clear_on_submit=True):
            col1, col2 = st.columns(2)
            data_incidente = st.date_input("Data do Ocorrido")
            hora_incidente = st.time_input("Hora do Ocorrido")
            setor = col1.selectbox("Setor da Obra", ["Civil", "Elétrica", "Mecânica", "Administrativo", "Escavação"])
            gravidade = col2.select_slider("Gravidade", options=[1, 2, 3], 
                                           format_func=lambda x: "Leve" if x==1 else ("Médio" if x==2 else "Grave"))
            descricao = st.text_area("Descrição da Não Conformidade")

            if st.form_submit_button("Registrar Incidente"):
                if not descricao:
                    st.error("O campo descrição é obrigatório!")
                else:
                    incidente_class.salvar_incidente(data_incidente, hora_incidente, setor, gravidade, st.session_state.user, descricao)
                    st.success("Incidente registrado com sucesso!")
                    st.rerun()

        st.divider()
        st.header("Dashboard de Inteligência Preventiva")

        df = incidente_class.carregar_incidentes()

        if not df.empty:
            criticos = df[df['gravidade'] >= 2].shape[0]
            total = df.shape[0]
            
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Total de Registros", total)
            kpi2.metric("Riscos Críticos", criticos, delta_color="inverse")
            setor_mais_perigoso = df.groupby('setor')['gravidade'].sum().idxmax()
            valor_total_risco = df.groupby('setor')['gravidade'].sum().max()

            kpi3.metric(
                label="Setor mais Crítico", 
                value=setor_mais_perigoso, 
                delta=f"{valor_total_risco} pts acumulados",
                delta_color="inverse"
            )

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
                incidente_class.excluir_incidente(id_para_deletar)
                
                st.warning(f"Registro ID {id_para_deletar} foi excluído!")
                
                st.rerun()

    elif menu == "Checklists":
        st.header("Checklists de Equipamentos")
        
        equip = st.selectbox("Equipamento", ["Pá Carregadeira", "Empilhadeira"])
        
        with st.form("form_check"):
            res = st.radio("Resultado", ["Aprovado", "Interditado"])
            obs = st.text_area("Observações")
            if st.form_submit_button("Salvar Inspeção"):
                inspecao_class.salvar_checklist(equip, st.session_state.user, res, obs)
                st.success("Inspeção salva!")

        st.subheader("Histórico de Inspeções")
        st.dataframe(inspecao_class.carregar_inspecoes(), use_container_width=True) 