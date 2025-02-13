import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from prediction_helper import predict

# Configure the page with a dark theme and custom settings
st.set_page_config(
    page_title="🏦 Lekhraj Finance: Credit Risk Modelling",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and better styling
st.markdown("""
    <style>
    /* Main page background */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }

    /* Metrics styling */
    .stMetric {
        background-color: #1e2530;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2d3745;
    }

    /* Button styling */
    .stButton>button {
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0052a3;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }

    /* Input fields styling */
    .stNumberInput div input, .stSelectbox div div {
        background-color: #1e2530;
        color: white;
        border: 1px solid #2d3745;
        border-radius: 5px;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e2530;
        padding: 10px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #2d3745;
        border-radius: 5px;
        color: white;
        padding: 8px 16px;
    }

    /* Card container styling */
    .card-container {
        background-color: #1e2530;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2d3745;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Create tabs with icons
tab1, tab2, tab3 = st.tabs([
    "🧮 Risk Calculator",
    "📊 Analytics Dashboard",
    "📚 Documentation"
])

with tab1:
    # Header with animation
    st.markdown("""
        <h1 style='text-align: center; color: #0066cc; animation: fadeIn 1s;'>
            🏦 Lekhraj Finance: Credit Risk Modelling
        </h1>
    """, unsafe_allow_html=True)

    with st.container():
        # Create form sections with better organization
        st.markdown("<div class='card-container'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        # Personal Information Section
        with col1:
            st.markdown("### 👤 Personal Info")
            age = st.number_input('Age', min_value=18, max_value=100, value=28)
            income = st.number_input('Income (₹)', min_value=0, value=1200000,
                                     format="%d", help="Annual income in rupees")

        with col2:
            st.markdown("### 💰 Loan Details")
            loan_amount = st.number_input('Loan Amount (₹)', min_value=0, value=2560000,
                                          format="%d")
            loan_tenure_months = st.number_input('Loan Tenure (months)',
                                                 min_value=0, step=1, value=36)

        with col3:
            st.markdown("### 📈 Credit Metrics")
            credit_utilization_ratio = st.number_input('Credit Utilization (%)',
                                                       min_value=0, max_value=100, value=30)
            delinquency_ratio = st.number_input('Delinquency Ratio (%)',
                                                min_value=0, max_value=100, value=30)
        st.markdown("</div>", unsafe_allow_html=True)

        # Additional Metrics Section
        st.markdown("<div class='card-container'>", unsafe_allow_html=True)
        col4, col5, col6 = st.columns(3)

        with col4:
            st.markdown("### 🏠 Property Info")
            residence_type = st.selectbox('Residence Type',
                                          ['Owned', 'Rented', 'Mortgage'],
                                          help="Current residence ownership status")

        with col5:
            st.markdown("### 🎯 Purpose")
            loan_purpose = st.selectbox('Loan Purpose',
                                        ['Education', 'Home', 'Auto', 'Personal'])

        with col6:
            st.markdown("### 🔒 Security")
            loan_type = st.selectbox('Loan Type',
                                     ['Secured', 'Unsecured'])
        st.markdown("</div>", unsafe_allow_html=True)

        # Calculate Risk Section
        if st.button('Calculate Risk 🎯', use_container_width=True):
            with st.spinner('Calculating risk profile...'):
                # Get prediction
                probability, credit_score, rating = predict(
                    age, income, loan_amount, loan_tenure_months, 20,
                    delinquency_ratio, credit_utilization_ratio, 2,
                    residence_type, loan_purpose, loan_type
                )

                # Display results in cards
                st.markdown("<div class='card-container'>", unsafe_allow_html=True)
                metric1, metric2, metric3 = st.columns(3)

                with metric1:
                    st.metric("Default Probability", f"{probability:.2%}",
                              delta="Low Risk" if probability < 0.3 else "High Risk")
                with metric2:
                    st.metric("Credit Score", f"{credit_score}",
                              delta="Good" if credit_score > 700 else "Needs Improvement")
                with metric3:
                    st.metric("Rating", rating)
                st.markdown("</div>", unsafe_allow_html=True)

                # Enhanced gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=credit_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Credit Score Analysis", 'font': {'color': "white"}},
                    delta={'reference': 750},
                    gauge={
                        'axis': {'range': [300, 900], 'tickcolor': "white"},
                        'bar': {'color': "#0066cc"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [300, 580], 'color': "#ff4444"},
                            {'range': [580, 670], 'color': "#ffbb33"},
                            {'range': [670, 900], 'color': "#00C851"}
                        ]
                    }
                ))

                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': "white"}
                )

                st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.title("📊 Analytics Dashboard")
    # Sample data for demonstration
    st.subheader("Risk Distribution")
    sample_data = pd.DataFrame({
        'Credit Score Range': ['300-580', '581-670', '671-900'],
        'Count': [25, 45, 30]
    })

    fig = go.Figure(data=[go.Pie(labels=sample_data['Credit Score Range'],
                                 values=sample_data['Count'],
                                 hole=.3)])
    st.plotly_chart(fig, use_container_width=True)

    # Add more visualizations as needed
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Loan Amount vs Credit Score")
        fig = go.Figure(data=go.Scatter(
            x=np.random.normal(700, 100, 100),
            y=np.random.normal(2000000, 500000, 100),
            mode='markers'
        ))
        fig.update_layout(xaxis_title="Credit Score", yaxis_title="Loan Amount")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Age Distribution")
        fig = go.Figure(data=go.Histogram(
            x=np.random.normal(35, 10, 1000),
            nbinsx=20
        ))
        fig.update_layout(xaxis_title="Age", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.title("📚 Documentation")
    st.write("""
       ### How to Use This Tool

       1. **Input Information**: Fill in all required fields in the Risk Calculator tab
       2. **Calculate Risk**: Click the 'Calculate Risk' button to get your results
       3. **Interpret Results**: 
           - Default Probability: Likelihood of loan default
           - Credit Score: Score between 300-900
           - Rating: Overall credit rating

       ### Metrics Explanation

       - **DPD (Days Past Due)**: Number of days payment is overdue
       - **Delinquency Ratio**: Percentage of times payments were late
       - **Credit Utilization**: Percentage of available credit being used

       ### Contact Support:

       For technical support or questions about your assessment, please contact:
       - Email: lekhrajyadav8190@gmail.com
       - Phone: 9928815089
       """)
