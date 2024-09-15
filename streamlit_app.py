import pandas as pd
import altair as alt
import streamlit as st

# Caching the data to avoid reloading
@st.cache_data
def load_data():
    df = pd.read_csv("test_temperature_data.csv")
    return df

df = load_data()

# Show a multiselect widget with the temperature points and other data columns
TP = st.multiselect(
    "Temperature Point/Parameter",
    df.columns,
    ["Temperature_Point_1", "Temperature_Point_2", "Temperature_Point_3", "Temperature_Point_5", "Temperature_Point_6", "Current (A)", "Voltage (V)"],
)

# Remove any duplicate selections
TP = list(set(TP))

# Show a slider widget for the temperature range
temp_range = st.slider("Temperature Range (°C)", 25, 100, (25, 100))

# Filter the dataframe based on the selected temperature range (assumes we are focusing on Temperature_Point_1 for this filter)
df_filtered = df[(df["Temperature_Point_1"].between(temp_range[0], temp_range[1]))]

# Reshape the dataframe to have temperature points and current/voltage data
df_reshaped = df_filtered[TP]

# Display the filtered data as a table
st.dataframe(
    df_reshaped,
    use_container_width=True,
)

# Preparing the data for visualization with Altair
df_chart = pd.melt(
    df_reshaped.reset_index(), id_vars="index", var_name="Parameter", value_name="Value"
)

# Create a chart
chart = (
    alt.Chart(df_chart)
    .mark_line()
    .encode(
        x=alt.X("index:N", title="Index"),
        y=alt.Y("Value:Q", title="Measured Values"),
        color="Parameter:N",
    )
    .properties(height=320)
)

# Display the chart
st.altair_chart(chart, use_container_width=True)
