import streamlit as st
import pandas as pd
import seaborn as sns
import math  
import matplotlib.pyplot as plt

# dataset
st.header('Application : HW 4 (CMSE 830)')
st.subheader('Developed by Md Arifuzzaman Faisal')

# List of dataset filenames
data = "water_potability.csv"
dataset_name = "Water Potability"
df = pd.read_csv(data)
st.header(f'Name of the dataset : {dataset_name}')

message = "Context: Access to safe drinking-water is essential to health, a basic human right and a component of effective policy for health protection. This is important as a health and development issue at a national, regional and local level. In some regions, it has been shown that investments in water supply and sanitation can yield a net economic benefit, since the reductions in adverse health effects and health care costs outweigh the costs of undertaking the interventions."
st.write(message)
# Add an image
st.image("dw.jpg", caption="Is the water safe for drink?", use_column_width=True)

st.write("Displaying the head (first 5 rows) of the dataset :")
st.write(df.head())  # Display the DataFrame

st.write("Displaying the statistics of the dataset :")  # Display the DataFrame
st.write(df.describe())

# Select only numeric column 
df_new = df.select_dtypes(include=['int64', 'float64'])
num_columns = len(df_new)

# Define the layout of subplots
n_rows = math.ceil(df_new.shape[1]/5)
n_cols = 5

# Corr Heat Map
hide_corr = st.checkbox("Hide Correlation Heat Map")
if not hide_corr:
    plt.figure(figsize=(10, 10))
    sns.heatmap(df_new.corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    heatmap_fig = plt.gcf()  # Get the current figure
    st.pyplot(heatmap_fig)

attribute1="Solids"
attribute2="Sulfate"
plot = sns.jointplot(data=df_new, x=attribute1, y=attribute2, hue="Potability")
# Display the plot in Streamlit
st.pyplot(plot)


# Regression plot
st.subheader("Regression Plot")
plt.figure(figsize=(10, 6))
x_column = st.selectbox('Select x column for plotting', df_new.columns, index=df_new.columns.get_loc('Solids'))
y_column = st.selectbox('Select y column for plotting', df_new.columns, index=df_new.columns.get_loc('Sulfate'))
plt.title(f'Regplot of {x_column} vs {y_column} with Lowess Smoother')
fig = sns.regplot(data=df_new, x=x_column, y=y_column, lowess=True, scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})
reg_fig = plt.gcf()  # Get the current figure
st.pyplot(reg_fig)

# KDE PLOT
hide_KDE = st.checkbox("Hide KDE Plot")
if not hide_KDE:
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 8))
    axes = axes.flatten()
    for i, column in enumerate(df_new):
        ax = axes[i]
        df[column].plot.kde(ax=ax)
        ax.set_title(f'KDE Plot for {column}')
    for i in range(num_columns, n_rows * n_cols):
        fig.delaxes(axes[i])
    plt.tight_layout()
    st.pyplot(fig)
