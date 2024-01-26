# Importando Bibliotecas
import pandas as pd
import plotly.express as px
import streamlit as st

# Lendo Arquivos
df_hapvida = pd.read_csv('RECLAMEAQUI_HAPVIDA.csv')
df_nagem = pd.read_csv('RECLAMEAQUI_NAGEM.csv')
df_ibyte = pd.read_csv('RECLAMEAQUI_IBYTE.csv')


# In[300]:


# Display Hapvida
display(df_hapvida)


# In[301]:


# Display Nagem
display(df_nagem)


# In[302]:


# Display Ibyte
display(df_ibyte)


# In[303]:


# Verificando Info Hapvida
df_hapvida.info()


# In[304]:


# Verificando Info Nagem
df_nagem.info()


# In[305]:


# Verificando Info Ibyte
df_ibyte.info()


# In[306]:


# Criando Coluna Empresa em cada Dataset
df_hapvida['Empresa'] = 'Hapvida'
df_nagem['Empresa'] = 'Nagem'
df_ibyte['Empresa'] = 'Ibyte'

# Unificando Datasets
df = pd.concat([df_hapvida,df_nagem,df_ibyte])
display(df)


# ### Série Temporal

# In[307]:


# Convertendo Para Datetime Coluna Tempo
df['TEMPO'] = pd.to_datetime(df['TEMPO'])


# In[308]:


# Groupby DataFrame
freq_df = df.groupby('ANO').size().reset_index(name='Frequência')

# Create a line chart with Plotly
fig = go.Figure(data=go.Scatter(x=freq_df['ANO'], y=freq_df['Frequência'], line=dict(color='green')))


# Adding labels and title
fig.update_layout(
    xaxis_title='Ano',
    yaxis_title='Frequência',
    title='Frequência x Ano'
)

# Display the plot
fig.show()


# In[309]:


# Groupby DataFrame
freq_df = df.groupby('MES').size().reset_index(name='Frequência')

# Create a line chart with Plotly
fig = go.Figure(data=go.Scatter(x=freq_df['MES'], y=freq_df['Frequência'], line=dict(color='green')))

# Adding labels and title
fig.update_layout(
    xaxis_title='Mês',
    yaxis_title='Frequência',
    title='Frequência x Mês'
)

# Display the plot
fig.show()


# In[310]:


# Groupby DataFrame
freq_df = df.groupby('DIA').size().reset_index(name='Frequência')

# Create a line chart with Plotly
fig = go.Figure(data=go.Scatter(x=freq_df['DIA'], y=freq_df['Frequência'], line=dict(color='green')))

# Adding labels and title
fig.update_layout(
    xaxis_title='Dia',
    yaxis_title='Frequência',
    title='Frequência x Dia'
)

# Display the plot
fig.show()


# ### Reclamações Por Estado

# In[311]:


# Função Estado
def state(x):
    split = x.split('-')
    if 'naoconsta' in x:
        return 'Não Informado'
    if ('JUAZEIRO DO NORTE' in x) and ('C' in x):
        return 'CE'
    if ('IPOJUCA' in x) and (' P' in x):
        return 'PE'
    if split[-1].strip() == '':
        return 'Não Informado'
    else:
        return split[-1].strip()
df['Estado'] = df['LOCAL'].apply(state)
display(df)


# In[312]:


import plotly.graph_objects as go

# Groupby DataFrame
freq_df = df.groupby('Estado').size().reset_index(name='Reclamações')
freq_df = freq_df.sort_values(by='Reclamações', ascending=True)

# Create bar chart
fig = go.Figure(data=[go.Bar(x=freq_df['Reclamações'], y=freq_df['Estado'],orientation='h', marker=dict(color='red'))])

# Update layout (optional)
fig.update_layout(title='Qtd Reclamações x Estado', xaxis_title='Estado', yaxis_title='Qtd Reclamações')

# Show the chart
fig.show()


# ### Reclamações Por Status

# In[313]:


import plotly.graph_objects as go

