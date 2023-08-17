import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Analysis Tool",
                   page_icon=":chart_with_upwards_trend:", layout="wide")

st.title(" :bar_chart: Simple SuperStore EDA")
st.markdown(
    '<style> div.block-container{padding-top:1rem;} </style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file",
                      type=(["csv", "txt", "xlsx", "xls"]))

if fl is not None:
    fileName = fl
    st.write(fileName)
    df = pd.read_csv(fileName)
else:
    os.chdir(r"C:\Users\WOFA K\Desktop\React\godwinpro")
    df = pd.read_csv('test-measures_uk1.csv')



df = pd.DataFrame(df)




st.sidebar.header("Choose your filter: ")
# data_col = st.sidebar.multiselect("Pick your Column", df.columns.unique())
# x_column = st.sidebar.selectbox("Choose x-axis column", df.columns)
data_type = st.sidebar.radio(
    "Select Data Representation Type", ("Scatter Plot", "Bar Chart", "Time Series", "Pie Chart", "scatter_geo"))


# Check for a date column
has_date_column = False

# for column in df.columns:
    # if pd.api.types.is_datetime64_any_dtype(df[column]):
if 'Date' in df.columns or 'date' in df.columns:
    has_date_column = True
    # break

if has_date_column:
    print("The DataFrame has a date column.")
    col1, col2 = st.columns((2))
    df["Date"] = pd.to_datetime(df["Date"])

    # Getting the min and max date
    startDate = pd.to_datetime(df["Date"]).min()
    endDate = pd.to_datetime(df["Date"]).max()

    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))

    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

    df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()
    if data_type == "Scatter Plot":
    # Dropdowns for x and y columns
        with col1:
            x_column = st.selectbox("Choose x-axis column", df.columns)
        with col2:
            y_column = st.selectbox("Choose y-axis column", df.columns)

    # Create a scatter plot using Plotly Express
        fig = px.scatter(df, x=x_column, y=y_column,
                     title=f"{y_column} vs {x_column}")

    elif data_type == "Bar Chart":
    # Dropdowns for x and y columns
        with col1:
            x_column = st.selectbox("Choose x-axis column", df.columns)
        with col2:
            y_column = st.selectbox("Choose y-axis column", df.columns)

    # Groupby column (categorical) for the bar chart
        with col1:
            groupby_column = st.selectbox("Choose grouping column", df.columns)

    # Create a bar chart using Plotly Express
        fig = px.bar(df, x=x_column, y=y_column, color=groupby_column,
                 title=f"{y_column} vs {x_column} by {groupby_column}")

    elif data_type == "Time Series":
        # Dropdowns for x and y columns
        with col1:
            x_column = st.selectbox("Choose x-axis column", df.columns)
        with col2: 
            y_column = st.selectbox("Choose y-axis column", df.columns)

    # Convert 'x_column' to datetime if needed
        if pd.api.types.is_string_dtype(df[x_column]):
            df[x_column] = pd.to_datetime(df[x_column])

# Create a time series plot using Plotly Express
        fig = px.line(df, x=x_column, y=y_column, title=f"{y_column} over Time")

    elif data_type == "Pie Chart":
        # Dropdown for categorical column
        category_column = st.selectbox("Choose categorical column", df.columns)

        # Create a pie chart using Plotly Express
        fig = px.pie(df, names=category_column,
                 title=f"Pie Chart of {category_column}")
 
# st.plotly_chart(fig)

else:
    center_lat = 51.53282
    center_lon = -0.4767624
    zom = 5
    print("The DataFrame does not have a date column.")
    if data_type == "scatter_geo":
        # Load the GeoJSON data for the UK (replace with the actual file path)
        with open('ukmap.json', encoding="utf8") as geojson_file:
            uk_geojson = geojson_file.read()

        # Create a choropleth map using go.Choroplethmapbox
        choropleth_map = go.Choroplethmapbox(geojson=uk_geojson,
                                     locations=[0],  # This can be any value
                                     z=[0],  # This can be any value
                                     colorscale='Viridis',
                                     marker_opacity=1,
                                     marker_line_width=0,
                                     colorbar_title='Colorbar')

        # Set the layout for the choropleth map
        layout = go.Layout(mapbox_style="carto-positron",
                   mapbox_zoom=9,
                   mapbox_center={"lat": center_lat, "lon": center_lon})  # Centered around London

        # Create the figure containing the choropleth map
        fig = go.Figure(choropleth_map, layout)

        # Add individual markers using go.Scattermapbox
        markers = go.Scattermapbox(lat=df['y'],
                            lon=df['x'],
                            mode='markers',
                            marker=dict(size=8, color='blue', opacity=1),
                            text=df['name'].astype(str))

        # Add the markers to the figure
        fig.add_trace(markers)

# Show the combined figure
# fig.show()


        # Show the map
        # fig.show()

        # Create a scatter map using Plotly Express
    #     fig = px.scatter_geo(df, 
    #     lat='y', 
    #     lon='x', 
    #     title='Brunel Buidings Location',   
    #     # text='name', 
    #     color='name', 
    #     scope='europe',
    #     center={'lat': center_lat, 'lon': center_lon},
    #     # zoom=zom,
    #     size='area', 
    #     # hover_data={'Latitude': ':.y', 'Longitude': ':.x'}, 
    #     template='plotly_dark', 
    #     # projection='orthographic'
    #     )
    # # fig.show()

st.plotly_chart(fig)
 





# Display the selected plot using Streamlit
# st.plotly_chart(fig)

# Display the raw data
st.subheader("Raw Data")
st.write(df)
