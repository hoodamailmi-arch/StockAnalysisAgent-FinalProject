"""
Stock Analysis Celery tasks
"""

from celery import shared_task
from django.utils import timezone
from datetime import timedelta


@shared_task
def process_stock_analysis(analysis_id):
    """Process stock analysis request"""
    from .models import AnalysisRequest
    
    try:
        analysis = AnalysisRequest.objects.get(id=analysis_id)
        analysis.status = 'processing'
        analysis.save()
        
        # Placeholder for actual AI analysis logic
        # This would integrate with your existing AI analyzer
        result = {
            'analysis_type': analysis.analysis_type,
            'symbol': analysis.symbol.symbol,
            'status': 'completed',
            'message': 'Analysis completed successfully',
            'recommendations': {
                'action': 'hold',
                'confidence': 0.75,
                'price_target': 150.00
            }
        }
        
        analysis.result_data = result
        analysis.status = 'completed'
        analysis.completed_at = timezone.now()
        analysis.processing_time = timezone.now() - analysis.created_at
        analysis.save()
        
        return f"Analysis {analysis_id} completed successfully"
        
    except AnalysisRequest.DoesNotExist:
        return f"Analysis {analysis_id} not found"
    except Exception as e:
        # Update analysis with error
        try:
            analysis = AnalysisRequest.objects.get(id=analysis_id)
            analysis.status = 'failed'
            analysis.error_message = str(e)
            analysis.save()
        except:
            pass
        return f"Analysis {analysis_id} failed: {str(e)}"


@shared_task
def update_stock_data():
    """Update stock data for all active symbols"""
    from .models import StockSymbol
    from .utils import get_stock_data
    
    symbols = StockSymbol.objects.filter(is_active=True)
    updated_count = 0
    
    for symbol in symbols:
        try:
            success = get_stock_data(symbol.symbol, '1d')
            if success:
                updated_count += 1
        except Exception as e:
            continue
    
    return f"Updated data for {updated_count} symbols"


@shared_task
def cleanup_old_data():
    """Clean up old stock data and analysis requests"""
    from .models import StockData, AnalysisRequest
    
    # Remove stock data older than 5 years
    cutoff_date = timezone.now().date() - timedelta(days=5*365)
    old_data_count = StockData.objects.filter(date__lt=cutoff_date).count()
    StockData.objects.filter(date__lt=cutoff_date).delete()
    
    # Remove failed analysis requests older than 30 days
    analysis_cutoff = timezone.now() - timedelta(days=30)
    old_analyses_count = AnalysisRequest.objects.filter(
        status='failed',
        created_at__lt=analysis_cutoff
    ).count()
    AnalysisRequest.objects.filter(
        status='failed',
        created_at__lt=analysis_cutoff
    ).delete()
    
    return f"Cleaned up {old_data_count} old data records and {old_analyses_count} old analyses"
