"""
fig.add_trace(go.Scatter(
    x=x[neg_mask], y=y[neg_mask], fill='tozeroy', fillcolor='rgba(255, 0, 0, 0.1)', line=dict(color='black', width=2), name='Loss', showlegend=False)
) """

import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as stc
#st.set_page_config(layout="wide")

def PL_colorfill(x, y):
    # create a mask for positive and negative values
    pos_mask = y >= 0
    neg_mask = y < 0

    # create a trace for positive and negative values
    fig.add_trace(go.Scatter(
        x=x[pos_mask], y=y[pos_mask], fill='tozeroy', fillcolor='rgba(26,150,65,0.5)', line=dict(color='black', width=2), name='Profit', showlegend=False)
    )

    fig.add_trace(go.Scatter(
        x=x[neg_mask], y=y[neg_mask], fill='tozeroy', fillcolor='rgba(255, 0, 0, 0.1)', line=dict(color='black', width=2), name='Loss', showlegend=False)
    ) 

# ============================================================================= #
st.title("Option Strategy Profit/Loss Calculator (Customized)")

spot_price = st.text_input("**:blue[Spot Price]**", value=100)
spot_price = float(spot_price)

lc = st.checkbox('Buy Call')
lp = st.checkbox('Buy Put')
with st.form(key='Long_Option'):
    c1, c2, c3, c4 = st.columns(4)
    if lc:
        with c1:
            strike_price_long_call = st.text_input("Long Call Strike Price", value=0)
            strike_price_long_call = float(strike_price_long_call)

        with c2:
            premium_long_call = st.text_input("Long Call Premium", value=0)
            premium_long_call = float(premium_long_call)
    if lp:
        with c3:
            strike_price_long_put = st.text_input("Long Put Strike Price", value="0")
            strike_price_long_put = float(strike_price_long_put)
        with c4:
            premium_long_put = st.text_input("Long Put Premium", value=0)
            premium_long_put = float(premium_long_put)

    submitButton = st.form_submit_button(label = 'Long Side Calculate')

sc = st.checkbox('Sell Call')
sp = st.checkbox('Sell Put')
with st.form(key='Short_Option'):
    c1, c2, c3, c4 = st.columns(4)
    if sc:
        with c1:
            strike_price_short_call = st.text_input("Short Call Strike Price", value=0)
            strike_price_short_call = float(strike_price_short_call)   
        with c2:
            premium_short_call = st.text_input("Short Call Premium", value=0)
            premium_short_call = float(premium_short_call)
    if sp:       
        with c3:
            strike_price_short_put = st.text_input("Short Put Strike Price", value="0")
            strike_price_short_put = float(strike_price_short_put)
        with c4:
            premium_short_put = st.text_input("Short Put Premium", value=0)
            premium_short_put = float(premium_short_put)
    
    submitButton = st.form_submit_button(label = 'Short Side Calculate')


st.write('='*88)

extra_legs = st.checkbox('Need Additional Legs')
if extra_legs:
    lc_add = st.checkbox('Additional Buy Call')
    lp_add = st.checkbox('Additional Buy Put')
    with st.form(key='Additional Long_Option'):
        c1, c2, c3, c4 = st.columns(4)
        if lc_add:
            with c1:
                strike_price_long_call_add = st.text_input("Long Call Strike Price", value=0)
                strike_price_long_call_add = float(strike_price_long_call_add)

            with c2:
                premium_long_call_add = st.text_input("Long Call Premium", value=0)
                premium_long_call_add = float(premium_long_call_add)
        if lp_add:
            with c3:
                strike_price_long_put_add = st.text_input("Long Put Strike Price", value="0")
                strike_price_long_put_add = float(strike_price_long_put_add)
            with c4:
                premium_long_put_add = st.text_input("Long Put Premium", value=0)
                premium_long_put_add = float(premium_long_put_add)

        submitButton_add = st.form_submit_button(label = 'Long Side Calculate')

    sc_add = st.checkbox('Additional Sell Call')
    sp_add = st.checkbox('Additional Sell Put')
    with st.form(key='AdditionalShort_Option'):
        c1, c2, c3, c4 = st.columns(4)
        if sc_add:
            with c1:
                strike_price_short_call_add = st.text_input("Short Call Strike Price", value=0)
                strike_price_short_call_add = float(strike_price_short_call_add)   
            with c2:
                premium_short_call_add = st.text_input("Short Call Premium", value=0)
                premium_short_call_add = float(premium_short_call_add)
        if sp_add:       
            with c3:
                strike_price_short_put_add = st.text_input("Short Put Strike Price", value="0")
                strike_price_short_put_add = float(strike_price_short_put_add)
            with c4:
                premium_short_put_add = st.text_input("Short Put Premium", value=0)
                premium_short_put_add = float(premium_short_put_add)
    
        submitButton = st.form_submit_button(label = 'Short Side Calculate')

# ============================================================================= #
PlotRange = np.arange(0.9*spot_price, 1.1*spot_price, 0.01)

