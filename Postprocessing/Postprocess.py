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
import plotly.graph_objects as go

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

def get_max_distance_by_voter(circuitos):
    """
    Reads data_modelo, result_model, and result_actual_model files for the given circuitos,
    and calculates the maximum distance assigned to a voter for both models.

    Args:
        circuitos (list of str): List of circuitos to process.

    Returns:
        tuple: (max_distance_nueva, max_distance_actual)
            - max_distance_nueva: Maximum distance assigned to a voter in the new model.
            - max_distance_actual: Maximum distance assigned to a voter in the actual model.
    """
    max_distance_nueva = 0
    max_distance_actual = 0

    for circuito in circuitos:
        # Load data_modelo
        with open(f'Preprocessing/data_modelo_{circuito}.pkl', 'rb') as f:
            data_modelo = pickle.load(f)
        
        # Extract distances dictionary
        distancias = data_modelo['distancias']

        # Load result_model and result_actual_model
        with open(f'Postprocessing/result_model_{circuito}.pkl', 'rb') as f:
            result_model = pickle.load(f)
        with open(f'Postprocessing/result_actual_model_{circuito}.pkl', 'rb') as f:
            result_actual_model = pickle.load(f)

        # Extract ASIGNACION_VOTANTE_ESCUELA for both models
        asignacion_nueva = result_model["solutions"]["ASIGNACION_VOTANTE_ESCUELA"]
        asignacion_actual = result_actual_model["solutions"]["ASIGNACION_VOTANTE_ESCUELA"]

        # Calculate maximum distance for the new model
        max_distance_nueva = max(
            max_distance_nueva,
            max(
                distancias[(votante, escuela)]
                for (votante, escuela), value in asignacion_nueva.items()
                if value == 1
            )
        )

        # Calculate maximum distance for the actual model
        max_distance_actual = max(
            max_distance_actual,
            max(
                distancias[(votante, escuela)]
                for (votante, escuela), value in asignacion_actual.items()
                if value == 1
            )
        )

    return max_distance_nueva, max_distance_actual


def metricas(circuitos=None, mapa_completo=True):
    """
    Calculates various metrics for the given circuitos or all data if mapa_completo is True.

    Args:
        circuitos (list of str): List of circuitos to process (e.g., ['11A']).
        mapa_completo (bool): Whether to process all data. Defaults to True.

    Returns:
        tuple: (distancia_total_nueva, distancia_total_actual, cantidad_votantes, max_distance_nueva, max_distance_actual)
            - distancia_total_nueva: Total distance for the new model.
            - distancia_total_actual: Total distance for the actual model.
            - cantidad_votantes: Total number of voters.
            - max_distance_nueva: Maximum distance assigned to a voter in the new model.
            - max_distance_actual: Maximum distance assigned to a voter in the actual model.
    """
    if mapa_completo:
        # Process all files
        distancia_total_nueva, cantidad_votantes_nueva = read_and_sum_objective_values('Postprocessing/result_model*.pkl')
        distancia_total_actual, cantidad_votantes_actual = read_and_sum_objective_values('Postprocessing/result_actual_model*.pkl')
        max_distance_nueva, max_distance_actual = get_max_distance_by_voter(
            [file.split('_')[-1].split('.')[0] for file in glob.glob('Preprocessing/data_modelo_*.pkl')]
        )
    else:
        # Process only files for the specified circuitos
        result_model_files_nueva = [f'Postprocessing/result_model_{circuito}.pkl' for circuito in circuitos]
        result_model_files_actual = [f'Postprocessing/result_actual_model_{circuito}.pkl' for circuito in circuitos]
        
        distancia_total_nueva, cantidad_votantes_nueva = read_and_sum_objective_values(result_model_files_nueva)
        distancia_total_actual, cantidad_votantes_actual = read_and_sum_objective_values(result_model_files_actual)
        max_distance_nueva, max_distance_actual = get_max_distance_by_voter(circuitos)

    if cantidad_votantes_nueva == cantidad_votantes_actual:
        cantidad_votantes = cantidad_votantes_nueva
        print('La cantidad de votantes asignados en el modelo actual y el nuevo es la misma')
    else:
        print('La cantidad de votantes asignados en el modelo actual y el nuevo es diferente')
        print(f'Cantidad de votantes asignados en el modelo actual: {cantidad_votantes_actual}')
        print(f'Cantidad de votantes asignados en el modelo nuevo: {cantidad_votantes_nueva}')
        
    return distancia_total_nueva, distancia_total_actual, cantidad_votantes, max_distance_nueva, max_distance_actual

