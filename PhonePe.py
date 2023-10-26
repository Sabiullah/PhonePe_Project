# pip install streamlit_option_menu
# pip install mysql-connector-python

import mysql.connector
import pandas as pd

# Import any other libraries you need

import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
import requests

# Establish a connection to the database
# Replace with your actual database credentials
db_config = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "database": "phonepe_pulse"
}

# Establish the database connection
conn = mysql.connector.connect(**db_config)

# Create a cursor object
cursor = conn.cursor()

#with st.sidebar:
SELECT = option_menu(
    menu_title = None,
    options = ["About","Home","Basic insights","Contact"],
    icons =["bar-chart","house","toggles","at"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white","size":"auto", "width": "100%"},
        "icon": {"color": "black", "font-size": "15px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}})

#---------------------Basic Insights -----------------#

if SELECT == "Basic insights":
    st.title("BASIC INSIGHTS")
    st.write("----")
    st.subheader("Let's know some basic insights about the data")
    options = ["--select--",
               "1. Top 10 states based on year and amount of transaction",
               "2. List 10 states based on Transation type and Number of transaction",
               "3. Top 5 Transaction_Type based on Transaction_Amount",
               "4. Top 10 Registered-users based on States and District",
               "5. Top 10 Districts based on states and Count of transaction",
               "6. List 10 Districts based on states and amount of transaction",
               "7. List 10 Transaction_Count based on Districts and states",
               "8. Top 10 RegisteredUsers based on states and District",
               "9. Year wise Transaction Amount in Crores",
               "10. Year wise Transaction Count",
               "11. Year wise Quaterly Analysis based on Transaction Amount",
               "12. Year wise Quarterly wise Transaction Count"]

    # 1

    select = st.selectbox("Select the option", options)
    if select == "1. Top 10 states based on year and amount of transaction":

        cursor.execute(
            "SELECT CONCAT(States, ' - ', Transaction_Year) AS State_Year, States, Transaction_Year, round(SUM(Transaction_Amount)/10000000) AS Total_Transaction_Amount_Crores FROM top_tran GROUP BY States, Transaction_Year ORDER BY Total_Transaction_Amount_Crores DESC LIMIT 10");

        df = pd.DataFrame(cursor.fetchall(),
                          columns=['State_Year', 'States', 'Transaction_Year', 'Total_Transaction_Amount_Crores'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            # st.markdown(
            #     "<style>.css-9hvz0z-Subheader{font-size: 15px !important;}</style>", unsafe_allow_html=True
            # )
            st.subheader("Top 10 states and amount of transaction")
            st.line_chart(data=df, y="Total_Transaction_Amount_Crores", x="State_Year")


            # 2

    elif select == "2. List 10 states based on Transation type and Number of transaction":
        cursor.execute(
            "SELECT  States,  SUM(Transaction_Count) as Total FROM top_tran GROUP BY States ORDER BY Total ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Total'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            # st.title("List 10 states based on type and Number of transaction")
            # st.bar_chart(data=df, y="States", x="Total")
            # fig = px.treemap(df, path=['States'], values='Total')
            fig = px.box(df, x='States', y='Total', title="List 10 states based on type and Number of transaction")
            st.plotly_chart(fig)

            # 3

    elif select == "3. Top 5 Transaction_Type based on Transaction_Amount":
        cursor.execute(
            "SELECT DISTINCT Transaction_Type, round(SUM(Transaction_Amount)/10000000) AS Amount FROM agg_user GROUP BY Transaction_Type ORDER BY Amount DESC LIMIT 5");
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_Type', 'Amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Top 5 Transaction_Type based on Transaction_Amount in Cr")
            # st.bar_chart(data=df, x="Transaction_Type", y="Amount")
            fig = px.line(df, x='Transaction_Type', y='Amount')
            st.plotly_chart(fig)

            # st.subheader("Top 5 Transaction_Type based on Transaction_Amount")
            st.bar_chart(data=df, x="Transaction_Type", y="Amount")
            # fig = px.line(df, x='Transaction_Type', y='Amount')
            # st.plotly_chart(fig)

            # 4

    elif select == "4. Top 10 Registered-users based on States and District":
        cursor.execute(
            "SELECT DISTINCT States, District, SUM(RegisteredUsers) AS Users FROM top_user GROUP BY States, District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'District', 'Users'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Top 10 Registered-users based on States and District")
            st.bar_chart(data=df, x="District", y="Users")

            # 5

    elif select == "5. Top 10 Districts based on states and Count of transaction":
        cursor.execute(
            "SELECT States,District,SUM(Transaction_Count) AS Counts FROM map_tran GROUP BY States,District ORDER BY Counts DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'District', 'Counts'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            # st.title("Top 10 Districts based on states and Count of transaction")
            # st.bar_chart(data=df, x="District", y="Counts")
            # fig = px.treemap(df, path=['States', 'District'], values='Counts')
            # st.plotly_chart(fig)
            fig = px.violin(df, x='District', y='Counts', box=True, title="Top 10 Districts based on states and Count of transaction")
            st.plotly_chart(fig)

            # 6

    elif select == "6. List 10 Districts based on states and amount of transaction":
        cursor.execute(
            "SELECT DISTINCT States, District, Transaction_year, round(SUM(Transaction_Amount)) AS Amount FROM map_tran GROUP BY States, Transaction_year ORDER BY Amount ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'District', 'Transaction_year', 'Amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            # st.title("Least 10 Districts based on states and amount of transaction")
            # st.bar_chart(data=df, x="District", y="Amount")
            fig = px.box(df, x='States', y='Amount', color="District", title="Least 10 Districts based on states and amount of transaction")
            st.plotly_chart(fig)
            # fig = px.line_polar(df, r='Amount', theta='District', line_close=True)
            # st.plotly_chart(fig)
            # fig = px.histogram(df, x='Amount', nbins=10, title="Amount Distribution for 10 Districts")
            # st.plotly_chart(fig)

            # 7

    elif select == "7. List 10 Transaction_Count based on Districts and states":
        cursor.execute(
            "SELECT DISTINCT States, District, SUM(Transaction_Count) AS Counts FROM map_tran GROUP BY States,District ORDER BY Counts ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'District', 'Counts'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("List 10 Transaction_Count based on Districts and states")
            # st.line_chart(data=df, x="District", y="Counts")
            st.plotly_chart(px.box(df, x="District", y="Counts"))

            # 8

    elif select == "8. Top 10 RegisteredUsers based on states and District":
        cursor.execute(
            "SELECT DISTINCT States,District, SUM(RegisteredUsers) AS Users FROM map_user GROUP BY States,District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'District', 'Users'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.subheader("Top 10 RegisteredUsers based on states and District")
            # st.line_chart(data=df, x="District", y="Users")
            st.plotly_chart(px.treemap(df, path=['States', 'District'], values='Users'))

    elif select == "9. Year wise Transaction Amount in Crores":
        cursor.execute(
            "SELECT Transaction_Year AS Year, round(SUM(Transaction_Amount)/10000000) AS Amount FROM agg_user GROUP BY Year ORDER BY Year DESC");
        df = pd.DataFrame(cursor.fetchall(), columns=['Year', 'Amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            # st.title("Top 5 Transaction_Type based on Transaction_Amount")
            # st.bar_chart(data=df, x="Transaction_Type", y="Amount")
            fig = px.pie(df, names='Year', values='Amount', hole=0.4, title="Year wise Transaction Amount in Crores")
            st.plotly_chart(fig)

    elif select == "10. Year wise Transaction Count":
        cursor.execute(
            "SELECT Transaction_Year AS Year, round(SUM(Transaction_Count)) AS Count FROM agg_user GROUP BY Year ORDER BY Year DESC");
        df = pd.DataFrame(cursor.fetchall(), columns=['Year', 'Count'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            # st.title("Top 5 Transaction_Type based on Transaction_Amount")
            # st.bar_chart(data=df, x="Transaction_Type", y="Amount")
            fig = px.pie(df, names='Year', values='Count', hole=0.4, title="Year wise Transaction Count")
            st.plotly_chart(fig)
            # st.subheader("Year wise Transaction Count")
            # st.line_chart(data=df, y="Count", x="Year")

    elif select == "11. Year wise Quaterly Analysis based on Transaction Amount":
        cursor.execute(
            "SELECT CONCAT(Transaction_Year,'-',Quarters) AS YrQtr,Transaction_Year AS Year,Quarters, round(SUM(Transaction_Amount)/10000000   ) AS Amount FROM agg_user GROUP BY YrQtr ORDER BY Year DESC");
        df = pd.DataFrame(cursor.fetchall(), columns=['YrQtr','Year', 'Quarters', 'Amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            # st.title("Top 5 Transaction_Type based on Transaction_Amount")
            # st.bar_chart(data=df, x="Transaction_Type", y="Amount")
            fig = px.line(df, x='Quarters', y='Amount', color = 'Year', title="Year wise Quaterly Analysis")
            st.plotly_chart(fig)

    elif select == "12. Year wise Quarterly wise Transaction Count":
        cursor.execute(
            "SELECT CONCAT (Transaction_Year ,'-', Quarters) AS YrQtr, Transaction_Year as Year, Quarters, round(SUM(Transaction_Count)) AS Count FROM agg_user GROUP BY YrQtr ORDER BY Year DESC");
        df = pd.DataFrame(cursor.fetchall(), columns=['YrQtr','Year','Quarters', 'Count'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            # st.title("Year wise Quarterly wise Count")
            fig = px.line(df, x='Quarters', y='Count', color='Year', title="Year wise Quaterly Analysis by Count")
            st.plotly_chart(fig)






#----------------Home----------------------#

import plotly.graph_objects as go
cursor = conn.cursor()

# Execute a SELECT statement to fetch data
cursor.execute("SELECT * FROM agg_trans")
rows = cursor.fetchall()

if SELECT == "Home":
    col1, col2 = st.columns(2)
    col1.image(Image.open("C:\\Users\\safyc\\Desktop\\Python files\\Phonepe Data\\PhonePe.jpg"), width=300)
    with col1:
        st.subheader(
            "India's digital payments revolution, driven by mobile access and robust infrastructure, includes PhonePe, founded in 2015, as a key player offering data-driven insights through PhonePe Pulse.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("C:\\Users\\safyc\\Desktop\\Python files\\Phonepe Data\\PhonePe.mp4")

    df = pd.DataFrame(rows, columns=['States', 'Transaction_Year', 'Quarters', 'Transaction_Type', 'Transaction_Count',
                                     'Transaction_Amount'])
    fig = px.choropleth(df, locations="States", scope="asia", color="States", hover_name="States",
                        title="Live Geo Visualization of India")
    st.plotly_chart(fig)


#----------------About-----------------------#

if SELECT == "About":
    col1,col2 = st.columns(2)
    with col1:
        st.video("C:\\Users\\safyc\\Desktop\\Python files\\Phonepe Data\\Introducing PhonePe.mp4")
    with col2:
        st.image(Image.open("C:\\Users\\safyc\\Desktop\\Python files\\Phonepe Data\\logo.jpeg"),width = 300)
        st.write("---")
        st.subheader("The Indian digital payments story has truly captured the world's imagination."
                 " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and states-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                 " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                 "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    st.write("---")
    col1,col2 = st.columns(2)
    with col1:
        st.title("THE BEAT OF PHONEPE")
        st.write("---")
        st.subheader("Phonepe became a leading digital payments company")
        st.image(Image.open("C:\\Users\\safyc\\Desktop\\Python files\\Phonepe Data\\hp-banner-pg.jpg"),width = 800)
        with open("C:\\Users\\safyc\\Desktop\\Python files\\Phonepe Data\\PhonePe_Pulse_BCG_report.pdf","rb") as f:
            data = f.read()
        st.download_button("DOWNLOAD REPORT",data,file_name="annual report.pdf")
    with col2:
        st.image(Image.open("C:\\Users\\safyc\\Desktop\\Python files\\Phonepe Data\\PhonePe.jpg"),width = 400)

# ----------------------Contact---------------#


if SELECT == "Contact":
    name = "Sabiullah Noor Mohamed"
    mail = (f'{"Mail :"}  {"safycosting@gmail.com"}')
    description = "An Aspiring DATA-SCIENTIST..!"
    social_media = {
        "Youtube": "https://www.youtube.com/channel/UCkVIdFHE5S8f9VXrv9mQSVg",
        "GITHUB": "https://github.com/Sabiullah",
        "LINKEDIN": "https://www.linkedin.com/in/sabiullah-noor-mohamed-83507386/"
        }

    col1, col2, col3 = st.columns(3)
    col3.image(Image.open("C:\\Users\\safyc\\Desktop\\Python files\\Phonepe Data\\Safy Photo.jpg"), width=350)
    with col2:
        st.subheader('Phonepe Pulse data visualisation')
        st.write(
            "The goal of this project is to extract data from the Phonepe pulse Github repository, transform and clean the data, insert it into a MySQL database, and create a live geo visualization dashboard using Streamlit and Plotly in Python. The dashboard will display the data in an interactive and visually appealing manner, with at least 10 different dropdown options for users to select different facts and figures to display. The solution must be secure, efficient, and user-friendly, providing valuable insights and information about the data in the Phonepe pulse Github repository.")
        st.write("---")
        st.subheader(mail)
    st.write("#")
    cols = st.columns(len(social_media))
    for index, (platform, link) in enumerate(social_media.items()):
        cols[index].write(f"[{platform}]({link})")


