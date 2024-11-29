from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import Car
from django.db import connection
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from sklearn.linear_model import LinearRegression
import joblib  # Para carregar o modelo salvo
import matplotlib.pyplot as plt
import os
from django.conf import settings  # Para acessar BASE_DIR

plt.switch_backend('Agg')  # Usa um backend não interativo para salvar gráficos em memóriafrom django.shortcuts import render

def index(request):
    return render(request, 'car_analysis/index.html')  # Página inicial

def car_list(request):
    # Inicializa a consulta com todos os carros
    cars = Car.objects.all().order_by('prod_year')  # Ordenando por ano de produção

    # Lista de marcas distintas
    brands = Car.objects.values_list('manufacturer', flat=True).distinct()

    # Filtro por marca
    brand = request.GET.get('brand')
    if brand:
        cars = cars.filter(manufacturer__iexact=brand)

    # Filtro por preço (se fornecido)
    price = request.GET.get('price')
    if price:
        try:
            price = float(price)
            cars = cars.filter(price__lte=price)
        except ValueError:
            pass

    # Filtro por ano (se fornecido)
    year = request.GET.get('year')
    if year:
        try:
            year = int(year)
            cars = cars.filter(prod_year=year)
        except ValueError:
            pass

    # Filtro por modelo (se fornecido)
    model = request.GET.get('model')
    if model:
        cars = cars.filter(model__icontains=model)

    # Paginação
    paginator = Paginator(cars, 10)  # Mostra 10 itens por página
    page_number = request.GET.get('page')
    cars_page = paginator.get_page(page_number)

    # Passando os filtros para o template
    context = {
        'cars': cars_page,
        'brands': brands,
        'brand': brand,
        'price': price,
        'year': year,
        'model': model,
    }
    return render(request, 'car_analysis/car_list.html', context)



def car_price_dashboard(request):
    try:
        # Caminho do arquivo CSV
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(BASE_DIR, 'car_analysis', 'data', 'car_price_prediction.csv')

        # Verificar se o arquivo existe
        if not os.path.exists(data_path):
            raise FileNotFoundError("Arquivo de dados não encontrado.")

        # Carregar os dados
        df = pd.read_csv(data_path)

        # Verificar se as colunas necessárias estão presentes
        required_columns = ['Price', 'Fuel type', 'Mileage', 'Engine volume', 'Levy']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("As colunas esperadas não foram encontradas no arquivo CSV.")

        # Limpar e processar os dados
        df['Mileage'] = df['Mileage'].str.replace(r'\D', '', regex=True).astype(float)
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        df['Engine volume'] = pd.to_numeric(df['Engine volume'], errors='coerce')
        df['Levy'] = pd.to_numeric(df['Levy'], errors='coerce')

        # Remover dados inválidos (NaN)
        df = df.dropna(subset=['Price', 'Mileage', 'Engine volume', 'Levy'])
        df['Fuel type'] = df['Fuel type'].astype(str)

        # Gráfico 1: Distribuição de Preços por Tipo de Combustível
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.histplot(data=df, x='Price', hue='Fuel type', kde=True, palette='Set2', multiple='stack', ax=ax1)
        ax1.set_title('Distribuição de Preços por Tipo de Combustível', fontsize=16)
        ax1.set_xlabel('Preço', fontsize=12)
        ax1.set_ylabel('Frequência', fontsize=12)

        # Salvar o gráfico como base64
        buf1 = BytesIO()
        fig1.savefig(buf1, format='png')
        buf1.seek(0)
        img_data_1 = base64.b64encode(buf1.read()).decode('utf-8')
        buf1.close()
        plt.close(fig1)

        # Gráfico 2: Preço vs Quilometragem por Tipo de Combustível
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x='Mileage', y='Price', hue='Fuel type', palette='coolwarm', alpha=0.8, ax=ax2)
        sns.regplot(data=df, x='Mileage', y='Price', scatter=False, color='red', ci=None, label='Tendência', ax=ax2)
        ax2.set_title('Preço vs Quilometragem por Tipo de Combustível', fontsize=16)
        ax2.set_xlabel('Quilometragem', fontsize=12)
        ax2.set_ylabel('Preço', fontsize=12)
        ax2.legend(title='Tipo de Combustível')

        # Salvar o gráfico como base64
        buf2 = BytesIO()
        fig2.savefig(buf2, format='png')
        buf2.seek(0)
        img_data_2 = base64.b64encode(buf2.read()).decode('utf-8')
        buf2.close()
        plt.close(fig2)

        # Gráfico 3: Matriz de Correlação
        fig3, ax3 = plt.subplots(figsize=(8, 6))
        correlation_matrix = df[['Price', 'Mileage', 'Engine volume', 'Levy']].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax3)
        ax3.set_title('Matriz de Correlação', fontsize=16)

        # Salvar o gráfico como base64
        buf3 = BytesIO()
        fig3.savefig(buf3, format='png')
        buf3.seek(0)
        img_data_3 = base64.b64encode(buf3.read()).decode('utf-8')
        buf3.close()
        plt.close(fig3)

        # Renderizar a página com os gráficos
        return render(request, 'car_analysis/car_dashboard.html', {
            'img_data_1': img_data_1,
            'img_data_2': img_data_2,
            'img_data_3': img_data_3,
        })

    except FileNotFoundError as fnf_error:
        return render(request, 'car_analysis/car_dashboard.html', {'error': str(fnf_error)})
    except ValueError as val_error:
        return render(request, 'car_analysis/car_dashboard.html', {'error': f'Erro de validação: {str(val_error)}'})
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return render(request, 'car_analysis/car_dashboard.html', {'error': f'Erro inesperado: {str(e)}'})



