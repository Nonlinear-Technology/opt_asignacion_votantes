# %%
# import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import pickle
import folium
from folium.plugins import MarkerCluster
# from folium.plugins import MarkerCluster
# from streamlit_folium import folium_static
import glob
import random

def read_and_concatenate_files(pattern_or_files):
    if isinstance(pattern_or_files, str):
        # If a string pattern is provided, use glob to find matching files
        files = glob.glob(pattern_or_files)
    elif isinstance(pattern_or_files, list):
        # If a list of files is provided, use it directly
        files = pattern_or_files
    else:
        raise ValueError("Invalid input: expected a string pattern or a list of file paths.")
    
    df_list = [pd.read_excel(file) for file in files]
    return pd.concat(df_list, ignore_index=True)

def read_and_concatenate_result_models(pattern_or_files):
    if isinstance(pattern_or_files, str):
        # If a string pattern is provided, use glob to find matching files
        files = glob.glob(pattern_or_files)
    elif isinstance(pattern_or_files, list):
        # If a list of files is provided, use it directly
        files = pattern_or_files
    else:
        raise ValueError("Invalid input: expected a string pattern or a list of file paths.")
    
    df_list = []
    for file in files:
        with open(file, 'rb') as f:
            result_model = pickle.load(f)
            asignacion_nueva = result_model["solutions"]["ASIGNACION_VOTANTE_ESCUELA"]
            filtered_keys = [key for key, value in asignacion_nueva.items() if value == 1]
            df_asignacion_nueva = pd.DataFrame(filtered_keys, columns=['VOTANTE', 'ESCUELA'])
            df_list.append(df_asignacion_nueva)
    return pd.concat(df_list, ignore_index=True)

def read_and_sum_objective_values(pattern_or_files):
    """
    Reads all result_model files, extracts the objective values, sums them up,
    and counts the number of activated variables (voters).
    
    Args:
        pattern_or_files (str or list): A string pattern to match files or a list of file paths.
    
    Returns:
        tuple: (total_objective_value, total_activated_variables)
            - total_objective_value: The sum of all objective values from the result_model files.
            - total_activated_variables: The total number of activated variables (voters).
    """
    if isinstance(pattern_or_files, str):
        # If a string pattern is provided, use glob to find matching files
        files = glob.glob(pattern_or_files)
    elif isinstance(pattern_or_files, list):
        # If a list of files is provided, use it directly
        files = pattern_or_files
    else:
        raise ValueError("Invalid input: expected a string pattern or a list of file paths.")
    
    total_objective_value = 0.0  # Initialize the sum of objective values
    total_activated_variables = 0  # Initialize the count of activated variables
    
    for file in files:
        with open(file, 'rb') as f:
            result_model = pickle.load(f)
            
            # Extract the objective value
            objective_value = result_model["Problem"][0]["Objetive value"]
            total_objective_value += objective_value  # Add to the total
            
            # Count the number of activated variables (voters)
            asignacion_votante_escuela = result_model["solutions"]["ASIGNACION_VOTANTE_ESCUELA"]
            activated_variables = sum(value == 1 for value in asignacion_votante_escuela.values())
            total_activated_variables += activated_variables  # Add to the total count
    
    return total_objective_value, total_activated_variables

