import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Page config
st.set_page_config(
    page_title="Flavors Kitchen - Business Intelligence",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database connection
@st.cache_resource
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'whatsapp_bot'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'taha123')
    )

# Fetch data
@st.cache_data(ttl=60)  # Cache for 1 minute
def fetch_orders():
    conn = get_db_connection()
    query = """
        SELECT 
            order_id,
            customer_phone,
            order_text,
            order_amount,
            created_at
        FROM orders
        ORDER BY created_at DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Sidebar navigation
st.sidebar.title("🍽️ Flavors Kitchen")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Customer Portal", "📊 Business Dashboard", "ℹ️ About"]
)

#############################################
# PAGE 1: CUSTOMER PORTAL
#############################################

if page == "🏠 Customer Portal":
    st.title("🍽️ Welcome to Flavors Kitchen!")
    st.markdown("### Your friendly neighbourhood place for delicious meals")
    
    # Big WhatsApp button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("---")
        st.markdown("### 📱 Order Now on WhatsApp")
        
        # WhatsApp link (replace with your actual Twilio number)
        whatsapp_url = "https://wa.me/14155238886?text=Hello%2C%20I%20want%20to%20order"
        
        st.markdown(f"""
        <a href="{whatsapp_url}" target="_blank">
            <button style="
                background-color: #25D366;
                color: white;
                padding: 20px 40px;
                font-size: 24px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                width: 100%;
                font-weight: bold;
            ">
            🟢 Chat with us on WhatsApp
            </button>
        </a>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Menu display
    st.markdown("## 📋 Our Menu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🍟 Snacks")
        st.markdown("""
        - Momos (Veg/Chicken) - ₹60/80
        - Samosa - ₹20
        - Paneer Roll - ₹70
        - Veg Sandwich - ₹50
        - French Fries - ₹60
        """)
        
        st.markdown("### 🍽️ Meals")
        st.markdown("""
        - Veg Thali - ₹120
        - Chicken Thali - ₹150
        - Dal Rice - ₹80
        - Biryani - ₹140
        """)
    
    with col2:
        st.markdown("### 🥗 Diet Food")
        st.markdown("""
        - Oats Bowl - ₹70
        - Sprouts Salad - ₹60
        - Protein Bowl - ₹90
        - Low-Cal Meal - ₹100
        """)
        
        st.markdown("### ☕ Beverages")
        st.markdown("""
        - Chai - ₹20
        - Coffee - ₹30
        - Lassi - ₹40
        - Fresh Juice - ₹50
        """)
    
    st.markdown("---")
    st.markdown("### 🎉 Catering Services Available")
    st.info("📞 For bulk orders and parties, contact us on WhatsApp!")

#############################################
# PAGE 2: BUSINESS DASHBOARD
#############################################

