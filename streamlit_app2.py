import pandas as pd
import altair as alt
import streamlit as st

# Caching the data to avoid reloading
@st.cache_data
def load_data():
    df = pd.read_csv("project_managment.csv")
    df= df.dropna()
    return df

df = load_data()

### Labels

df.columns = df.columns.str.strip()
unique_labels = df["Label"].drop_duplicates()
# Show a multiselect widget with the temperature points and other data columns
TP = st.multiselect(
    "Projectmanagment_labels",unique_labels)

# Remove any duplicate selections
TP = list(set(TP))

### zeitrange
df["Start"] = pd.to_datetime(df["Start"], format="%d.%m.%Y")
df["Ende"] = pd.to_datetime(df["Ende"], format="%d.%m.%Y")

# Get the earliest "Start" and latest "Ende" dates, converting them to Python's datetime type
start = df["Start"].min().to_pydatetime()
ende = df["Ende"].max().to_pydatetime()

# Create a slider for the time range based on the dataset
time_range = st.slider(
    "Select Time Range",
    min_value=start,
    max_value=ende,
    value=(start, ende),
    format="DD.MM.YYYY"  # Use European date format in the slider
)

st.write(f"Selected time range: {time_range[0].strftime('%d.%m.%Y')} to {time_range[1].strftime('%d.%m.%Y')}")




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