def calculate_global_and_average_saving():
    """
    Calculates the global saving (ahorro), the average distance saving,
    the average distances for the nueva and actual models, and the time metrics.

    Returns:
        tuple: (global_actual, global_nuevo, global_saving, average_distance_saving, 
                average_distance_actual, average_distance_nueva, 
                global_time_saved, average_time_saved, average_time_actual, average_time_nueva)
            - global_actual: Total distance for the actual model.
            - global_nuevo: Total distance for the nueva model.
            - global_saving: Total saving across all circuitos.
            - average_distance_saving: Global saving divided by the total number of voters.
            - average_distance_actual: Average distance per voter for the actual model.
            - average_distance_nueva: Average distance per voter for the nueva model.
            - global_time_saved: Total time saved across all circuitos.
            - average_time_saved: Average time saved per voter.
            - average_time_actual: Average time per voter for the actual model.
            - average_time_nueva: Average time per voter for the nueva model.
    """
    # Get all result_model and result_model_actual files
    result_model_files = glob.glob('Postprocessing/result_model_*.pkl')
    result_model_actual_files = glob.glob('Postprocessing/result_actual_model_*.pkl')

    # Ensure the number of files match
    if len(result_model_files) != len(result_model_actual_files):
        raise ValueError("Mismatch in the number of result_model and result_model_actual files.")

    global_saving = 0
    total_voters = 0
    global_actual = 0
    global_nuevo = 0
    global_time_actual = 0
    global_time_nueva = 0

    # Iterate over all circuitos
    for result_model_file, result_model_actual_file in zip(result_model_files, result_model_actual_files):
        # Load result_model and result_model_actual
        with open(result_model_file, 'rb') as f:
            result_model = pickle.load(f)
        with open(result_model_actual_file, 'rb') as f:
            result_actual_model = pickle.load(f)

        # Extract the objective function values
        nuevo_value = result_model["Problem"][0]["Objetive value"]
        actual_value = result_actual_model["Problem"][0]["Objetive value"]

        # Calculate the saving for this circuito
        global_actual += actual_value
        global_nuevo += nuevo_value
        circuito_saving = actual_value - nuevo_value
        global_saving += circuito_saving

        # Count the number of voters in this circuito
        votantes = result_model["solutions"]["ASIGNACION_VOTANTE_ESCUELA"]
        total_voters += sum(value == 1 for value in votantes.values())

        # Calculate time for actual and nueva
        time_actual = (actual_value / 2) / 20 + (actual_value / 2) / 4  # Half at 20 km/h, half at 4 km/h
        time_nueva = (nuevo_value / 2) / 20 + (nuevo_value / 2) / 4  # Half at 20 km/h, half at 4 km/h
        global_time_actual += time_actual
        global_time_nueva += time_nueva

    # Calculate the average distance saving
    average_distance_saving = global_saving / total_voters if total_voters > 0 else 0

    # Calculate the average distances for nueva and actual
    average_distance_actual = global_actual / total_voters if total_voters > 0 else 0
    average_distance_nueva = global_nuevo / total_voters if total_voters > 0 else 0

    # Calculate the global time saved
    global_time_saved = global_time_actual - global_time_nueva

    # Calculate the average time saved and average times for nueva and actual
    average_time_saved = global_time_saved / total_voters if total_voters > 0 else 0
    average_time_actual = global_time_actual / total_voters if total_voters > 0 else 0
    average_time_nueva = global_time_nueva / total_voters if total_voters > 0 else 0

    return (global_actual, global_nuevo, global_saving, average_distance_saving, 
            average_distance_actual, average_distance_nueva, 
            global_time_saved, average_time_saved, average_time_actual, average_time_nueva)
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
    distances_actual = {}
    distances_nueva = {}

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

            # Store distances for the circuito
            distances_nueva[circuito] = nuevo_value
            distances_actual[circuito] = actual_value

            # Calculate the savings (actual - nuevo)
            savings[circuito] = actual_value - nuevo_value
        except FileNotFoundError:
            # If files are missing, set savings and distances to None
            savings[circuito] = None
            distances_nueva[circuito] = None
            distances_actual[circuito] = None

    # Add the savings and distances data to the GeoDataFrame
    gdf['savings'] = gdf['circuito'].map(savings)
    gdf['distancia_actual'] = gdf['circuito'].map(distances_actual)
    gdf['distancia_nueva'] = gdf['circuito'].map(distances_nueva)

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
        popup_text = (
            f"Circuito: {row['circuito']}<br>"
            f"Distancia actual: {row['distancia_actual']:.2f} km<br>"
            f"Distancia nueva: {row['distancia_nueva']:.2f} km<br>"
            f"Ahorro: {row['savings']:.2f} km"
            if row['savings'] is not None else
            f"Circuito: {row['circuito']}<br>Savings (Ahorro): N/A"
        )

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

