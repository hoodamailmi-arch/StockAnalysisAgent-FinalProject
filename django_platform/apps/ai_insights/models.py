"""
AI Insights app models
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()


class AIModel(models.Model):
    """AI model configurations"""
    
    name = models.CharField(max_length=100, unique=True)
    provider = models.CharField(max_length=50)  # groq, openai, etc.
    model_id = models.CharField(max_length=100)
    max_tokens = models.IntegerField(default=4000)
    temperature = models.FloatField(default=0.1)
    is_active = models.BooleanField(default=True)
    cost_per_token = models.DecimalField(max_digits=8, decimal_places=6, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'ai_model'
        verbose_name = 'AI Model'
        verbose_name_plural = 'AI Models'
    
    def __str__(self):
        return f"{self.provider} - {self.name}"


class PromptTemplate(models.Model):
    """Prompt templates for different analysis types"""
    
    ANALYSIS_TYPES = [
        ('technical', 'Technical Analysis'),
        ('fundamental', 'Fundamental Analysis'),
        ('sentiment', 'Sentiment Analysis'),
        ('comprehensive', 'Comprehensive Analysis'),
    ]
    
    name = models.CharField(max_length=100)
    analysis_type = models.CharField(max_length=20, choices=ANALYSIS_TYPES)
    template = models.TextField()
    variables = models.JSONField(default=list)  # List of variable names expected in template
    is_default = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'prompt_template'
        verbose_name = 'Prompt Template'
        verbose_name_plural = 'Prompt Templates'
        unique_together = ['name', 'analysis_type']
    
    def __str__(self):
        return f"{self.name} ({self.analysis_type})"


class AnalysisPrompt(models.Model):
    """Generated prompts for analysis requests"""
    
    analysis_request = models.OneToOneField(
        'stock_analysis.AnalysisRequest',
        on_delete=models.CASCADE,
        related_name='prompt'
    )
    template = models.ForeignKey(PromptTemplate, on_delete=models.SET_NULL, null=True)
    prompt_text = models.TextField()
    variables_used = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'analysis_prompt'
        verbose_name = 'Analysis Prompt'
        verbose_name_plural = 'Analysis Prompts'
    
    def __str__(self):
        return f"Prompt for {self.analysis_request.id}"


class AIResponse(models.Model):
    """AI model responses"""
    
    analysis_request = models.OneToOneField(
        'stock_analysis.AnalysisRequest',
        on_delete=models.CASCADE,
        related_name='ai_response'
    )
    model = models.ForeignKey(AIModel, on_delete=models.SET_NULL, null=True)
    prompt_tokens = models.IntegerField(default=0)
    completion_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)
    response_time = models.DurationField(null=True, blank=True)
    cost = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    raw_response = models.TextField()
    processed_response = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'ai_response'
        verbose_name = 'AI Response'
        verbose_name_plural = 'AI Responses'
    
    def __str__(self):
        return f"AI Response for {self.analysis_request.id}"


class InsightMetric(models.Model):
    """Metrics and scores for insights"""
    
    ai_response = models.OneToOneField(
        AIResponse,
        on_delete=models.CASCADE,
        related_name='metrics'
    )
    
    # Sentiment scores
    sentiment_score = models.FloatField(null=True, blank=True)  # -1 to 1
    confidence_score = models.FloatField(null=True, blank=True)  # 0 to 1
    
    # Technical scores
    technical_score = models.FloatField(null=True, blank=True)  # 0 to 100
    momentum_score = models.FloatField(null=True, blank=True)  # -100 to 100
    
    # Risk metrics
    volatility_score = models.FloatField(null=True, blank=True)  # 0 to 100
    risk_score = models.FloatField(null=True, blank=True)  # 0 to 100
    
    # Overall recommendation
    recommendation = models.CharField(
        max_length=20,
        choices=[
            ('strong_buy', 'Strong Buy'),
            ('buy', 'Buy'),
            ('hold', 'Hold'),
            ('sell', 'Sell'),
            ('strong_sell', 'Strong Sell'),
        ],
        null=True,
        blank=True
    )
    
    price_target = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'insight_metric'
        verbose_name = 'Insight Metric'
        verbose_name_plural = 'Insight Metrics'
    
    def __str__(self):
        return f"Metrics for {self.ai_response.analysis_request.id}"


class ModelUsageStats(models.Model):
    """Track model usage statistics"""
    
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='usage_stats')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='model_usage')
    date = models.DateField(default=timezone.now)
    
    # Usage counts
    total_requests = models.IntegerField(default=0)
    successful_requests = models.IntegerField(default=0)
    failed_requests = models.IntegerField(default=0)
    
    # Token usage
    total_tokens = models.IntegerField(default=0)
    prompt_tokens = models.IntegerField(default=0)
    completion_tokens = models.IntegerField(default=0)
    
    # Costs
    total_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    # Performance
    avg_response_time = models.DurationField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'model_usage_stats'
        verbose_name = 'Model Usage Stats'
        verbose_name_plural = 'Model Usage Stats'
        unique_together = ['model', 'user', 'date']
    
    def __str__(self):
        return f"{self.user.email} - {self.model.name} - {self.date}"
