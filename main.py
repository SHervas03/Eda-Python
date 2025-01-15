import pandas as pd
import os
import matplotlib.pyplot as plt


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
    df["tipo_vehiculo"] = df["tipo_vehiculo"].replace({
        "Turismo": "Car",
        "Ciclomotor": "Car",
        "Todo terreno": "Car",
        "Cuadriciclo no ligero": "Car",
        "Cuadriciclo ligero": "Car",
        "Ciclomotor de tres ruedas": "Car",
        "Motocicleta > 125cc": "Motorcicle",
        "Motocicleta hasta 125cc": "Motorcicle",
        "Moto de tres ruedas > 125cc": "Motorcicle",
        "Moto de tres ruedas hasta 125cc": "Motorcicle",
        "Ciclomotor de dos ruedas L1e-B": "Motorcicle",
        "Furgoneta": "Van",
        "Caravana": "Van",
        "Autocaravana": "Van",
        "Bicicleta": "Bicicle",
        "Bicicleta EPAC (pedaleo asistido)": "Bicicle",
        "Ciclo de motor L1e-A": "Bicicle",
        "Camión rígido": "Truck",
        "Tractocamión": "Truck",
        "Vehículo articulado": "Truck",
        "Camión de bomberos": "Truck",
        "Autobús": "Bus",
        "Autobús articulado": "Bus",
        "Microbús <= 17 plazas": "Bus",
        "Autobús articulado EMT": "Bus",
        "Otros vehículos con motor": "Other vehicle",
        "Patinete": "Other vehicle",
        "Ciclo": "Other vehicle",
        "VMU eléctrico": "Other vehicle",
        "Semiremolque": "Other vehicle",
        "Sin especificar": "Other vehicle",
        "Autobus EMT": "Other vehicle",
        "Remolque": "Other vehicle",
        "Tranvía": "Other vehicle",
        "Otros vehículos sin motor": "Other vehicle",
        "Tren/metro": "Other vehicle",
        "Ambulancia SAMUR": "Other vehicle",
        "Maquinaria agrícola": "Other vehicle",
        "Patinete no eléctrico": "Other vehicle",
        "Maquinaria de obras": "Other vehicle"
    })

    return df


def null_treatment(df):
    df.dropna(axis=1, how="all", inplace=True)
    df["positiva_droga"] = df["positiva_droga"].fillna(0)
    df["positiva_alcohol"] = df["positiva_alcohol"].fillna("N")
    df["lesividad"] = df["lesividad"].fillna("Sin atención sanitaria")
    df["cod_lesividad"] = df["cod_lesividad"].fillna(0)
    df["estado_meteorológico"] = df["estado_meteorológico"].fillna("Se desconoce")
    df.dropna(inplace=True)
    return df


def restructuringByPercentage(df):
    frequency = df["tipo_accidente"].value_counts(normalize=True) * 100
    minor_categories = frequency[frequency < 10].index
    df["tipo_accidente"] = df["tipo_accidente"].replace(minor_categories, "Other categories")
    return df


def alcohol_and_drug_testing(df):
    positiveResults = df[(df["positiva_alcohol"] == "S") & (df["positiva_droga"] == 1)]
    involved = positiveResults.groupby("num_expediente").size().sum()
    files = positiveResults["num_expediente"].nunique()
    print("Many involved in alcohol and drugs: ", involved)
    print("Different files: ", files, "\n")


def difference_between_positive_and_negative(df):
    positive = df[df["positiva_alcohol"] == "S"]
    negative = df[df["positiva_alcohol"] == "N"]
    frecuency_positive_type = positive.groupby("tipo_accidente").size().idxmax()
    frecuency_negative_type = negative.groupby("tipo_accidente").size().idxmax()
    frecuency_positive_munb = positive.groupby("tipo_accidente").size().max()
    frecuency_negative_munb = negative.groupby("tipo_accidente").size().max()

    print(f"Most common accident involving alcohol: {frecuency_positive_type} - {frecuency_positive_munb} cases")
    print(f"Most common accident without alcohol: {frecuency_negative_type} - {frecuency_negative_munb} cases\n")


def grouping_of_files(df):
    df_grouped = df.groupby("num_expediente")["tipo_vehiculo"].nunique().reset_index(name="implications")
    multiple_files = df_grouped[df_grouped['implications'] >= 5]
    number_of_files = multiple_files["num_expediente"].nunique()
    print("Number of files with 5 or more types of vehicle: ", number_of_files, "\n")

    implicated_by_case = df[df['num_expediente'].isin(multiple_files['num_expediente'])].groupby("num_expediente")[
        "tipo_vehiculo"].count().reset_index(name="number of times")
    print("Number of people involved in each case:\n ", implicated_by_case, "\n")

    types_of_vehicle = df[df['num_expediente'].isin(multiple_files['num_expediente'])].groupby("num_expediente")[
        "tipo_vehiculo"].unique().reset_index(name="types of vehicles")

    print("Different types of vehicles for each file:\n ", types_of_vehicle, "\n")


def display_times(df):
    df['hora'] = pd.to_datetime(df['hora'], format='%H:%M:%S')
    df['hora'] = df['hora'].dt.hour
    accidents_by_hour = df['hora'].value_counts().sort_index()

    plt.figure(figsize=(12, 6))
    plt.bar(accidents_by_hour.index, accidents_by_hour.values, color="blue")
    plt.title("Most dangerous hours to drive in Madrid")
    plt.xlabel("Time of day")
    plt.ylabel("Number of accidents")
    plt.xticks(rotation=0)
    plt.grid(axis="y")
    plt.show()


if __name__ == "__main__":
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    origin_df = "./Data/Accidentalidad.xlsx"
    vehicle_types = "./Data/Clasification.xlsx"

    if os.path.exists(origin_df):
        df = pd.read_excel(origin_df)
    else:
        df = reading_and_unifying_files(years=years)
        df.to_excel(origin_df, index=False)

    df.drop(["coordenada_x_utm", "coordenada_y_utm"], axis=1, inplace=True)

    # print(df["tipo_vehiculo"].unique)

    df_renaming = renaming_values(df=df)

    print("dataframe before cleaning: ", df.shape)
    df_clean = null_treatment(df_renaming)
    print("dataframe after cleaning: ", df.shape)

    df_percentage = restructuringByPercentage(df_clean)

    alcohol_and_drug_testing(df_percentage)

    difference_between_positive_and_negative(df_percentage)

    grouping_of_files(df_percentage)

    display_times(df_percentage)