# Groupby DataFrame
freq_df = df.groupby('STATUS').size().reset_index(name='Reclamações')
freq_df = freq_df.sort_values(by='Reclamações', ascending=False)

# Create bar chart
fig = go.Figure(data=[go.Bar(x=freq_df['STATUS'], y=freq_df['Reclamações'], marker=dict(color='blue'))])

# Update layout (optional)
fig.update_layout(title='Qtd Reclamações x Status', xaxis_title='Status', yaxis_title='Qtd Reclamações')

# Show the chart
fig.show()


# ### Tamanho do Texto

# In[314]:


# Criando Coluna Tamanho Texto
df['Tamanho Texto Desc'] = df['DESCRICAO'].apply(lambda x: len(x.strip()))


# In[315]:


import plotly.graph_objects as go

# Create histogram
fig = go.Figure(data=[go.Histogram(x=df['Tamanho Texto Desc'], marker=dict(color='orange'))])

# Update layout (optional)
fig.update_layout(title='Histograma Tamanho Texto', xaxis_title='Tamanho Texto', yaxis_title='Frequência')

# Show the chart
fig.show()


# ### Streamlit

# In[316]:


# streamlit run appstreamlitguilhermeterceiro.py
st.title('Reclame Aqui')


st.write('Informação Geral')
col1, col2, col3, col4= st.columns(4)
col1.metric(label="Número de colunas", value=len(df.columns))
col2.metric(label="Número de linhas", value=len(df))
col3.metric(label="Descrição mínima", value=df['Tamanho Texto Desc'].min())
col4.metric(label="Descrição máxima", value=df['Tamanho Texto Desc'].max())

col1, col2= st.columns(2)
col1.metric(label="Primeira data", value=df['TEMPO'].min().strftime("%Y-%m-%d"))
col2.metric(label="Última data", value=df['TEMPO'].max().strftime("%Y-%m-%d"))

with st.sidebar:
        st.title('Filtros')

        seletor_empresa=st.selectbox('Selecione a empresa', 
                                     list(df['Empresa'].unique()), 
                                     index=None, 
                                     placeholder='Selecione a empresa',
                                     label_visibility='collapsed')
        
        seletor_estado=st.selectbox('Selecione o estado',
                                    list(df['Estado'].unique()), 
                                    index=None, 
                                    placeholder='Selecione o estado',
                                    label_visibility='collapsed')
        
        seletor_status=st.selectbox('Selecione a status',
                                    list(df['STATUS'].unique()), 
                                    index=None, 
                                    placeholder='Selecione a status',
                                    label_visibility='collapsed')
        
        start_desc, end_desc = st.select_slider(
            'Selecione o intervalo do tamanho do texto da coluna Descrição',
            options=list(range(df['Tamanho Texto Desc'].min(),df['Tamanho Texto Desc'].max()+1,1)),
            value=(df['Tamanho Texto Desc'].min(), df['Tamanho Texto Desc'].max()))

        st.write('Selecione o período de análise')
        #col1, col2= st.columns(2)
        ini=st.date_input("Data inicial", value=df['TEMPO'].min())
        fim=st.date_input("Data final", value=df['TEMPO'].max())

        options = st.multiselect(
            'Selecione as colunas',
            list(df.columns),
            list(df.columns))




#### Após os Filtros

if seletor_empresa!=None:
    df = df[df['Empresa'] == seletor_empresa] 
if seletor_estado!=None:
    df = df[df['Estado'] == seletor_estado]
if seletor_status!=None:
    df = df[df['STATUS'] == seletor_status]
df = df[(df['Tamanho Texto Desc']>=start_desc) & (df['Tamanho Texto Desc']<=end_desc)]
df = df[(df['TEMPO']>=(pd.to_datetime(ini))) & (df['TEMPO']<=(pd.to_datetime(fim)))]

# Verificação se existe dado selecionado 
if len(df) == 0:
    st.write('Nenhum dado para visualizar.')
