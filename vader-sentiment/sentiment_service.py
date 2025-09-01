from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize VADER analyzer
analyzer = SentimentIntensityAnalyzer()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'VADER Sentiment Analysis API',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment for multiple texts"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        texts = data.get('texts', [])
        
        if not texts:
            return jsonify({'error': 'No texts provided for analysis'}), 400
        
        if not isinstance(texts, list):
            return jsonify({'error': 'Texts must be provided as an array'}), 400
        
        # Analyze each text
        results = []
        for i, text in enumerate(texts):
            if not isinstance(text, str):
                logger.warning(f"Skipping non-string text at index {i}: {type(text)}")
                continue
                
            scores = analyzer.polarity_scores(text)
            classification = classify_sentiment(scores['compound'])
            
            results.append({
                'text': text,
                'scores': scores,
                'classification': classification,
                'index': i
            })
        
        if not results:
            return jsonify({'error': 'No valid texts to analyze'}), 400
        
        # Calculate summary statistics
        summary = calculate_summary(results)
        insights = generate_insights(results)
        
        response = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'total_analyzed': len(results),
            'results': results,
            'summary': summary,
            'insights': insights
        }
        
        logger.info(f"Successfully analyzed {len(results)} texts")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/analyze/single', methods=['POST'])
def analyze_single_text():
    """Analyze sentiment for a single text"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided for analysis'}), 400
        
        if not isinstance(text, str):
            return jsonify({'error': 'Text must be a string'}), 400
        
        # Analyze the text
        scores = analyzer.polarity_scores(text)
        classification = classify_sentiment(scores['compound'])
        
        response = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'text': text,
            'scores': scores,
            'classification': classification,
            'details': {
                'positive_percentage': round(scores['pos'] * 100, 1),
                'neutral_percentage': round(scores['neu'] * 100, 1),
                'negative_percentage': round(scores['neg'] * 100, 1),
                'intensity': abs(scores['compound']),
                'confidence': calculate_confidence(scores)
            }
        }
        
        logger.info(f"Successfully analyzed single text: {classification}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error analyzing single text: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

def classify_sentiment(compound_score):
    """Classify sentiment based on compound score"""
    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def calculate_confidence(scores):
    """Calculate confidence level based on score distribution"""
    # Higher absolute compound score = higher confidence
    compound_abs = abs(scores['compound'])
    
    # More extreme pos/neg vs neu = higher confidence
    extreme_ratio = max(scores['pos'], scores['neg']) / max(scores['neu'], 0.01)
    
    # Combine factors
    confidence = min(100, (compound_abs + extreme_ratio / 10) * 100)
    return round(confidence, 1)

def calculate_summary(results):
    """Calculate summary statistics for multiple results"""
    if not results:
        return {}
    
    # Calculate averages
    total_results = len(results)
    avg_compound = sum(r['scores']['compound'] for r in results) / total_results
    avg_pos = sum(r['scores']['pos'] for r in results) / total_results
    avg_neu = sum(r['scores']['neu'] for r in results) / total_results
    avg_neg = sum(r['scores']['neg'] for r in results) / total_results
    
    # Count classifications
    sentiment_counts = {}
    for result in results:
        classification = result['classification']
        sentiment_counts[classification] = sentiment_counts.get(classification, 0) + 1
    
    # Convert to percentages
    sentiment_percentages = {
        sentiment: round((count / total_results) * 100, 1)
        for sentiment, count in sentiment_counts.items()
    }
    
    # Ensure all sentiment types are present
    for sentiment in ['Positive', 'Neutral', 'Negative']:
        if sentiment not in sentiment_percentages:
            sentiment_percentages[sentiment] = 0.0
    
    return {
        'overall': {
            'compound': round(avg_compound, 3),
            'pos': round(avg_pos, 3),
            'neu': round(avg_neu, 3),
            'neg': round(avg_neg, 3),
            'classification': classify_sentiment(avg_compound)
        },
        'percentages': sentiment_percentages,
        'distribution': sentiment_counts,
        'total_analyzed': total_results
    }

def generate_insights(results):
    """Generate insights from sentiment analysis results"""
    if not results:
        return {}
    
    # Find most positive and negative
    most_positive = max(results, key=lambda x: x['scores']['compound'])
    most_negative = min(results, key=lambda x: x['scores']['compound'])
    
    # Calculate emotional intensity
    intensities = [abs(r['scores']['compound']) for r in results]
    avg_intensity = sum(intensities) / len(intensities)
    
    # Count strong emotions
    strong_positive = len([r for r in results if r['scores']['compound'] > 0.5])
    strong_negative = len([r for r in results if r['scores']['compound'] < -0.5])
    
    # Detect patterns
    neutral_ratio = len([r for r in results if r['classification'] == 'Neutral']) / len(results)
    emotional_variance = max(intensities) - min(intensities) if intensities else 0
    
    insights = {
        'emotional_intensity': {
            'average': round(avg_intensity, 3),
            'max': round(max(intensities), 3),
            'min': round(min(intensities), 3),
            'variance': round(emotional_variance, 3)
        },
        'strong_emotions': {
            'positive_count': strong_positive,
            'negative_count': strong_negative,
            'total_strong': strong_positive + strong_negative
        },
        'extremes': {
            'most_positive': {
                'text': most_positive['text'][:100] + '...' if len(most_positive['text']) > 100 else most_positive['text'],
                'score': most_positive['scores']['compound'],
                'index': most_positive['index']
            } if most_positive['scores']['compound'] > 0 else None,
            'most_negative': {
                'text': most_negative['text'][:100] + '...' if len(most_negative['text']) > 100 else most_negative['text'],
                'score': most_negative['scores']['compound'],
                'index': most_negative['index']
            } if most_negative['scores']['compound'] < 0 else None
        },
        'patterns': {
            'neutral_dominant': neutral_ratio > 0.5,
            'polarized': emotional_variance > 1.0,
            'highly_positive': strong_positive > len(results) * 0.3,
            'concerning_negative': strong_negative > len(results) * 0.2
        }
    }
    
    return insights

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting VADER Sentiment Analysis API...")
    logger.info("Available endpoints:")
    logger.info("  GET  / - Health check")
    logger.info("  POST /analyze - Analyze multiple texts")
    logger.info("  POST /analyze/single - Analyze single text")
    
    app.run(
        host='0.0.0.0', 
        port=5001, 
        debug=True,
        threaded=True
    )
