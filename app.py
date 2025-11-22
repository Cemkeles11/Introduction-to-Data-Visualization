import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt


st.set_page_config(layout="wide", page_title="Küresel Hava Kirliliği Dashboard")

@st.cache_data
def load_data():
    """
    Veri setini 'global_air_pollution_data.csv' dosyasından yükler ve temizler.
    Sütun adlarını kodun beklediği formata dönüştürür.
    """
    try:
        df = pd.read_csv("global_air_pollution_data.csv")
    except FileNotFoundError:
        st.error(
            "HATA: 'global_air_pollution_data.csv' dosyası bulunamadı. "
            "Lütfen dosyanın 'app.py' ile aynı klasörde olduğundan emin olun."
        )
        return None
    
    column_mapping = {
        'country_name': 'Country',
        'city_name': 'City',
        'aqi_value': 'AQI Value',
        'aqi_category': 'AQI Category',
        'co_aqi_value': 'CO AQI Value',
        'ozone_aqi_value': 'Ozone AQI Value',
        'no2_aqi_value': 'NO2 AQI Value',
        'pm2_5_aqi_value': 'PM2.5 AQI Value',
        'pm10_aqi_value': 'PM10 AQI Value' 
    }
    
    df.rename(columns=column_mapping, inplace=True)
    
   
    df.columns = df.columns.str.strip()
    
   
    if 'AQI Category' in df.columns:
        df['AQI Category'] = df['AQI Category'].str.strip()
    else:
        st.error("Kritik Hata: Veri setinizde 'aqi_category' veya 'AQI Category' sütunu bulunamadı.")
        return None

    numeric_cols_desired = ['AQI Value', 'CO AQI Value', 'Ozone AQI Value', 'NO2 AQI Value', 'PM2.5 AQI Value', 'PM10 AQI Value']
    numeric_cols_available = [col for col in numeric_cols_desired if col in df.columns]
    
    for col in numeric_cols_available:
        df[col] = pd.to_numeric(df[col], errors='coerce') 
    
    
    df.dropna(inplace=True)

    return df

df = load_data()


if df is None:
    st.stop()

st.title("🌍 Küresel Hava Kirliliği ve Sağlık Etkileri Dashboard")
st.markdown("""
Bu dashboard, dünya genelindeki şehirlerin hava kalitesi endeks (AQI) değerlerini ve 
ana kirletici seviyelerini analiz etmek için oluşturulmuştur.
Veri Seti Kaynağı: [Kaggle - Global Air Pollution Data](https://www.kaggle.com/datasets/sazidthe1/global-air-pollution-data)
""")


st.sidebar.header("Filtreleme Seçenekleri")


countries = ["Tüm Ülkeler"] + sorted(df['Country'].unique())
selected_country = st.sidebar.selectbox("Ülke Seçin", countries)

if selected_country == "Tüm Ülkeler":
    df_filtered = df
else:
    df_filtered = df[df['Country'] == selected_country]


if selected_country == "Tüm Ülkeler":
    cities = sorted(df['City'].unique())
    selected_cities = st.sidebar.multiselect("Şehir(ler) Seçin (Karşılaştırma için)", 
                                             options=cities, 
                                             default=[],
                                             help="Tüm ülkeler seçiliyken bu filtre en iyi karşılaştırma grafikleri için çalışır.")
else:
    cities = sorted(df_filtered['City'].unique())
    selected_cities = st.sidebar.multiselect(f"{selected_country} İçin Şehir(ler) Seçin", 
                                             options=cities, 
                                             default=[])


pollutant_options = {
    'Genel AQI Değeri': 'AQI Value',
    'CO (Karbon Monoksit)': 'CO AQI Value',
    'Ozon (O3)': 'Ozone AQI Value',
    'Azot Dioksit (NO2)': 'NO2 AQI Value',
    'PM2.5 (Partikül Madde 2.5)': 'PM2.5 AQI Value',
    'PM10 (Partikül Madde 10)': 'PM10 AQI Value'
}

