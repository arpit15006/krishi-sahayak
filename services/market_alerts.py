"""
Real-time market price alerts
"""

import asyncio
import json
from datetime import datetime

class MarketAlerts:
    def __init__(self):
        self.price_thresholds = {}
        self.alerts = []
    
    def set_price_alert(self, user_id, crop, target_price, alert_type='above'):
        """Set price alert for user"""
        alert_id = f"{user_id}_{crop}_{datetime.now().timestamp()}"
        
        self.price_thresholds[alert_id] = {
            'user_id': user_id,
            'crop': crop,
            'target_price': target_price,
            'alert_type': alert_type,
            'created_at': datetime.now().isoformat()
        }
        
        return alert_id
    
    def check_price_alerts(self, current_prices):
        """Check if any alerts should be triggered"""
        triggered_alerts = []
        
        for alert_id, alert in self.price_thresholds.items():
            crop = alert['crop']
            target = alert['target_price']
            alert_type = alert['alert_type']
            
            if crop in current_prices:
                current_price = current_prices[crop]
                
                should_trigger = False
                if alert_type == 'above' and current_price >= target:
                    should_trigger = True
                elif alert_type == 'below' and current_price <= target:
                    should_trigger = True
                
                if should_trigger:
                    triggered_alerts.append({
                        'user_id': alert['user_id'],
                        'crop': crop,
                        'current_price': current_price,
                        'target_price': target,
                        'message': f"🚨 {crop} price alert! Current: ₹{current_price}/kg (Target: ₹{target}/kg)"
                    })
        
        return triggered_alerts

market_alerts = MarketAlerts()