elif page == "📊 Business Dashboard":
    # Simple password protection
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.title("🔐 Owner Login")
        password = st.text_input("Enter password:", type="password")
        if st.button("Login"):
            if password == "flavors2024":  # Change this password
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password")
    else:
        st.title("📊 Flavors Kitchen - Business Dashboard")
        st.markdown("### Real-time Analytics & Insights")
        
        # Fetch data
        try:
            df = fetch_orders()
            
            if df.empty:
                st.warning("No orders yet! Share your WhatsApp link with customers.")
            else:
                # Add refresh button
                col1, col2 = st.columns([6, 1])
                with col2:
                    if st.button("🔄 Refresh"):
                        st.cache_data.clear()
                        st.rerun()
                
                # KEY METRICS ROW
                st.markdown("### 📈 Key Metrics")
                col1, col2, col3, col4 = st.columns(4)
                
                total_orders = len(df)
                total_revenue = df['order_amount'].sum() if 'order_amount' in df.columns else 0
                unique_customers = df['customer_phone'].nunique()
                avg_order = total_revenue / total_orders if total_orders > 0 else 0
                
                col1.metric("📦 Total Orders", total_orders)
                col2.metric("💰 Revenue", f"₹{total_revenue:,.0f}")
                col3.metric("👥 Customers", unique_customers)
                col4.metric("⭐ Avg Order", f"₹{avg_order:.0f}")
                
                st.markdown("---")
                
                # REVENUE TREND
                st.markdown("### 📈 Revenue Trend (Last 7 Days)")
                df['date'] = pd.to_datetime(df['created_at']).dt.date
                daily_revenue = df.groupby('date')['order_amount'].sum().reset_index()
                
                fig = px.line(
                    daily_revenue, 
                    x='date', 
                    y='order_amount',
                    markers=True,
                    title="Daily Revenue"
                )
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Revenue (₹)",
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # TWO COLUMN LAYOUT
                col1, col2 = st.columns(2)
                
                with col1:
                    # TOP ITEMS (if you're parsing items from order_text)
                    st.markdown("### 🏆 Popular Orders")
                    # For now, showing top order texts
                    top_orders = df['order_text'].value_counts().head(5)
                    
                    fig = px.bar(
                        x=top_orders.values,
                        y=top_orders.index,
                        orientation='h',
                        title="Top 5 Orders"
                    )
                    fig.update_layout(
                        xaxis_title="Count",
                        yaxis_title="Order",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # HOURLY DISTRIBUTION
                    st.markdown("### ⏰ Peak Hours")
                    df['hour'] = pd.to_datetime(df['created_at']).dt.hour
                    hourly = df.groupby('hour').size().reset_index(name='orders')
                    
                    fig = px.bar(
                        hourly,
                        x='hour',
                        y='orders',
                        title="Orders by Hour"
                    )
                    fig.update_layout(
                        xaxis_title="Hour of Day",
                        yaxis_title="Number of Orders"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                
                # CUSTOMER INSIGHTS
                st.markdown("### 👥 Customer Insights")
                col1, col2, col3 = st.columns(3)
                
                customer_orders = df.groupby('customer_phone').size()
                new_customers = (customer_orders == 1).sum()
                returning_customers = (customer_orders > 1).sum()
                most_orders = customer_orders.max()
                
                col1.metric("🆕 New Customers", new_customers)
                col2.metric("🔄 Returning", returning_customers)
                col3.metric("🏆 Most Orders", f"{most_orders} orders")
                
                st.markdown("---")
                
                # RECENT ORDERS TABLE
                st.markdown("### 📋 Recent Orders")
                recent = df.head(10).copy()
                recent['created_at'] = pd.to_datetime(recent['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                recent['customer_phone'] = recent['customer_phone'].apply(lambda x: f"XXX-{str(x)[-4:]}")
                
                st.dataframe(
                    recent[['created_at', 'customer_phone', 'order_text', 'order_amount']],
                    column_config={
                        "created_at": "Time",
                        "customer_phone": "Customer",
                        "order_text": "Order",
                        "order_amount": st.column_config.NumberColumn("Amount", format="₹%.0f")
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.info("Make sure your database is set up and contains an 'orders' table.")

#############################################
# PAGE 3: ABOUT
#############################################

elif page == "ℹ️ About":
    st.title("ℹ️ About This System")
    
    st.markdown("""
    ## 🤖 WhatsApp Business Intelligence Bot
    
    ### What is this?
    An AI-powered system that helps small restaurants:
    - ✅ Take orders via WhatsApp automatically
    - ✅ Track all orders in a database
    - ✅ Generate real-time business analytics
    - ✅ Understand customer behavior
    
    ### Tech Stack
    - **Frontend**: Streamlit
    - **Backend**: Python + Flask
    - **Database**: PostgreSQL
    - **Messaging**: Twilio WhatsApp API
    - **Analytics**: Plotly, Pandas
    
    ### Features
    - 📱 Easy ordering via WhatsApp
    - 📊 Real-time analytics dashboard
    - 💰 Revenue tracking
    - 👥 Customer insights
    - ⏰ Peak hours analysis
    
    ### Built by
    **Taha Anik** - BCA Student, MSU Baroda
    
    📧 tahaanik729@gmail.com  
    🔗 [GitHub](https://github.com/anikhere)  
    💼 [LinkedIn](https://linkedin.com/in/taha-anik-56ba7531b)
    
    ---
    
    ### Why I Built This
    Small restaurants use WhatsApp for orders but have no way to track:
    - Which items sell best
    - When they're busiest
    - Who their repeat customers are
    - How much revenue they're making
    
    This system solves that problem with zero learning curve for customers 
    (they just use WhatsApp like normal) and gives owners powerful insights.
    
    ### Impact
    - Currently used by Flavors Kitchen in Godhra, Gujarat
    - Processing 20+ orders daily
    - Helping owner make data-driven decisions
    """)
    
    st.success("⭐ This is a portfolio project demonstrating real-world ML/AI application")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ by [Taha Anik](https://github.com/anikhere)")