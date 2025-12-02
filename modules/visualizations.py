# Visualization Module
# Handles chart creation and visual components

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
from .config import UIConfig


class ChartCreator:
    """Professional chart creation with dark theme"""
    
    @staticmethod
    def create_dark_theme_chart(data, symbol):
        """Create professional dark theme chart with geometric styling"""
        try:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                subplot_titles=(f'{symbol} Price Movement', 'Volume Analysis'),
                row_heights=[0.7, 0.3]
            )
            
            # Candlestick chart with dark theme
            fig.add_trace(
                go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name=symbol,
                    increasing_line_color=UIConfig.COLORS['accent_green'],
                    decreasing_line_color=UIConfig.COLORS['accent_red'],
                    increasing_fillcolor=UIConfig.COLORS['accent_green'],
                    decreasing_fillcolor=UIConfig.COLORS['accent_red']
                ),
                row=1, col=1
            )
            
            # Volume chart with matching colors
            colors = [UIConfig.COLORS['accent_red'] if close < open else UIConfig.COLORS['accent_green'] 
                     for close, open in zip(data['Close'], data['Open'])]
            
            fig.add_trace(
                go.Bar(
                    x=data.index,
                    y=data['Volume'],
                    name='Volume',
                    marker_color=colors,
                    opacity=0.6
                ),
                row=2, col=1
            )
            
            # Update layout for dark theme
            fig.update_layout(
                title={
                    'text': f'{symbol} Technical Analysis',
                    'font': {'color': UIConfig.COLORS['text_primary'], 'size': 20, 'family': UIConfig.FONTS['primary']},
                    'x': 0.5
                },
                plot_bgcolor=UIConfig.COLORS['primary_bg'],
                paper_bgcolor=UIConfig.COLORS['card_bg'],
                font={'color': UIConfig.COLORS['text_primary'], 'family': UIConfig.FONTS['primary']},
                height=600,
                showlegend=False,
                xaxis_rangeslider_visible=False
            )
            
            # Update axes
            fig.update_xaxes(
                showgrid=True, 
                gridwidth=1, 
                gridcolor=UIConfig.COLORS['border_color'],
                showline=True,
                linecolor=UIConfig.COLORS['border_color'],
                color=UIConfig.COLORS['text_secondary']
            )
            fig.update_yaxes(
                showgrid=True, 
                gridwidth=1, 
                gridcolor=UIConfig.COLORS['border_color'],
                showline=True,
                linecolor=UIConfig.COLORS['border_color'],
                color=UIConfig.COLORS['text_secondary']
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Chart creation failed: {str(e)}")
            return None


class UIComponents:
    """Reusable UI components with consistent styling"""
    
    @staticmethod
    def create_section_header(title):
        """Create a styled section header"""
        return f'<div class="section-header">{title}</div>'
    
    @staticmethod
    def create_metric_card(label, value, delta=None, delta_color="normal"):
        """Create a styled metric card"""
        return st.metric(label, value, delta, delta_color=delta_color)
    
    @staticmethod
    def create_info_box(title, content):
        """Create an information box"""
        return f"""
        <div class="info-box">
            <div class="info-title">{title}</div>
            <div class="info-content">{content}</div>
        </div>
        """
    
    @staticmethod
    def create_status_indicator(service, status, description):
        """Create a status indicator for API services"""
        status_class = "status-active" if status == "Active" else "status-inactive"
        return f"""
        <div class="metric-card">
            <div class="{status_class}">{service}: {status}</div>
            <div class="info-content">{description}</div>
        </div>
        """
