"""
Stock Analysis app signals
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AnalysisRequest