else:
    
    ### Criar DataFrame
    df_time = pd.pivot_table(df,values='ID',index='TEMPO',columns='Empresa',aggfunc=pd.Series.nunique)
    df_time = df_time.reset_index()

    #### Frequência de reclamações por estado.
    # Criar coluna com UF
    estado_lista=[]
    for i in range(len(df)):
        estado_lista.append(df['LOCAL'].iloc[i][-2:])
    df['ESTADO']=estado_lista

    # Criar DataFrame
    df_estado = pd.pivot_table(df,values='ID',index='Estado',columns='Empresa',aggfunc=pd.Series.nunique,fill_value=0)
    df_estado = df_estado.reset_index()
    df_estado = df_estado[~(df_estado['Estado']==' C')]
    df_estado = df_estado[~(df_estado['Estado']==' P')]
    df_estado = df_estado[~(df_estado['Estado']=='--')]
    df_estado = df_estado[~(df_estado['Estado']=='ta')]

    if seletor_empresa!=None:
        df_estado.sort_values(by=seletor_empresa, ascending=False, inplace = True)
    else:
        for i in list(df['Empresa'].unique()):
            df_estado['Total'] = df_estado[i]
        df_estado.sort_values(by='Total', ascending=False, inplace = True)

    #### Frequência de cada tipo de STATUS
    df_status = df.STATUS.value_counts()
    df_status.sort_values(ascending=False, inplace = True)

    ## Distribuição do tamanho do texto (coluna DESCRIÇÃO)
    df['Tamanho Texto Desc'] = [len(i) for i in df['DESCRICAO']]

    st.markdown('---')
    st.write('Dados após aplicação dos filtros')
    st.dataframe(df[options][(df['TEMPO'] >= pd.to_datetime(ini)) & (df['TEMPO'] <= pd.to_datetime(fim))],
                column_config={"ANO":st.column_config.NumberColumn(format='%f'),
                                "ID":st.column_config.NumberColumn(format='%f'),
                                "":st.column_config.NumberColumn(format='%f'),},
                                hide_index=True)

    st.markdown('---')
    if seletor_empresa!=None:
        fig1=px.line(df_time,x='TEMPO',y=seletor_empresa,title='Série temporal do número de reclamações',
                labels={'TEMPO':'Data','value':'Reclamações'})
    else:
        fig1=px.line(df_time,x='TEMPO',y=list(df['Empresa'].unique()),title='Série temporal do número de reclamações',
                labels={'TEMPO':'Data','value':'Reclamações'})
    st.plotly_chart(fig1)

    st.markdown('---')
    st.write('Frequência de reclamações por Estado')
    col1, col2= st.columns(2,gap="small")
    col1.dataframe(df_estado,hide_index=True)
    #             column_config={"Hap":st.column_config.NumberColumn(format='%f'),
    #                            "ID":st.column_config.NumberColumn(format='%f'),
    #                            "CONT_DESC":st.column_config.NumberColumn(format='%f'),})

    if seletor_empresa!=None:
        fig2=px.bar(df_estado.sort_values(by=seletor_empresa, ascending=True),
                y='ESTADO',x=seletor_empresa,labels={'ESTADO':'Estado',seletor_empresa:'Frequência'})
    else:
        fig2=px.bar(df_estado.sort_values(by='Total', ascending=True),
                y='Estado',x='Total',labels={'ESTADO':'Estado','Total':'Frequência Total'})
    col2.plotly_chart(fig2,use_container_width=True)

    st.markdown('---')

    st.write('Frequência de reclamações por Status')
    col1, col2 = st.columns([0.3, 0.7],gap="small")
    col1.dataframe(df_status)
    fig3=px.bar(df_status,x=df_status.index,y=df_status.values,labels={'index':'Status','y':'Frequência'})
    col2.plotly_chart(fig3,use_container_width=True)

    st.markdown('---')
    st.write('Distribuição do tamanho do texto da coluna Descrição')
    fig4=px.histogram(df,x=['Tamanho Texto Desc'],labels={'value':'Tamanho da descrição'})
    fig4.update_layout(yaxis_title='Frequência',showlegend=False)
    st.plotly_chart(fig4)

col1, col2= st.columns([0.7, 0.3])

col2.write('by Felipe Gomes')

