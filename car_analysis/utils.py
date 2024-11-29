import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

def save_chart_as_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return img_data

def create_price_distribution_chart(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=df, x='Price', hue='Fuel type', kde=True, palette='Set2', multiple='stack', ax=ax)
    ax.set_title('Distribuição de Preços por Tipo de Combustível')
    ax.set_xlabel('Preço')
    ax.set_ylabel('Frequência')
    return save_chart_as_base64(fig)

def create_correlation_chart(df):
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = df.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    ax.set_title('Mapa de Correlação entre Variáveis')
    return save_chart_as_base64(fig)

def create_boxplot_chart(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='Fuel type', y='Price', palette='Set3', ax=ax)
    ax.set_title('Distribuição de Preços por Tipo de Combustível')
    ax.set_xlabel('Tipo de Combustível')
    ax.set_ylabel('Preço')
    return save_chart_as_base64(fig)