def predict_car_price(request):
    if request.method == "GET":
        try:
            ano = int(request.GET.get('ano', 0))
            quilometragem = float(request.GET.get('quilometragem', 0.0))
            combustivel = request.GET.get('combustivel', '')

            if not combustivel:
                raise ValueError("O tipo de combustível é obrigatório.")

            input_data = pd.DataFrame([[ano, quilometragem, combustivel]], columns=['Prod. year', 'Mileage', 'Fuel type'])
            input_data = pd.get_dummies(input_data, drop_first=True)

            # Carregar o modelo treinado
            model_path = os.path.join(settings.BASE_DIR, 'car_analysis', 'models', 'car_price_model.pkl')
            model = joblib.load(model_path)

            model_columns = joblib.load(os.path.join(settings.BASE_DIR, 'car_analysis', 'models', 'model_columns.pkl'))
            input_data = input_data.reindex(columns=model_columns, fill_value=0)

            predicted_price = model.predict(input_data)[0]

            # Gráfico com a predição
            df = pd.read_csv(os.path.join(settings.BASE_DIR, 'car_analysis', 'data', 'car_price_prediction.csv'))

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(df['Mileage'], df['Price'], color='blue', label='Preços Reais')
            ax.scatter([quilometragem], [predicted_price], color='red', label='Predição', zorder=5)
            ax.set_title('Predição de Preço de Carros')
            ax.set_xlabel('Quilometragem')
            ax.set_ylabel('Preço')
            ax.legend()

            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()
            plt.close()

            context = {
                'predicted_price': round(predicted_price, 2),
                'image': img_str
            }
            return render(request, 'car_analysis/predict_price.html', context)

        except FileNotFoundError:
            return render(request, 'car_analysis/predict_price.html', {'error': 'Arquivo de dados ou modelo não encontrado.'})
        except ValueError as ve:
            return render(request, 'car_analysis/predict_price.html', {'error': f'Erro nos dados fornecidos: {str(ve)}'})
        except Exception as e:
            return render(request, 'car_analysis/predict_price.html', {'error': f'Erro inesperado: {str(e)}'})