def call_payoff(PlotRange, strike_price, premium):
    return np.where(PlotRange > strike_price, PlotRange - strike_price, 0) - premium

def put_payoff(PlotRange, strike_price, premium):
    return np.where(PlotRange < strike_price, strike_price - PlotRange, 0) - premium

payoff = np.zeros(len(PlotRange))
if lc:
    payoff_long_call = call_payoff(PlotRange, strike_price_long_call, premium_long_call)
    payoff += payoff_long_call
if lp:
    payoff_long_put = put_payoff(PlotRange, strike_price_long_put, premium_long_put)
    payoff += payoff_long_put

if sc:
    payoff_short_call = -1.0*call_payoff(PlotRange, strike_price_short_call, premium_short_call)
    payoff += payoff_short_call
if sp:
    payoff_short_put = -1.0*put_payoff(PlotRange, strike_price_short_put, premium_short_put)
    payoff += payoff_short_put

if extra_legs:
    if lc_add:
        payoff_long_call_add = call_payoff(PlotRange, strike_price_long_call_add, premium_long_call_add)
        payoff += payoff_long_call_add
    if lp_add:
        payoff_long_put_add = put_payoff(PlotRange, strike_price_long_put_add, premium_long_put_add)
        payoff += payoff_long_put_add
    if sc_add:
        payoff_short_call_add = -1.0*call_payoff(PlotRange, strike_price_short_call_add, premium_short_call_add)
        payoff += payoff_short_call_add
    if sp_add:
        payoff_short_put_add = -1.0*put_payoff(PlotRange, strike_price_short_put_add, premium_short_put_add)
        payoff += payoff_short_put_add 

payoff = 100*payoff
# ============================================================================= #
fig = go.Figure()

# plot long call payoff
#fig.add_trace(go.Scatter(x=PlotRange, y=payoff_long_call, mode='lines', line=dict(dash='dot'), name='Long Call', line_color='green'))
#fig.add_trace(go.Scatter(x=PlotRange, y=payoff_long_put, mode='lines', line=dict(dash='dot'), name='Long Put', line_color='red'))
#fig.add_trace(go.Scatter(x=PlotRange, y=payoff_short_call, mode='lines', name='Short Call', line_color='green'))
#fig.add_trace(go.Scatter(x=PlotRange, y=payoff_short_put, mode='lines', name='Short Put', line_color='red'))

fig.add_trace(go.Scatter(x=PlotRange, y=payoff, mode='lines', name='Strategy', line_color='black'))

# fill the area below the payoff curve
#PL_colorfill(PlotRange, payoff_long_call)
#PL_colorfill(PlotRange, payoff_long_put)
#PL_colorfill(PlotRange, payoff_short_call)
#PL_colorfill(PlotRange, payoff_short_put)
PL_colorfill(PlotRange, payoff)

st.write("Maximum Profit [within the shown range]:", str(round(payoff[np.where(payoff==max(payoff))][0], 2)))
st.write("Maximum Loss [within the shown range]:", str(round(payoff[np.where(payoff==min(payoff))][0], 2)))

zero_crossings = np.where(np.diff(np.sign(payoff)))[0]

if (len(zero_crossings) == 1):
    st.write("Breakeven Price:", round(PlotRange[zero_crossings[0]],2))

if (len(zero_crossings) == 2):
    st.write("Lower Breakeven Price:", round(PlotRange[zero_crossings[0]],2))
    st.write("Upper Breakeven Price:", round(PlotRange[zero_crossings[1]],2))

fig.add_vline(x=spot_price, line_width=1, line_color="blue")

# format the layout
fig.update_layout(
    plot_bgcolor="#FFF", 
    hovermode="x",
    hoverdistance=500, # Distance to show hover label of data point
    spikedistance=1000, # Distance to show spike
    xaxis=dict(
        title="Price",
        linecolor="#BCCCDC",  
        showgrid=False,
        titlefont=dict(size=20),
        tickfont = dict(size=18),
        showspikes=True, # Show spike line for X-axis
        spikethickness=2,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across"
    ),
    yaxis=dict(
        title="Profit/Loss",
        linecolor="#BCCCDC", 
        zeroline=True,
        zerolinewidth=1, 
        zerolinecolor='black',
        showgrid=False, 
        titlefont=dict(size=20),
        tickfont = dict(size=18)
    ),
    legend=dict(
        x=0.45, y=0.98, 
        font=dict(size=15),
        bgcolor='rgba(0,0,0,0)',
        itemsizing='constant',
        itemclick=False,
        itemdoubleclick=False
    )
)


st.plotly_chart(fig, theme="streamlit", use_container_width=True)

''' Disclaimer:
The Profit and Loss Chart provided assumes that positions will be held until their expiration date.
However, it is important to note that the actual losses incurred may be greater than the values calculated in the chart due to various factors 
such as changes in implied volatility, early assignment, ex-dividend dates, and other market conditions.
This Chart is intended for informational purposes only and should not be considered as personalized recommendations or investment advice. 
'''