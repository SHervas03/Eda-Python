import pandas as pd
import os

def reading_and_unifying_files(years):
    df = []
    columns = None
    for year in years:
        dataset = pd.read_excel(f"./Data/{year}_Accidentalidad.xlsx")
        if columns is None:
            columns = set(dataset.columns)
        else:
            if set(dataset.columns) != columns:
                print(f"Columns for year {year} do not match")
                continue
        df.append(dataset)

    if df:
        df = pd.concat(df, ignore_index=True)
        print("Files successfully unified")
        return df
    else:
        print("The files could not be merged.")
        return None

def renaming_values(df):
    df['tipo_vehiculo'] = df['tipo_vehiculo'].replace({
        'Turismo':'Car',
        'Ciclomotor': 'Car',
        'Todo terreno': 'Car',
        'Cuadriciclo no ligero': 'Car',
        'Cuadriciclo ligero': 'Car',
        'Ciclomotor de tres ruedas': 'Car',
        'Motocicleta > 125cc': 'Motorcicle',
        'Motocicleta hasta 125cc': 'Motorcicle',
        'Moto de tres ruedas > 125cc': 'Motorcicle',
        'Moto de tres ruedas hasta 125cc': 'Motorcicle',
        'Ciclomotor de dos ruedas L1e-B': 'Motorcicle',
        'Furgoneta': 'Van',
        'Caravana': 'Van',
        'Autocaravana': 'Van',
        'Bicicleta': 'Bicicle',
        'Bicicleta EPAC (pedaleo asistido)': 'Bicicle',
        'Ciclo de motor L1e-A': 'Bicicle',
        'Camión rígido': 'Truck',
        'Tractocamión': 'Truck',
        'Vehículo articulado': 'Truck',
        'Camión de bomberos': 'Truck',
        'Autobús': 'Bus',
        'Autobús articulado': 'Bus',
        'Microbús <= 17 plazas': 'Bus',
        'Autobús articulado EMT': 'Bus',
        'Otros vehículos con motor': 'Other vehicle',
        'Patinete': 'Other vehicle',
        'Ciclo': 'Other vehicle',
        'VMU eléctrico': 'Other vehicle',
        'Semiremolque': 'Other vehicle',
        'Sin especificar': 'Other vehicle',
        'Autobus EMT': 'Other vehicle',
        'Remolque': 'Other vehicle',
        'Tranvía': 'Other vehicle',
        'Otros vehículos sin motor': 'Other vehicle',
        'Tren/metro': 'Other vehicle',
        'Ambulancia SAMUR': 'Other vehicle',
        'Maquinaria agrícola': 'Other vehicle',
        'Patinete no eléctrico': 'Other vehicle',
        'Maquinaria de obras': 'Other vehicle'
    })

    return df





if __name__ == "__main__":
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    origin_df = "./Data/Accidentalidad.xlsx"
    vehicle_types = "./Data/Clasification.xlsx"

    if os.path.exists(origin_df):
        df = pd.read_excel(origin_df)
        print(1)
    else:
        df = reading_and_unifying_files(years=years)
        df.to_excel(origin_df, index=False)
        print(2)

    df.drop(['coordenada_x_utm', 'coordenada_y_utm'], axis=1, inplace=True)

    df_renaming = renaming_values(df=df)

    print(df['tipo_vehiculo'].unique())