def create_distance_histograms_plotly(circuito):
    """
    Reads data_modelo and result_model files for a given circuito, extracts distances,
    and creates histograms for the distances in the actual and new models using Plotly.
    Saves the histograms as pickle files.
    
    Args:
        circuito (str): The circuito identifier (e.g., '11A').
    """
    # Load data_modelo
    with open(f'Preprocessing/data_modelo_{circuito}.pkl', 'rb') as f:
        data_modelo = pickle.load(f)
    
    # Extract distances dictionary
    distancias = data_modelo['distancias']
    df_distancias = pd.DataFrame(
        [(votante, escuela, distancia) for (votante, escuela), distancia in distancias.items()],
        columns=['VOTANTE', 'ESCUELA', 'DISTANCIA']
    )
    
    # Load result_model and result_model_actual
    with open(f'Postprocessing/result_model_{circuito}.pkl', 'rb') as f:
        result_model = pickle.load(f)
    with open(f'Postprocessing/result_actual_model_{circuito}.pkl', 'rb') as f:
        result_model_actual = pickle.load(f)
    
    # Extract ASIGNACION_VOTANTE_ESCUELA for both models
    asignacion_nueva = result_model["solutions"]["ASIGNACION_VOTANTE_ESCUELA"]
    asignacion_actual = result_model_actual["solutions"]["ASIGNACION_VOTANTE_ESCUELA"]
    
    # Create DataFrames for the assignments
    df_asignacion_nueva = pd.DataFrame(
        [(votante, escuela) for (votante, escuela), value in asignacion_nueva.items() if value == 1],
        columns=['VOTANTE', 'ESCUELA']
    )
    df_asignacion_actual = pd.DataFrame(
        [(votante, escuela) for (votante, escuela), value in asignacion_actual.items() if value == 1],
        columns=['VOTANTE', 'ESCUELA']
    )
    
    # Merge with distances
    df_nueva = pd.merge(df_asignacion_nueva, df_distancias, on=['VOTANTE', 'ESCUELA'], how='left')
    df_actual = pd.merge(df_asignacion_actual, df_distancias, on=['VOTANTE', 'ESCUELA'], how='left')
    
    # Create Plotly histograms
    fig_nueva = go.Figure()
    fig_nueva.add_trace(go.Histogram(
        x=df_nueva['DISTANCIA'],
        nbinsx=20,  # Number of bins
        name='Modelo Nuevo',
        marker=dict(color='blue'),
        opacity=0.7
    ))
    fig_nueva.update_layout(
        # title=f'Histograma de Distancias - Modelo Nuevo (Circuito {circuito})',
        xaxis_title='Distancia por persona (km)',
        yaxis_title='Frecuencia',
        template='plotly_white',
        margin=dict(t=0)  # Remove space above the plot
    )
    
    fig_actual = go.Figure()
    fig_actual.add_trace(go.Histogram(
        x=df_actual['DISTANCIA'],
        nbinsx=20,  # Number of bins
        name='Modelo Actual',
        marker=dict(color='orange'),
        opacity=0.7
    ))
    fig_actual.update_layout(
        # title=f'Histograma de Distancias - Modelo Actual (Circuito {circuito})',
        xaxis_title='Distancia por persona (km)',
        yaxis_title='Frecuencia',
        template='plotly_white',
        margin=dict(t=0)  # Remove space above the plot
    )
    
    # Save the histograms as pickle files
    with open(f'Postprocessing/histogram_nueva_{circuito}.pkl', 'wb') as f:
        pickle.dump(fig_nueva, f)
    with open(f'Postprocessing/histogram_actual_{circuito}.pkl', 'wb') as f:
        pickle.dump(fig_actual, f)
    
    print(f"Histograms saved as pickle files for circuito {circuito}.")
    
