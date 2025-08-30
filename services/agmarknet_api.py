import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_real_market_prices(crops_list):
    """Get real market prices from AGMARKNET API"""
    try:
        # AGMARKNET API endpoint
        base_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        api_key = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
        
        market_data = []
        
        for crop in crops_list[:13]:  # Increased to 13 crops
            params = {
                'api-key': api_key,
                'format': 'json',
                'limit': 10,
                'filters[commodity]': crop
            }
            
            response = requests.get(base_url, params=params, timeout=3)
            
            if response.status_code == 200:
                data = response.json()
                records = data.get('records', [])
                
                if records:
                    # Get the most recent record
                    latest = records[0]
                    
                    market_data.append({
                        'crop': crop,
                        'current_price': latest.get('modal_price', 'N/A'),
                        'min_price': latest.get('min_price', 'N/A'),
                        'max_price': latest.get('max_price', 'N/A'),
                        'market': latest.get('market', 'Unknown'),
                        'state': latest.get('state', 'Unknown'),
                        'date': latest.get('arrival_date', datetime.now().strftime('%Y-%m-%d')),
                        'unit': 'per quintal'
                    })
                else:
                    # No data available for this crop
                    market_data.append({
                        'crop': crop,
                        'current_price': 'No data',
                        'market': 'Data not available',
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'unit': 'per quintal'
                    })
            else:
                logger.error(f"AGMARKNET API error for {crop}: {response.status_code}")
        
        return {
            'prices': market_data,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'AGMARKNET - Government of India'
        }
        
    except Exception as e:
        logger.error(f"Error fetching real market prices: {str(e)}")
        return None