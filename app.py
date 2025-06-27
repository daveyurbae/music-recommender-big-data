import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Music Recommender System",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-running {
        color: #28a745;
        font-weight: bold;
    }
    .status-stopped {
        color: #dc3545;
        font-weight: bold;
    }
    .status-training {
        color: #ffc107;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'kafka_status' not in st.session_state:
    st.session_state.kafka_status = 'Running'
if 'spark_status' not in st.session_state:
    st.session_state.spark_status = 'Running'
if 'model_status' not in st.session_state:
    st.session_state.model_status = 'Ready'
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x100/1f77b4/ffffff?text=LOGO", width=150)
    st.title("🎵 Music Recommender")
    
    # Navigation
    page = st.selectbox(
        "Navigate to:",
        ["Dashboard", "Recommendations", "Data Management", "Model Training", "System Monitoring"]
    )
    
    st.markdown("---")
    
    # System Status
    st.subheader("System Status")
    
    # Kafka Status
    kafka_color = "🟢" if st.session_state.kafka_status == "Running" else "🔴"
    st.markdown(f"{kafka_color} **Kafka**: {st.session_state.kafka_status}")
    
    # Spark Status
    spark_color = "🟢" if st.session_state.spark_status == "Running" else "🔴"
    st.markdown(f"{spark_color} **Spark**: {st.session_state.spark_status}")
    
    # Model Status
    model_color = "🟢" if st.session_state.model_status == "Ready" else "🟡"
    st.markdown(f"{model_color} **Model**: {st.session_state.model_status}")

# Main content
if page == "Dashboard":
    st.markdown("<h1 class='main-header'>🎵 Music Recommendation System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #666;'>Kafka + Spark + MinIO Integration</p>", unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Songs",
            value="125,340",
            delta="1,234 new"
        )
    
    with col2:
        st.metric(
            label="Active Users",
            value="8,721",
            delta="156 online"
        )
    
    with col3:
        st.metric(
            label="Recommendations Today",
            value="45,123",
            delta="12.5%"
        )
    
    with col4:
        st.metric(
            label="Model Accuracy",
            value="92.3%",
            delta="1.2%"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Usage Analytics")
        
        # Generate sample data
        dates = pd.date_range(start='2024-01-01', end='2024-01-30', freq='D')
        usage_data = pd.DataFrame({
            'Date': dates,
            'Recommendations': np.random.randint(1000, 5000, len(dates)),
            'Active Users': np.random.randint(500, 2000, len(dates))
        })
        
        fig = px.line(usage_data, x='Date', y=['Recommendations', 'Active Users'],
                     title="Daily System Usage")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎭 Genre Distribution")
        
        # Sample genre data
        genres = ['Pop', 'Rock', 'Jazz', 'Classical', 'Electronic', 'Hip-Hop', 'Country', 'R&B']
        counts = np.random.randint(5000, 25000, len(genres))
        
        fig = px.pie(values=counts, names=genres, title="Music Genre Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    # Real-time data stream simulation
    st.subheader("🔄 Real-time Data Stream")
    
    # Create placeholder for real-time updates
    placeholder = st.empty()
    
    # Sample streaming data
    streaming_data = pd.DataFrame({
        'Timestamp': [datetime.now() - timedelta(minutes=i) for i in range(10, 0, -1)],
        'Messages/sec': np.random.randint(100, 1000, 10),
        'Errors': np.random.randint(0, 5, 10)
    })
    
    fig = px.line(streaming_data, x='Timestamp', y='Messages/sec', 
                 title="Kafka Message Throughput")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Recommendations":
    st.header("🎯 Music Recommendations")
    
    # User input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Get Personalized Recommendations")
        
        # User preferences
        user_id = st.text_input("User ID", placeholder="Enter user ID or leave empty for demo")
        
        col1a, col1b = st.columns(2)
        with col1a:
            preferred_genres = st.multiselect(
                "Preferred Genres",
                ['Pop', 'Rock', 'Jazz', 'Classical', 'Electronic', 'Hip-Hop', 'Country', 'R&B'],
                default=['Pop', 'Rock']
            )
        
        with col1b:
            mood = st.selectbox(
                "Current Mood",
                ['Happy', 'Sad', 'Energetic', 'Relaxed', 'Romantic', 'Party']
            )
        
        num_recommendations = st.slider("Number of Recommendations", 5, 50, 10)
        
        if st.button("🎵 Get Recommendations", type="primary"):
            with st.spinner("Generating recommendations..."):
                # Simulate API call delay
                time.sleep(2)
                
                # Generate mock recommendations
                artists = ['Taylor Swift', 'Ed Sheeran', 'Adele', 'Bruno Mars', 'Billie Eilish', 
                          'The Weeknd', 'Ariana Grande', 'Drake', 'Dua Lipa', 'Post Malone']
                songs = ['Song A', 'Song B', 'Song C', 'Song D', 'Song E', 
                        'Song F', 'Song G', 'Song H', 'Song I', 'Song J']
                
                recommendations = []
                for i in range(num_recommendations):
                    recommendations.append({
                        'Rank': i + 1,
                        'Song': np.random.choice(songs) + f' {i+1}',
                        'Artist': np.random.choice(artists),
                        'Genre': np.random.choice(preferred_genres if preferred_genres else ['Pop']),
                        'Confidence': round(np.random.uniform(0.7, 0.99), 3),
                        'Duration': f"{np.random.randint(2, 5)}:{np.random.randint(10, 59):02d}"
                    })
                
                st.session_state.recommendations = recommendations
                st.success(f"Generated {num_recommendations} recommendations!")
    
    with col2:
        st.subheader("Recommendation Stats")
        st.info("🎯 **Collaborative Filtering**\nUsing user behavior patterns")
        st.info("🧠 **Content-Based**\nUsing song features")
        st.info("🔄 **Real-time Learning**\nUpdating with new data")
    
    # Display recommendations
    if st.session_state.recommendations:
        st.subheader("🎵 Your Recommendations")
        
        # Convert to DataFrame for better display
        df_recommendations = pd.DataFrame(st.session_state.recommendations)
        
        # Display as interactive table
        st.dataframe(
            df_recommendations,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Confidence": st.column_config.ProgressColumn(
                    "Confidence Score",
                    help="Model confidence in recommendation",
                    min_value=0,
                    max_value=1,
                ),
                "Rank": st.column_config.NumberColumn(
                    "Rank",
                    help="Recommendation ranking",
                    min_value=1,
                    max_value=50,
                )
            }
        )
        
        # Export options
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Export to CSV"):
                csv = df_recommendations.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("🔄 Refresh Recommendations"):
                st.rerun()
        
        with col3:
            if st.button("👍 Save Playlist"):
                st.success("Playlist saved successfully!")

elif page == "Data Management":
    st.header("📊 Data Management")
    
    tab1, tab2, tab3 = st.tabs(["Upload Data", "Dataset Overview", "MinIO Storage"])
    
    with tab1:
        st.subheader("📤 Upload New Dataset")
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload music dataset with columns: user_id, song_id, rating, genre, etc."
        )
        
        if uploaded_file is not None:
            # Read and display sample data
            df = pd.read_csv(uploaded_file)
            st.success(f"File uploaded: {uploaded_file.name}")
            st.write(f"Shape: {df.shape}")
            
            st.subheader("Data Preview")
            st.dataframe(df.head(10))
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🚀 Process Data"):
                    with st.spinner("Processing data..."):
                        time.sleep(3)
                        st.success("Data processed and sent to Kafka!")
            
            with col2:
                if st.button("💾 Save to MinIO"):
                    with st.spinner("Saving to MinIO..."):
                        time.sleep(2)
                        st.success("Data saved to MinIO storage!")
    
    with tab2:
        st.subheader("📈 Dataset Overview")
        
        # Mock dataset statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Records", "2,847,392")
            st.metric("Unique Users", "125,847")
        
        with col2:
            st.metric("Unique Songs", "89,234")
            st.metric("Unique Artists", "12,456")
        
        with col3:
            st.metric("Genres", "15")
            st.metric("Avg Rating", "4.2")
        
        # Data quality metrics
        st.subheader("Data Quality")
        quality_data = pd.DataFrame({
            'Metric': ['Completeness', 'Accuracy', 'Consistency', 'Timeliness'],
            'Score': [95.2, 88.7, 92.1, 87.3]
        })
        
        fig = px.bar(quality_data, x='Metric', y='Score', 
                    title="Data Quality Metrics",
                    color='Score', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("🗄️ MinIO Storage Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Storage Used", "2.4 GB", "12% increase")
            st.metric("Total Files", "1,247", "23 new")
        
        with col2:
            st.metric("Buckets", "5")
            st.metric("Last Backup", "2 hours ago")
        
        # Storage usage chart
        storage_data = pd.DataFrame({
            'Bucket': ['raw-data', 'processed-data', 'models', 'logs', 'backups'],
            'Size_GB': [1.2, 0.8, 0.3, 0.1, 0.2],
            'Files': [450, 320, 15, 234, 128]
        })
        
        fig = px.bar(storage_data, x='Bucket', y='Size_GB',
                    title="Storage Usage by Bucket")
        st.plotly_chart(fig, use_container_width=True)

elif page == "Model Training":
    st.header("🤖 Model Training")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Training Configuration")
        
        model_type = st.selectbox(
            "Model Type",
            ["Collaborative Filtering", "Content-Based", "Hybrid Model", "Deep Learning"]
        )
        
        col1a, col1b = st.columns(2)
        with col1a:
            batch_size = st.number_input("Batch Size", min_value=32, max_value=2048, value=512)
            learning_rate = st.number_input("Learning Rate", min_value=0.0001, max_value=0.1, value=0.01, format="%.4f")
        
        with col1b:
            epochs = st.number_input("Epochs", min_value=1, max_value=100, value=10)
            validation_split = st.slider("Validation Split", 0.1, 0.5, 0.2)
        
        st.subheader("Advanced Settings")
        use_gpu = st.checkbox("Use GPU Acceleration", value=True)
        early_stopping = st.checkbox("Enable Early Stopping", value=True)
        
        if st.button("🚀 Start Training", type="primary"):
            st.session_state.model_status = "Training"
            
            # Training progress simulation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                status_text.text(f'Training Progress: {i+1}%')
                time.sleep(0.05)
            
            st.success("Model training completed!")
            st.session_state.model_status = "Ready"
    
    with col2:
        st.subheader("Training History")
        
        # Mock training history
        history_data = pd.DataFrame({
            'Epoch': list(range(1, 11)),
            'Loss': np.random.exponential(0.5, 10)[::-1] + 0.1,
            'Accuracy': np.random.uniform(0.7, 0.95, 10)
        })
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=history_data['Epoch'], y=history_data['Loss'], name="Loss"),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=history_data['Epoch'], y=history_data['Accuracy'], name="Accuracy"),
            secondary_y=True,
        )
        
        fig.update_layout(title_text="Training Progress")
        fig.update_xaxes(title_text="Epoch")
        fig.update_yaxes(title_text="Loss", secondary_y=False)
        fig.update_yaxes(title_text="Accuracy", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Model Performance")
        st.metric("Current Accuracy", "92.3%", "2.1%")
        st.metric("F1 Score", "0.89", "0.03")
        st.metric("Training Time", "45 min", "-5 min")

elif page == "System Monitoring":
    st.header("🔍 System Monitoring")
    
    # Real-time metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Kafka Metrics")
        st.metric("Messages/sec", "1,234", "56")
        st.metric("Consumer Lag", "12ms", "-2ms")
        
    with col2:
        st.subheader("Spark Metrics")
        st.metric("CPU Usage", "68%", "5%")
        st.metric("Memory Usage", "4.2GB", "0.3GB")
        
    with col3:
        st.subheader("System Health")
        st.metric("Uptime", "99.8%")
        st.metric("Error Rate", "0.02%", "-0.01%")
    
    # System logs
    st.subheader("📋 Recent Logs")
    
    logs = [
        {"timestamp": "2024-01-15 10:30:25", "level": "INFO", "service": "Kafka", "message": "New message batch processed"},
        {"timestamp": "2024-01-15 10:30:20", "level": "INFO", "service": "Spark", "message": "Model training completed"},
        {"timestamp": "2024-01-15 10:30:15", "level": "WARN", "service": "MinIO", "message": "Storage usage above 80%"},
        {"timestamp": "2024-01-15 10:30:10", "level": "INFO", "service": "API", "message": "Recommendation request processed"}
    ]
    
    for log in logs:
        level_color = {"INFO": "🟢", "WARN": "🟡", "ERROR": "🔴"}.get(log["level"], "⚪")
        st.text(f"{level_color} {log['timestamp']} [{log['service']}] {log['message']}")
    
    # Performance charts
    st.subheader("📊 Performance Metrics")
    
    # Generate sample performance data
    timestamps = pd.date_range(start=datetime.now()-timedelta(hours=1), 
                              end=datetime.now(), freq='1min')
    perf_data = pd.DataFrame({
        'Timestamp': timestamps,
        'CPU_Usage': np.random.uniform(50, 90, len(timestamps)),
        'Memory_Usage': np.random.uniform(40, 80, len(timestamps)),
        'Network_IO': np.random.uniform(10, 50, len(timestamps))
    })
    
    fig = px.line(perf_data, x='Timestamp', 
                 y=['CPU_Usage', 'Memory_Usage', 'Network_IO'],
                 title="System Performance (Last Hour)")
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>Music Recommender System v1.0 | "
    "Built with Streamlit, Kafka, Spark & MinIO</p>",
    unsafe_allow_html=True
)