def create_distance_histograms_all_circuitos():
    """
    Reads all data_modelo, result_model, and result_actual_model files for all circuitos,
    aggregates the distances, and creates histograms for the distances in the actual and new models.
    Saves the histograms as pickle files.
    """
    # Initialize empty DataFrames for aggregated data
    df_distancias_all = pd.DataFrame(columns=['VOTANTE', 'ESCUELA', 'DISTANCIA'])
    df_nueva_all = pd.DataFrame(columns=['VOTANTE', 'ESCUELA', 'DISTANCIA'])
    df_actual_all = pd.DataFrame(columns=['VOTANTE', 'ESCUELA', 'DISTANCIA'])

    # Get all circuito files
    data_modelo_files = glob.glob('Preprocessing/data_modelo_*.pkl')
    result_model_files = glob.glob('Postprocessing/result_model_*.pkl')
    result_actual_model_files = glob.glob('Postprocessing/result_actual_model_*.pkl')

    # Ensure the number of files match
    if len(result_model_files) != len(result_actual_model_files):
        raise ValueError("Mismatch in the number of result_model and result_actual_model files.")

    # Iterate over all circuitos
    for data_modelo_file, result_model_file, result_actual_model_file in zip(data_modelo_files, result_model_files, result_actual_model_files):
        # Load data_modelo
        with open(data_modelo_file, 'rb') as f:
            data_modelo = pickle.load(f)
        
        # Extract distances dictionary
        distancias = data_modelo['distancias']
        df_distancias = pd.DataFrame(
            [(votante, escuela, distancia) for (votante, escuela), distancia in distancias.items()],
            columns=['VOTANTE', 'ESCUELA', 'DISTANCIA']
        )
        df_distancias_all = pd.concat([df_distancias_all, df_distancias], ignore_index=True)

        # Load result_model and result_actual_model
        with open(result_model_file, 'rb') as f:
            result_model = pickle.load(f)
        with open(result_actual_model_file, 'rb') as f:
            result_actual_model = pickle.load(f)

        # Extract ASIGNACION_VOTANTE_ESCUELA for both models
        asignacion_nueva = result_model["solutions"]["ASIGNACION_VOTANTE_ESCUELA"]
        asignacion_actual = result_actual_model["solutions"]["ASIGNACION_VOTANTE_ESCUELA"]

        # Create DataFrames for the assignments
        df_asignacion_nueva = pd.DataFrame(
            [(votante, escuela) for (votante, escuela), value in asignacion_nueva.items() if value == 1],
            columns=['VOTANTE', 'ESCUELA']
        )
        df_asignacion_actual = pd.DataFrame(
            [(votante, escuela) for (votante, escuela), value in asignacion_actual.items() if value == 1],
            columns=['VOTANTE', 'ESCUELA']
        )

        # Merge with distances
        df_nueva = pd.merge(df_asignacion_nueva, df_distancias, on=['VOTANTE', 'ESCUELA'], how='left')
        df_actual = pd.merge(df_asignacion_actual, df_distancias, on=['VOTANTE', 'ESCUELA'], how='left')

        # Append to aggregated DataFrames
        df_nueva_all = pd.concat([df_nueva_all, df_nueva], ignore_index=True)
        df_actual_all = pd.concat([df_actual_all, df_actual], ignore_index=True)

    # Create Plotly histograms
    fig_nueva = go.Figure()
    fig_nueva.add_trace(go.Histogram(
        x=df_nueva_all['DISTANCIA'],
        nbinsx=20,  # Number of bins
        name='Modelo Nuevo',
        marker=dict(color='blue'),
        opacity=0.7
    ))
    fig_nueva.update_layout(
        # title='Histograma de Distancias - Modelo Nuevo (Todos los Circuitos)',
        xaxis_title='Distancia por persona (km)',
        yaxis_title='Frecuencia',
        template='plotly_white',
        margin=dict(t=0)  # Remove space above the plot
    )

    fig_actual = go.Figure()
    fig_actual.add_trace(go.Histogram(
        x=df_actual_all['DISTANCIA'],
        nbinsx=20,  # Number of bins
        name='Modelo Actual',
        marker=dict(color='orange'),
        opacity=0.7
    ))
    fig_actual.update_layout(
        # title='Histograma de Distancias - Modelo Actual (Todos los Circuitos)',
        xaxis_title='Distancia por persona (km)',
        yaxis_title='Frecuencia',
        template='plotly_white',
        margin=dict(t=0)  # Remove space above the plot
    )

    # Save the histograms as pickle files
    with open('Postprocessing/histogram_nueva_all.pkl', 'wb') as f:
        pickle.dump(fig_nueva, f)
    with open('Postprocessing/histogram_actual_all.pkl', 'wb') as f:
        pickle.dump(fig_actual, f)

    print("Histograms saved as pickle files for all circuitos.")