available_pollutant_options = {k: v for k, v in pollutant_options.items() if v in df.columns}


if not available_pollutant_options:
    st.error("Veri setinde gösterilecek kirletici sütunları bulunamadı. Lütfen veri setini kontrol edin.")
    selected_pollutant_col = None
    st.stop()
else:
    selected_pollutant_label = st.sidebar.radio(
        "Görselleştirilecek Ana Kirleticiyi Seçin",
        options=available_pollutant_options.keys(),
        index=0 
    )
    selected_pollutant_col = available_pollutant_options[selected_pollutant_label]




col1, col2 = st.columns((2, 1))

with col1:
 
    st.subheader(f"Dünya Geneli {selected_pollutant_label} Dağılım Haritası")
    
    if selected_pollutant_col:
        map_data = df.groupby('Country')[selected_pollutant_col].mean().reset_index()
        
        fig_map = px.choropleth(
            map_data,
            locations="Country",
            locationmode="country names",
            color=selected_pollutant_col,
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.YlOrRd,
            title=f"Ülke Bazlı Ortalama {selected_pollutant_label}",
            template="plotly_dark"
        )
        fig_map.update_layout(geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'))
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("Harita grafiği için kirletici seçeneği bulunmuyor.")

with col2:
 
    st.subheader("Genel AQI Kategori Dağılımı")
    
    pie_data = df_filtered['AQI Category'].value_counts().reset_index()
    pie_data.columns = ['AQI Category', 'Count']
    
    fig_pie = px.pie(
        pie_data,
        names='AQI Category',
        values='Count',
        title=f"AQI Kategorileri ({selected_country})",
        hole=0.3
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

col3, col4 = st.columns(2)

with col3:

    st.subheader(f"{selected_country}'daki En Kirli 10 Şehir ({selected_pollutant_label})")
    
    if selected_pollutant_col:
        top_10_cities = df_filtered.groupby('City')[selected_pollutant_col].mean().nlargest(10).reset_index()
        
        fig_bar = px.bar(
            top_10_cities,
            x='City',
            y=selected_pollutant_col,
            title="En Yüksek Değerler",
            color=selected_pollutant_col,
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Sütun grafiği için kirletici seçeneği bulunmuyor.")

    
    st.subheader("AQI Kategorilerine Göre Kirletici Dağılımı")
    
    if selected_pollutant_col:
        fig_box = px.box(
            df_filtered,
            x='AQI Category',
            y=selected_pollutant_col,
            color='AQI Category',
            title=f"{selected_pollutant_label} Dağılımı (Kategori Bazlı)",
            points="all"
        )
        st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.info("Kutu grafiği için kirletici seçeneği bulunmuyor.")
    

    st.subheader("Kirletici Parametreleri Arası Korelasyon")
    
    desired_corr_cols = ['AQI Value', 'CO AQI Value', 'Ozone AQI Value', 'NO2 AQI Value', 'PM2.5 AQI Value', 'PM10 AQI Value']
    corr_cols = [col for col in desired_corr_cols if col in df_filtered.columns]
    
    if len(corr_cols) > 1:
        corr_matrix = df_filtered[corr_cols].corr()
        fig_heatmap, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
        ax.set_title(f"Korelasyon Isı Haritası ({selected_country})")
        st.pyplot(fig_heatmap)
    else:
        st.warning(f"Korelasyon matrisi için yeterli veri sütunu bulunamadı ({selected_country}).")


with col4:

    st.subheader(f"{selected_country}'daki Şehirlerin Kirlilikteki Payı (Treemap)")
    
    if selected_pollutant_col:
        if selected_country == "Tüm Ülkeler":
            top_countries = df['Country'].value_counts().nlargest(20).index
            treemap_data = df[df['Country'].isin(top_countries)]
            path = ['Country', 'City']
            title_suffix = " (En Fazla Veriye Sahip 20 Ülke)"
        else:
            treemap_data = df_filtered
            path = ['City']
            title_suffix = f" ({selected_country})"

        fig_tree = px.treemap(
            treemap_data,
            path=[px.Constant(selected_country)] + path,
            values=selected_pollutant_col,
            color=selected_pollutant_col,
            color_continuous_scale='Reds',
            title=f"Şehir Bazlı {selected_pollutant_label} Yoğunluğu{title_suffix}"
        )
        fig_tree.update_layout(margin = dict(t=50, l=25, r=25, b=25))
        st.plotly_chart(fig_tree, use_container_width=True)
    else:
        st.info("Treemap grafiği için kirletici seçeneği bulunmuyor.")

        
   
    st.subheader(f"Genel AQI Değerlerinin Dağılımı (Histogram)")
    st.markdown("Bu grafik, seçilen filtredeki şehirlerin hangi AQI değeri aralıklarında yoğunlaştığını gösterir.")

    if 'AQI Value' in df_filtered.columns:
        chart_hist = alt.Chart(df_filtered).mark_bar().encode(
            x=alt.X('AQI Value:Q', bin=alt.Bin(maxbins=50), title='AQI Değeri'),
            y=alt.Y('count()', title='Gözlem Sayısı (Şehir)'),
            tooltip=[
                alt.Tooltip('AQI Value', bin=alt.Bin(maxbins=50), title='AQI Aralığı'),
                alt.Tooltip('count()', title='Bu Aralıktaki Şehir Sayısı')
            ]
        ).properties(
            title=f"AQI Değerlerinin Frekans Dağılımı ({selected_country})"
        ).interactive() #
        
        st.altair_chart(chart_hist, use_container_width=True)
    else:
        st.warning("Histogram grafiği için 'AQI Value' sütunu bulunamadı.")



st.divider()
st.subheader("Ülkeden Kategoriye Kirlilik Akışı (Genel Bakış)")
st.markdown("Bu grafik, veri setinde en çok gözleme sahip **10 ülkenin** kirlilik kategorilerine nasıl dağıldığını gösterir.")

top_countries = df['Country'].value_counts().nlargest(10).index
df_sankey_global = df[df['Country'].isin(top_countries)].copy() 


df_sankey_global['Country'] = df_sankey_global['Country'].replace(
    'United Kingdom of Great Britain and Northern Ireland', 'UK & N. Ireland'
)
df_sankey_global['Country'] = df_sankey_global['Country'].replace(
    'United States of America', 'USA'
)

sankey_data = df_sankey_global.groupby(['Country', 'AQI Category']).size().reset_index(name='Count')

if not sankey_data.empty:
 
    unique_countries = sankey_data['Country'].unique()
    unique_categories = sankey_data['AQI Category'].unique()
    all_nodes = list(unique_countries) + list(unique_categories)
    
   
    node_dict = {node: i for i, node in enumerate(all_nodes)}
    
    num_countries = len(unique_countries)
    num_categories = len(unique_categories)
    
    country_colors = px.colors.qualitative.Light24[:num_countries] 
    category_colors = px.colors.qualitative.Set2[:num_categories]
    
    node_colors = []
    for node in all_nodes:
        if node in unique_countries:
            idx = list(unique_countries).index(node)
            node_colors.append(country_colors[idx % len(country_colors)])
        else:
            idx = list(unique_categories).index(node)
            node_colors.append(category_colors[idx % len(category_colors)])
    
 
    source = sankey_data['Country'].map(node_dict).tolist()
    target = sankey_data['AQI Category'].map(node_dict).tolist()
    value = sankey_data['Count'].tolist()
    
  
    fig_sankey_global = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
            color=node_colors 
        ),
        link=dict(
            source=source, 
            target=target, 
            value=value,
            color= [node_colors[source_node] for source_node in source] 
        )
    )])
    
    fig_sankey_global.update_layout(
        title_text="En Çok Gözlem Yapılan 10 Ülkenin AQI Kategori Akışı", 
        font_size=12,  
        height=900,   
        margin=dict(l=10, r=10, t=50, b=10)
    )
    
    st.plotly_chart(fig_sankey_global, use_container_width=True)
