import streamlit             as st
import io

import numpy                 as np
import pandas                as pd
import matplotlib.pyplot     as plt
import seaborn               as sns

from gower                   import gower_matrix

from scipy.spatial.distance  import squareform
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import fcluster



@st.cache_data(show_spinner=False)
def calcularGowerMatrix(data_x, cat_features):
    return gower_matrix(data_x=data_x, cat_features=cat_features)


@st.cache_data(show_spinner=False)
# Definir a função para criar um dendrograma
def dn(color_threshold: float, num_groups: int, Z: list) -> None:
    """
    Cria e exibe um dendrograma.

    Parameters:
        color_threshold (float): Valor de threshold de cor para a coloração do dendrograma.
        num_groups (int): Número de grupos para o título do dendrograma.
        Z (list): Matriz de ligação Z.

    Returns:
        None
    """
    plt.figure(figsize=(24, 6))
    plt.ylabel(ylabel='Distância')
    
    # Adicionar o número de grupos como título
    plt.title(f'Dendrograma Hierárquico - {num_groups} Grupos')

    # Criar o dendrograma com base na matriz de ligação Z
    dn = dendrogram(Z=Z, 
                    p=6, 
                    truncate_mode='level', 
                    color_threshold=color_threshold, 
                    show_leaf_counts=True, 
                    leaf_font_size=8, 
                    leaf_rotation=45, 
                    show_contracted=True)
    plt.yticks(np.linspace(0, .6, num=31))
    plt.xticks([])

    # Exibir o dendrograma criado
    st.pyplot(plt)

    # Imprimir o número de elementos em cada parte do dendrograma
    for i in dn.keys():
        st.text(f'dendrogram.{i}: {len(dn[i])}')


