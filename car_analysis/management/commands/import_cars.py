import csv
from django.core.management.base import BaseCommand
from car_analysis.models import Car  # Substitua 'car_analysis' pelo nome correto do seu app

class Command(BaseCommand):
    help = "Importa dados do arquivo CSV para o modelo Car"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Caminho para o arquivo CSV")

    def parse_year(self, year_value):
        """Função para tratar o valor do ano de produção"""
        try:
            # Se o valor do ano contiver algo como '04-May', tentamos extrair o ano
            if '-' in year_value:
                return int(year_value.split('-')[1])  # Extrai o ano após o "-"
            # Caso contrário, tentamos converter diretamente para um número
            return int(year_value)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Erro ao processar o ano de produção '{year_value}': {e}"))
            return None

    def sanitize_doors(self, doors_value):
        """Função para tratar valores inconsistentes no campo 'Doors'"""
        try:
            # Tenta converter para inteiro diretamente
            return int(doors_value)
        except ValueError:
            # Trata valores como '04-May' ou outros formatos inconsistentes
            if doors_value == '04-May':
                return 4  # Substitui por 4 como exemplo
            self.stderr.write(self.style.WARNING(f"Valor inválido no campo 'Doors': {doors_value}. Substituindo por None."))
            return None

    def handle(self, *args, **options):
        file_path = options['file_path']
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                cars = []
                for row in reader:
                    try:
                        # Tratamento de dados para adaptar ao modelo
                        car = Car(
                            id=row['ID'],
                            price=int(row['Price']) if row['Price'].isdigit() else None,
                            levy=row['Levy'] if row['Levy'] != '-' else None,
                            manufacturer=row['Manufacturer'],
                            model=row['Model'],
                            prod_year=self.parse_year(row['Prod. year']),
                            category=row['Category'],
                            leather_interior=(row['Leather interior'] == 'Yes'),
                            fuel_type=row['Fuel type'],
                            engine_volume=float(row['Engine volume'].split()[0]) if row['Engine volume'] else None,
                            mileage=int(row['Mileage'].split()[0]) if row['Mileage'] else None,
                            cylinders=float(row['Cylinders']) if row['Cylinders'] else None,
                            gear_box_type=row['Gear box type'],
                            drive_wheels=row['Drive wheels'],
                            doors=self.sanitize_doors(row['Doors']),
                            wheel=row['Wheel'],
                            color=row['Color'],
                            airbags=int(row['Airbags']) if row['Airbags'].isdigit() else None,
                        )
                        cars.append(car)
                    except Exception as row_error:
                        self.stderr.write(self.style.ERROR(f"Erro ao processar a linha: {row}: {row_error}"))

                # Salva os objetos em batch
                if cars:
                    Car.objects.bulk_create(cars, ignore_conflicts=True)
                    self.stdout.write(self.style.SUCCESS(f"Importação concluída com sucesso! {len(cars)} registros adicionados."))
                else:
                    self.stderr.write(self.style.ERROR("Nenhum registro foi importado. Verifique os erros nas linhas."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Erro ao importar os dados: {e}"))
