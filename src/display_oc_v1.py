import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import get_market_direction_data, get_spot_price, get_strike_prices
import time

# Set up page config
st.set_page_config(
    page_title='Option Chain Analytics Dashboard',
    page_icon='✅',
    layout='wide'
)

st.title("Real-Time / Option Chain Analytics")

# Get strike prices and spot price
sp_list = get_strike_prices()
spot_df = get_spot_price()
spot_strike_price = int((spot_df['price'].iloc[-1] + 50) / 100) * 100
idx = sp_list.index(spot_strike_price)
sp_list_new = sp_list[idx-8:idx+8]

# UI Elements
strike_price = st.select_slider("Strike_price", options=sp_list_new, value=spot_strike_price)
chart_placeholder = st.empty()  # Create a placeholder for the chart

# Main loop
while True:
    with chart_placeholder.container():
        # Get data
        direction_df = get_market_direction_data(strike_price, strike_price)
        spot_df = get_spot_price()
        
        # Create figure with unique key
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(
                x=spot_df['time'],
                y=spot_df['price'],
                mode='lines',
                name='Spot price'
            ),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(
                x=spot_df['time'],
                y=direction_df,
                mode='lines',
                name='direction: put-call'
            ),
            secondary_y=True
        )
        
        # Display chart with unique key
        st.plotly_chart(fig, use_container_width=True, key=f"option_chart_{time.time()}")
    
    time.sleep(3)