else:
    st.warning("Global Sankey grafiği için veri bulunamadı.")



if selected_cities and len(selected_cities) > 1:
    
    st.header(f"Seçilen Şehirlerin Karşılaştırması ({', '.join(selected_cities)})")
    
    comparison_df = df[df['City'].isin(selected_cities)]
    
    
    comparison_cols_desired = ['CO AQI Value', 'Ozone AQI Value', 'NO2 AQI Value', 'PM2.5 AQI Value', 'PM10 AQI Value']
    comparison_cols_available = [col for col in comparison_cols_desired if col in comparison_df.columns]
    
    comparison_labels = {
        'CO AQI Value': 'CO',
        'Ozone AQI Value': 'Ozon',
        'NO2 AQI Value': 'NO2',
        'PM2.5 AQI Value': 'PM2.5',
        'PM10 AQI Value': 'PM10'
    }
    available_labels = {k: v for k, v in comparison_labels.items() if k in comparison_cols_available}

    col5, col6 = st.columns(2)

    with col5:
        
        st.subheader("Paralel Koordinatlar (Kirletici Karşılaştırması)")
        
        if len(comparison_cols_available) > 1:
            parallel_data = comparison_df.groupby('City')[comparison_cols_available].mean().reset_index()
            
   
            parallel_data['City_ID'] = parallel_data['City'].astype('category').cat.codes
            
            fig_parallel = px.parallel_coordinates(
                parallel_data,
                color='City_ID',
                dimensions=comparison_cols_available,
                labels=available_labels, 
                title="Şehirlerin Kirletici Profilleri (Ortalama Değerler)",
                color_continuous_scale=px.colors.sequential.Viridis
            )
            fig_parallel.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_parallel, use_container_width=True)
        else:
            st.warning("Paralel koordinat grafiği için yeterli kirletici verisi (CO, Ozon vb.) bulunamadı.")

    with col6:
        st.subheader("Gruplandırılmış Sütun Grafiği (Şehir Karşılaştırması)")

        if len(comparison_cols_available) > 1:
           
            radar_data = comparison_df.groupby('City')[comparison_cols_available].mean().reset_index()
            radar_data_long = pd.melt(radar_data, id_vars=['City'], 
                                      value_vars=comparison_cols_available, 
                                      var_name='Pollutant', value_name='Value')
            
           
            radar_data_long['Pollutant_Label'] = radar_data_long['Pollutant'].map(available_labels)
            radar_data_long['Pollutant_Label'] = radar_data_long['Pollutant_Label'].fillna(radar_data_long['Pollutant'])

            fig_grouped_bar = px.bar(
                radar_data_long,
                x="City",          
                y="Value",         
                color="Pollutant_Label", 
                barmode="group",    
                title="Şehirlerin Kirletici Profili (Sütun)",
                labels={"Pollutant_Label": "Kirletici Türü", "Value": "Ortalama Değer", "City": "Şehir"}
            )
          
            fig_grouped_bar.update_layout(legend_title_text='Kirletici')
            st.plotly_chart(fig_grouped_bar, use_container_width=True)
        else:
            st.warning("Karşılaştırma grafiği için yeterli kirletici verisi (CO, Ozon vb.) bulunamadı.")

elif selected_cities and len(selected_countries) == 1:
    st.info("Karşılaştırma grafikleri (Paralel Koordinatlar ve Radar) için lütfen en az 2 şehir seçin.")

else:
    st.info("Sol taraftaki 'Şehir(ler) Seçin' filtresini kullanarak 2 veya daha fazla şehri karşılaştırabilirsiniz.")



st.subheader("Ham Veri Seti (Filtrelenmiş)")
st.dataframe(df_filtered.head(100))