def create_map(df, title):
        # Ensure the required columns exist
        if 'VOTANTE' not in df.columns or 'Latitude_votante' not in df.columns or 'Longitude_votante' not in df.columns:
            raise KeyError("Required columns ('VOTANTE', 'Latitude_votante', 'Longitude_votante') are missing in the DataFrame.")
        
        # Create a map centered around the average latitude and longitude
        map_center = [df['Latitude_escuela'].mean(), df['Longitude_escuela'].mean()]
        m = folium.Map(location=map_center, zoom_start=12)
        
        # Define colors for the schools
        colors = ['blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
        
        # Add schools to the map with different colors
        school_colors = {}
        for i, (_, row) in enumerate(df.drop_duplicates(subset=['ESCUELA']).iterrows()):
            color = colors[i % len(colors)]
            school_colors[row['ESCUELA']] = color
            folium.Marker(
                location=[row['Latitude_escuela'], row['Longitude_escuela']],
                popup=row['ESCUELA'],
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(m)
        
        # Add voters to the map
        for _, row in df.iterrows():
            school_color = school_colors.get(row['ESCUELA'], 'gray')  # Default to gray if school not found
            
            # Apply a small random offset to overlapping points
            jitter_lat = random.uniform(-0.0001, 0.0001)  # Small random offset for latitude
            jitter_lon = random.uniform(-0.0001, 0.0001)  # Small random offset for longitude
            adjusted_lat = row['Latitude_votante'] + jitter_lat
            adjusted_lon = row['Longitude_votante'] + jitter_lon
            
            folium.CircleMarker(
                location=[adjusted_lat, adjusted_lon],
                radius=5,  # Adjust the size of the point
                color=school_color,
                fill=True,
                fill_color=school_color,
                fill_opacity=0.6,
                popup=f"VOTANTE: {row['VOTANTE']}<br>ESCUELA: {row['ESCUELA']}"
            ).add_to(m)
        
        return m

def postprocessing(circuitos=None, mapa_completo=True):
    """
    Process electoral data for specified circuitos or all data if mapa_completo is True.
    
    Args:
        circuitos (list of str): List of circuitos to process (e.g., ['11A']).
        mapa_completo (bool): Whether to process all data. Defaults to True.
    """
    if mapa_completo:
        # Process all files
        df_asignacion_nueva = read_and_concatenate_result_models('Postprocessing/result_model*.pkl')
        df_asignacion_actual = read_and_concatenate_result_models('Postprocessing/result_actual_model*.pkl')
        df_escuelas = read_and_concatenate_files('Preprocessing/escuelas_geolocalizadas*.xlsx')
    else:
        # Process only files for the specified circuitos
        result_model_files_nueva = [f'Postprocessing/result_model_{circuito}.pkl' for circuito in circuitos]
        result_model_files_actual = [f'Postprocessing/result_actual_model_{circuito}.pkl' for circuito in circuitos]
        escuelas_files = [f'Preprocessing/escuelas_geolocalizadas_{circuito}.xlsx' for circuito in circuitos]
        
        df_asignacion_nueva = read_and_concatenate_result_models(result_model_files_nueva)
        df_asignacion_actual = read_and_concatenate_result_models(result_model_files_actual)
        df_escuelas = read_and_concatenate_files(escuelas_files)
    
    # Process escuelas data
    df_escuelas = df_escuelas[['Escuela', 'Latitude', 'Longitude', 'Desde', 'Hasta']].rename(
        columns={'Escuela': 'ESCUELA', 'Latitude': 'Latitude_escuela', 'Longitude': 'Longitude_escuela'}
    )
    df_escuelas.to_clipboard()
    
    # Process nueva assignment
    df_asignacion_nueva = pd.merge(df_asignacion_nueva, df_escuelas, on='ESCUELA', how='left')
    df_asignacion_nueva['VOTANTE'] = df_asignacion_nueva['VOTANTE'].astype(str)
    
    # Process votantes data
    if mapa_completo:
        df_votantes = read_and_concatenate_files('Preprocessing/votantes_geolocalizados*.xlsx')
    else:
        votantes_files = [f'Preprocessing/votantes_geolocalizados_{circuito}.xlsx' for circuito in circuitos]
        df_votantes = read_and_concatenate_files(votantes_files)
    
    df_votantes = df_votantes[['DNI', 'Latitude', 'Longitude', 'Mesa Actual']].rename(
        columns={'DNI': 'VOTANTE', 'Latitude': 'Latitude_votante', 'Longitude': 'Longitude_votante'}
    ).dropna()
    
    # Ensure VOTANTE column in both DataFrames is of the same type
    df_asignacion_nueva['VOTANTE'] = df_asignacion_nueva['VOTANTE'].astype(float)
    df_votantes['VOTANTE'] = pd.to_numeric(df_votantes['VOTANTE'], errors='coerce')
    df_votantes.dropna(subset=['VOTANTE'], inplace=True)
    df_votantes['VOTANTE'] = df_votantes['VOTANTE'].astype(float)
    
    # Merge nueva assignment with votantes
    df_asignacion_nueva = pd.merge(df_asignacion_nueva, df_votantes, on='VOTANTE', how='inner')
    
    
    # Create the map for the nueva assignment
    map_nueva = create_map(df_asignacion_nueva, 'Asignación Nueva')
    
    # Process actual assignment
    df_asignacion_actual = pd.merge(df_asignacion_actual, df_escuelas, on='ESCUELA', how='left')
    df_asignacion_actual['VOTANTE'] = df_asignacion_actual['VOTANTE'].astype(float)
    
    # Merge actual assignment with votantes
    df_asignacion_actual = pd.merge(df_asignacion_actual, df_votantes, on='VOTANTE', how='inner')
    
    # Create the map for the actual assignment
    map_actual = create_map(df_asignacion_actual, 'Asignación Actual')
    
    if circuitos is not None:
        circuito = circuitos[0]
    
        # Save the maps
        with open(f'Postprocessing/mapa_nuevo_{circuito}.pkl', 'wb') as f:
            pickle.dump(map_nueva, f)
            
        with open(f'Postprocessing/mapa_actual_{circuito}.pkl', 'wb') as f:
            pickle.dump(map_actual, f)
    
    # return map_nueva, map_actual
# postprocessing()

# # Streamlit app
# st.title('Asignación de votantes')

# # Generate the maps
# map_nueva, map_actual = postprocessing()

# # Display the maps using Streamlit
# st.header('Asignación Nueva')
# folium_static(map_nueva)

# st.header('Asignación Actual')
# folium_static(map_actual)

# %%

def metricas(circuitos=None, mapa_completo=True):
    
    if mapa_completo:
        # Process all files
        distancia_total_nueva, cantidad_votantes_nueva = read_and_sum_objective_values('Postprocessing/result_model*.pkl')
        distancia_total_actual, cantidad_votantes_actual = read_and_sum_objective_values('Postprocessing/result_actual_model*.pkl')
    else:
        # Process only files for the specified circuitos
        result_model_files_nueva = [f'Postprocessing/result_model_{circuito}.pkl' for circuito in circuitos]
        result_model_files_actual = [f'Postprocessing/result_actual_model_{circuito}.pkl' for circuito in circuitos]
        
        distancia_total_nueva, cantidad_votantes_nueva = read_and_sum_objective_values(result_model_files_nueva)
        distancia_total_actual, cantidad_votantes_actual = read_and_sum_objective_values(result_model_files_actual)
        
    if cantidad_votantes_nueva == cantidad_votantes_actual:
        cantidad_votantes = cantidad_votantes_nueva
        print('La cantidad de votantes asignados en el modelo actual y el nuevo es la misma')
    else:
        print('La cantidad de votantes asignados en el modelo actual y el nuevo es diferente')
        print(f'Cantidad de votantes asignados en el modelo actual: {cantidad_votantes_actual}')
        print(f'Cantidad de votantes asignados en el modelo nuevo: {cantidad_votantes_nueva}')
        
    return distancia_total_nueva, distancia_total_actual, cantidad_votantes

def calculate_global_and_average_saving():
    """
    Calculates the global saving (ahorro) and the average distance saving
    by processing all result_model and result_model_actual files.

    Returns:
        tuple: (global_saving, average_distance_saving)
            - global_saving: Total saving across all circuitos.
            - average_distance_saving: Global saving divided by the total number of voters.
    """
    # Get all result_model and result_model_actual files
    result_model_files = glob.glob('Postprocessing/result_model_*.pkl')
    result_model_actual_files = glob.glob('Postprocessing/result_actual_model_*.pkl')

    # Ensure the number of files match
    if len(result_model_files) != len(result_model_actual_files):
        raise ValueError("Mismatch in the number of result_model and result_model_actual files.")

    global_saving = 0
    total_voters = 0

    # Iterate over all circuitos
    for result_model_file, result_model_actual_file in zip(result_model_files, result_model_actual_files):
        # Load result_model and result_model_actual
        with open(result_model_file, 'rb') as f:
            result_model = pickle.load(f)
        with open(result_model_actual_file, 'rb') as f:
            result_model_actual = pickle.load(f)

        # Extract the objective function values
        nuevo_value = result_model["Problem"][0]["Objetive value"]
        actual_value = result_model_actual["Problem"][0]["Objetive value"]

        # Calculate the saving for this circuito
        circuito_saving = actual_value - nuevo_value
        global_saving += circuito_saving

        # Count the number of voters in this circuito
        votantes = result_model["solutions"]["ASIGNACION_VOTANTE_ESCUELA"]
        total_voters += sum(value == 1 for value in votantes.values())

    # Calculate the average distance saving
    average_distance_saving = global_saving / total_voters if total_voters > 0 else 0

    return global_saving, average_distance_saving
# %%
def create_heatmap_with_savings():
    """
    Creates a heat map of Santa Fe circuitos based on the difference in objective function values
    (actual - nuevo) using the circ_santafe23.geojson file and result_model pickles.
    """
    # Load the GeoJSON file
    geojson_path = './Postprocessing/circ_santafe23.geojson'
    gdf = gpd.read_file(geojson_path)

    # Initialize a dictionary to store savings (ahorro) for each circuito
    savings = {}

    # Iterate over each circuito and calculate the savings
    for circuito in gdf['circuito']:
        try:
            # Load the result_model and result_actual_model pickles for the circuito
            with open(f'./Postprocessing/result_model_{circuito}.pkl', 'rb') as f:
                result_model = pickle.load(f)
            with open(f'./Postprocessing/result_actual_model_{circuito}.pkl', 'rb') as f:
                result_actual_model = pickle.load(f)

            # Extract the objective function values
            nuevo_value = result_model["Problem"][0]["Objetive value"]
            actual_value = result_actual_model["Problem"][0]["Objetive value"]

            # Calculate the savings (actual - nuevo)
            savings[circuito] = actual_value - nuevo_value
        except FileNotFoundError:
            # If files are missing, set savings to None
            savings[circuito] = None

    # Add the savings data to the GeoDataFrame
    gdf['savings'] = gdf['circuito'].map(savings)

    # Clean the savings column (remove None or NaN values)
    gdf['savings'] = gdf['savings'].fillna(0)  # Replace None/NaN with 0 (or another default value)

    # Normalize the savings for color mapping
    min_savings = gdf['savings'].min()
    max_savings = gdf['savings'].max()
    if min_savings == max_savings:
        # Avoid division by zero if all savings are the same
        gdf['normalized_savings'] = 0.5  # Set all to the middle of the gradient
    else:
        gdf['normalized_savings'] = gdf['savings'].apply(
            lambda x: (x - min_savings) / (max_savings - min_savings)
        )

    # Create a folium map centered on Santa Fe
    map_center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
    m = folium.Map(location=map_center, zoom_start=10)

    # Define a colormap for the gradient (shades of green)
    colormap = folium.LinearColormap(
        colors=['#e5f5e0', '#a1d99b', '#31a354'],  # Light green to dark green
        vmin=min_savings,
        vmax=max_savings,
        caption='Savings (Ahorro)'
    )
    colormap.add_to(m)

    # Add polygons and labels to the map
    for _, row in gdf.iterrows():
        color = colormap(row['savings']) if row['savings'] is not None else 'gray'
        popup_text = f"Circuito: {row['circuito']}<br>Ahorro: {row['savings']:.2f} km" if row['savings'] is not None else f"Circuito: {row['circuito']}<br>Savings (Ahorro): N/A"
        
        # Add the polygon to the map
        folium.GeoJson(
            row['geometry'],
            style_function=lambda feature, color=color: {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7,
            },
            tooltip=popup_text
        ).add_to(m)

        # # Add a label above the polygon with the ahorro value
        # centroid = row['geometry'].centroid
        # folium.map.Marker(
        #     [centroid.y, centroid.x],
        #     icon=folium.DivIcon(
        #         html=f'<div style="font-size: 12px; color: black; text-align: center;">{row["savings"]:.2f}</div>'
        #     )
        # ).add_to(m)

    # Save the map to an HTML file
    m.save('./Postprocessing/savings_heatmap.html')

    return m

m = create_heatmap_with_savings()
# %%
def create_circuitos_map_with_labels():
    """
    Creates a map of Santa Fe circuitos with labeled polygons.
    Each polygon is labeled with its circuito name.
    """
    # Load the GeoJSON file
    geojson_path = './Postprocessing/circ_santafe23.geojson'
    gdf = gpd.read_file(geojson_path)

    # Create a folium map centered on Santa Fe
    map_center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
    m = folium.Map(location=map_center, zoom_start=10)

    # Add polygons and labels to the map
    for _, row in gdf.iterrows():
        # Add the polygon to the map
        folium.GeoJson(
            row['geometry'],
            style_function=lambda feature: {
                'fillColor': '#add8e6',  # Light blue color
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.5,
            },
            tooltip=f"Circuito: {row['circuito']}"
        ).add_to(m)

        # Add a fancy label above the polygon
        centroid = row['geometry'].centroid
        folium.Marker(
            [centroid.y, centroid.x],
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size: 14px;
                    font-weight: bold;
                    color: black;
                    text-align: center;">
                    {row['circuito']}
                </div>
                """
            )
        ).add_to(m)

    # Save the map to an HTML file
    m.save('./Postprocessing/circuitos_map_with_labels.html')

    return m