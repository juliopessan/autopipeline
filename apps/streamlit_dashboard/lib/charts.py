"""Chart utilities using Plotly"""
import plotly.graph_objects as go
import pandas as pd

def success_rate_chart(data: pd.DataFrame) -> go.Figure:
    return go.Figure(data=[
        go.Scatter(
            x=data.get('date', []),
            y=data.get('success_rate', []),
            mode='lines+markers',
            name='Success Rate',
            line=dict(color='#F04E37', width=2),
            fill='tozeroy'
        )
    ]).update_layout(title='Success Rate Over Time', hovermode='x unified')

def experiments_chart(successful: int, failed: int) -> go.Figure:
    return go.Figure(data=[
        go.Pie(labels=['Successful', 'Failed'], values=[successful, failed], 
               marker=dict(colors=['#4CAF50', '#f44336']))
    ]).update_layout(title='Experiments Status')