# Função principal da aplicação
def main():
    # Configuração inicial da página da aplicação
    st.set_page_config(
        page_title="EBAC X SEMANTIX",
        page_icon='https://raw.githubusercontent.com/raafarosa/Ebac_Data_Scientist_General/main/utilities/regular_ebac-logo.ico', 
        layout="wide",
        initial_sidebar_state="expanded",
    )


    st.sidebar.markdown('''
                        # **Profissão: Cientista de Dados**
                        ### **Brazilian Amazon Rainforest Degradation 1999-2019**

                        **Por:** [Rafael Rosa](https://www.linkedin.com/in/rafael-rosa-alves/)<br>
                        
                        ---
                        ''', unsafe_allow_html=True)
    

    with st.sidebar.expander(label="Bibliotecas/Pacotes", expanded=False):
        st.code('''
                import streamlit             as st
                import io

                import numpy                 as np
                import pandas                as pd
                import matplotlib.pyplot     as plt
                import seaborn               as sns

                from gower                   import gower_matrix

                from scipy.spatial.distance  import squareform
                from scipy.cluster.hierarchy import linkage
                from scipy.cluster.hierarchy import dendrogram
                from scipy.cluster.hierarchy import fcluster
                ''', language='python')

        

    st.markdown('''
                <div style="text-align:center">
                    <img src="https://raw.githubusercontent.com/raafarosa/Ebac-Semantix/main/utilities/Logos_colab.jpg" alt="ebac_logo-data_science" width="100%">
                </div>

                ---

                <!-- # **Profissão: Cientista de Dados** -->
                ### **Brazilian Amazon Rainforest Degradation 1999-2019**

                **Por:** [Rafael Rosa](https://www.linkedin.com/in/rafael-rosa-alves/)<br>

                ---
                ''', unsafe_allow_html=True)


    st.markdown('''
                <a name="intro"></a> 

                # Agrupamento hierárquico

                Neste projeto foi utilizada a base Brazilian Amazon Rainforest Degradation 1999-2019. Antes das análises, vamos a um contexto rápido sobre o assunto!

                A Floresta Amazônica é uma floresta tropical úmida de folhas largas no bioma Amazônia que cobre territórios pertencentes a nove nações. A maior parte da floresta está contida dentro do Brasil, com 60% da floresta tropical, seguido pelo Peru com 13%, Colômbia com 10%, e com quantidades menores na Venezuela, Equador, Bolívia, Guiana, Suriname e Guiana Francesa.

                A região fornece benefícios importantes para comunidades que vivem perto e longe. Quase 500 comunidades indígenas chamam a Floresta Amazônica de lar. É um ecossistema altamente biodiverso, lar de inúmeras espécies de plantas e animais. A floresta tropical pode criar seu próprio clima e influenciar os climas ao redor do mundo. Infelizmente, o ecossistema frágil enfrenta a constante ameaça de desmatamento e incêndios (por causas naturais ou antropogênicas).

                O desmatamento ocorre por muitas razões, como agricultura ilegal, desastres naturais, urbanização e mineração. Existem várias maneiras de remover florestas - queimar e cortar árvores são dois métodos. Embora o desmatamento esteja ocorrendo em todo o mundo hoje, é um problema especialmente crítico nas florestas tropicais da Amazônia, como a única grande floresta ainda de pé no mundo. Lá, as espécies de plantas e animais que abrigam têm desaparecido em uma taxa alarmante.

                ''', unsafe_allow_html=True)


    st.markdown(''' 
                ## Visualização dos Dados
                <a name="visualizacao"></a> 
                ''', unsafe_allow_html=True)
    

    st.markdown(''' 
                ### Carregar e ler dados de arquivo .csv
                <a name="read_csv"></a> 
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Leitura do arquivo CSV e armazenar os dados em um DataFrame chamado df
        df = pd.read_csv('https://raw.githubusercontent.com/raafarosa/Ebac-Semantix/main/Data/inpe_brazilian_amazon_fires_1999_2019.csv')

        # Exibir o DataFrame df, mostrando os dados carregados do arquivo CSV
        st.dataframe(df)


    st.markdown(''' 
                ### Visualização da contagem de valores na coluna 'year'
                <a name="value_counts"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Exibir a contagem de valores na coluna 'year'
        st.text(df.year.value_counts())


    st.markdown(''' 
                ### Representação gráfica da contagem de 'year' 
                <a name="countplot"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Criar um gráfico de contagem (count plot) para a coluna 'year' usando seaborn
        sns.countplot(x='year', data=df)

        # Exibir o gráfico
        st.pyplot(plt)


    st.markdown(''' 
                ## Análise Descritiva
                <a name="descritiva"></a>
                ''', unsafe_allow_html=True)
    

    st.markdown(''' 
                ### Informações sobre a estrutura do DataFrame
                <a name="info"></a>
                ''', unsafe_allow_html=True)
    # Imprimir informações sobre a estrutura do DataFrame
    st.info(f''' 
            Quantidade de linhas: {df.shape[0]}

            Quantidade de colunas: {df.shape[1]}

            Quantidade de valores missing: {df.isna().sum().sum()} 
            ''')
    with st.echo():
        ""
        # Exibir informações detalhadas sobre o DataFrame, incluindo os tipos de dados de cada coluna e a contagem de valores não nulos
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())


    st.markdown(''' 
                ### Resumo estatístico para variáveis numéricas
                <a name="describe"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Exibir estatísticas descritivas para colunas numéricas do DataFrame
        st.dataframe(df.describe())


    st.markdown(''' 
                ### Representação gráfica da correlação entre variáveis
                <a name="corr"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Criar um mapa de calor (heatmap) para visualizar a correlação entre as colunas do DataFrame
        sns.heatmap(df.corr(numeric_only=True), cmap='viridis')

        # Exibir o mapa de calor
        st.pyplot(plt)


    st.markdown('''
                ## Feature Selection
                <a name="feature_selection"></a>
                ''', unsafe_allow_html=True)
    

    st.markdown(''' 
                ### Dados que descrevem quantitativos para o desmatamento.
                <a name="session_navigation_pattern"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Lista de variáveis que descrevem o padrão de navegação na sessão
        session_navigation_pattern = ['year', 
                                      'month', 
                                      'state', 
                                      'latitude', 
                                      'longitude', 
                                      'firespots', ]

        # Obter os tipos de dados das variáveis relacionadas ao padrão de navegação na sessão, criar um DataFrame e renomear as colunas
        st.dataframe(df[session_navigation_pattern].dtypes.reset_index().rename(columns={'index': 'Variável (session_navigation_pattern)', 
                                                                                         0: 'Tipo'}), hide_index=True)

    st.markdown(''' 
                ### Seleção e análise das variáveis que indicam a característica da data
                <a name="temporal_indicators"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Lista de variáveis que indicam a característica da data
        temporal_indicators = ['month', 'state', 'firespots']

        # Obter os tipos de dados das variáveis relacionadas à característica da data, criar um DataFrame e renomear as colunas
        st.dataframe(df[temporal_indicators].dtypes.reset_index().rename(columns={'index': 'Variável (temporal_indicators)', 
                                                                                  0: 'Tipo'}), hide_index=True)


    st.markdown(''' 
                ### Seleção das variáveis numéricas e categóricas
                <a name="cat_selection"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Lista de variáveis numéricas
        numerical = ['year', 'month', 'state']

        # Selecionar as variáveis relacionadas ao padrão de navegação e à característica da data
        df_ = df[session_navigation_pattern + temporal_indicators]

        # Selecionar as variáveis categóricas removendo as variáveis numéricas
        df_cat = df_.drop(columns=numerical)


    st.markdown(''' 
                ### Variáveis categóricas e seus valores únicos
                <a name="unique"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Imprimir os valores únicos para cada variável categórica
        [f'{cat}: {df[cat].unique()}' for cat in df_cat]


    st.markdown(''' 
                ### Processamento de Variáveis Dummy: Identificação categórica e análise dos tipos de dados
                <a name="dummy"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Criar variáveis dummy para as variáveis relacionadas ao padrão de navegação e à característica da data
        df_dummies = pd.get_dummies(data=df_, drop_first=False)

        # Obter as colunas que representam as variáveis categóricas
        categorical_features = df_dummies.select_dtypes(include='object').columns.tolist()

        # Criar uma lista de valores booleanos indicando se cada coluna é categórica
        cat_features = [True if column in categorical_features else False for column in df_dummies]

        # Obter os tipos de dados das variáveis dummy, criar um DataFrame e adicionar uma coluna indicando se a variável é categórica
        st.dataframe(df_dummies.dtypes.reset_index().rename(columns={'index': 'Variável', 
                                                                     0: 'Tipo'
                                                                     }).assign(Categorical=cat_features), hide_index=True)


    st.markdown(''' 
                ## Agrupamentos Hierárquicos com 3 e 4 grupos 
                <a name="agrupamento"></a>
                ''', unsafe_allow_html=True)


    st.markdown(''' 
                ### Cálculo da Matriz de Distância Gower
                <a name="gower"></a>
                ''', unsafe_allow_html=True)
    with st.spinner(text='Calculando matriz de distância Gower... (Tempo previsto: 4 minutos)'):
        with st.echo():
            ""
            # Calcular a matriz de distância Gower
            dist_gower = calcularGowerMatrix(data_x=df_dummies, cat_features=cat_features)
    st.success('Matriz de distância Gower calculada!')
    with st.echo():
        ""
        # Criar um DataFrame com a matriz de distância Gower
        st.dataframe(pd.DataFrame(dist_gower).head())


    st.markdown(''' 
                ### Cálculo da matriz de ligação a partir da vetorização da distância Gower
                <a name="linkage"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Converter a matriz de distância Gower em um vetor
        gdv = squareform(X=dist_gower, force='tovector')

        # Calcular a matriz de ligação usando o método 'complete'
        Z = linkage(y=gdv, method='complete')

        # Criar um DataFrame com a matriz de ligação
        st.dataframe(pd.DataFrame(data=Z, columns=['id1', 'id2', 'dist', 'n']), hide_index=True)


    st.markdown(''' 
                ### Visualização dos agrupamentos: Dendrogramas para diferentes números de grupos
                <a name="dendrogram"></a>
                ''', unsafe_allow_html=True)
    # Para cada quantidade desejada de grupos e valor de threshold de cor, criar e exibir o dendrograma com título
    for qtd, color_threshold in [(3, .53), (4, .5)]:
        st.info(f'\n{qtd} grupos:')
        # Exibir os dendrogramas criados
        dn(color_threshold=color_threshold, num_groups=qtd, Z=Z)


    st.markdown('''
                ## Construção, Avaliação e Análise dos Grupos
                <a name="grupos"></a>
                ''', unsafe_allow_html=True)
    

    st.markdown(''' 
                ### Agrupamento e atualização do dataFrame com resultados para 3 grupos
                <a name="grupo_3"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Adicionar uma coluna 'grupo_3' ao DataFrame com base no agrupamento hierárquico
        df['grupo_3'] = fcluster(Z=Z, t=3, criterion='maxclust')

        # Criar um DataFrame contendo a contagem de elementos em cada grupo
        st.dataframe(pd.DataFrame({'Grupo': df.grupo_3.value_counts().index, 
                                   'Quantidade': df.grupo_3.value_counts().values
                                   }).set_index('Grupo').style.format({'Quantidade': lambda x : '{:d}'.format(x)}))


    st.markdown(''' 
                ### Tabela cruzada percentual com renomeação dos 3 grupos
                <a name="crosstab3rename"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Criar e exibir uma tabela cruzada normalizada por linha para as variáveis 'year' e 'grupo_3', com renomeação dos grupos
        st.table(pd.crosstab(index=df.year, 
                             columns=df.grupo_3, 
                             normalize='index'
                             ).applymap(lambda x: f'{x*100:.2f} %').rename(columns={1: '1 (Returning_Visitor)', 
                                                                                    2: '2 (New_Visitor)', 
                                                                                    3: '3 (Other)'}))


    st.markdown(''' 
                ### Agrupamento e atualização do dataFrame com resultados para 4 grupos
                <a name="grupo_4"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Adicionar uma coluna 'grupo_4' ao DataFrame com base no agrupamento hierárquico
        df['grupo_4'] = fcluster(Z=Z, t=4, criterion='maxclust')

        # Criar um DataFrame contendo a contagem de elementos em cada grupo
        st.dataframe(pd.DataFrame({'Grupo': df.grupo_4.value_counts().index, 
                                   'Quantidade': df.grupo_4.value_counts().values
                                   }).set_index('Grupo').sort_index().style.format({'Quantidade': lambda x : '{:d}'.format(x)}))


    st.markdown(''' 
                <br>

                ### Pair Plot final
                <a name="pairplot"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Criar um pair plot para visualizar as relações entre as variáveis "year","month","state","latitude","longitude","firespots", colorindo pelo valor da variável 'year'
        sns.pairplot(data=df[['year', 'month', 'state', 'latitude', 'longitude', 'firespots']], 
                     hue='year')

        # Exibir o pair plot
        st.pyplot(plt)


    st.markdown('''
                ## Conclusão

                O destamamento da Amazônia é uma preocupação global urgente, impulsionada pela expansão da agricultura, mineração e infraestrutura. Isso resulta na perda de habitat, ameaça à biodiversidade e contribui significativamente para as mudanças climáticas. Combater o desmatamento ilegal, promover práticas sustentáveis e fortalecer a aplicação da lei são essenciais para proteger esse ecossistema vital e garantir um futuro sustentável.
                
                ---
                <a name="final"></a>
                ''', unsafe_allow_html=True)


if __name__ == '__main__':
    main()