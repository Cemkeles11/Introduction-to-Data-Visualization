# CEN445 Introduction to Data Visualization Assignment: Global Air Pollution Dashboard

This project is developed within the scope of the CEN445 Introduction to Data Visualization course. It presents an interactive dashboard analyzing and visualizing global air pollution data using Python, Streamlit, Plotly, and Altair libraries.

**🔴 Live Dashboard:** [Click Here to View the App](https://introduction-to-data-visualization-evm8azwzrxmbsw3tcpcayy.streamlit.app/)

## 📊 Key Visualization Techniques

To extract meaningful insights from the dataset, this dashboard utilizes a variety of advanced and basic visualization methods as requested in the assignment:

* **Choropleth Map (Advanced):** Displays the geographical distribution of pollution intensity across countries.
* **Sankey Diagram (Advanced):** Illustrates the flow of data from the top 10 most-observed countries to their corresponding AQI categories (Good, Moderate, Unhealthy, etc.).
* **Treemap (Advanced):** Visualizes the hierarchical share of pollution levels of cities within a selected country.
* **Parallel Coordinates (Advanced):** Compares multiple pollutant metrics (PM2.5, Ozone, NO2, etc.) simultaneously for selected cities or countries.
* **Grouped Bar Chart (Advanced):** Provides a side-by-side comparison of pollutant values for selected locations.
* **Heatmap (Advanced):** Shows the correlation matrix between different types of pollutants to identify relationships.
* **Box Plot (Advanced):** Analyzes the distribution of pollutant values within each AQI category.
* **Basic Charts:** Pie Chart (Category Distribution), Bar Chart (Top 10 Cities), and Histogram (AQI Value Frequency).

All visualizations feature interactivity such as tooltips, zooming, panning, and filtering.

## 🌍 Dataset

We used the **Global Air Pollution Data** sourced from Kaggle. The dataset includes observations from over 170 countries, containing both categorical data (e.g., `AQI Category`, `Country`) and numerical data (e.g., `AQI Value`, `PM2.5 AQI Value`, `Ozone AQI Value`), meeting the course requirements.

## 🚀 Installation and Execution (Local)

To run this dashboard on your local machine:

1.  Clone this repository:
    ```bash
    git clone [https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git)
    cd YOUR_REPO_NAME
    ```

2.  Install the required libraries:
    ```bash
    pip install streamlit pandas plotly seaborn matplotlib altair
    ```

3.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

## 👥 Team Members & Contributions

This project was **collaboratively developed** by the team members listed below. We adopted a pair programming approach and worked jointly on all phases of the project to ensure a comprehensive understanding of the entire codebase.

**Team Members:**
1.  **Cem Keleş** (ID: 2020556037)
2.  **Eray Doğan** (ID: 2020556021)

**Joint Contributions:**
Both members contributed equally to the following tasks:
* **Data Preparation:** Selection, cleaning, and preprocessing of the Kaggle dataset.
* **Dashboard Architecture:** Designing the layout, implementing the Streamlit sidebar filters, and handling data flow.
* **Visualization Implementation:** Coding both basic and advanced charts (Map, Sankey, Parallel Coordinates, Treemap, etc.) using Plotly and Altair.
* **Machine Learning & Analysis:** Implementing the comparative analysis modules.
* **Documentation:** Preparing this README file and the final project report.
