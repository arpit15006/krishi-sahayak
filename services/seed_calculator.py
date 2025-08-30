"""
Seed Calculator Service for Krishi Sahayak
Calculates seed requirements based on crop, area, and farming practices
"""

class SeedCalculator:
    def __init__(self):
        # Seed rates in kg per acre for different crops
        self.seed_rates = {
            'rice': {
                'broadcasting': 25,
                'line_sowing': 20,
                'transplanting': 8,
                'dibbling': 15
            },
            'wheat': {
                'broadcasting': 50,
                'line_sowing': 40,
                'transplanting': 35,
                'dibbling': 45
            },
            'maize': {
                'broadcasting': 12,
                'line_sowing': 8,
                'transplanting': 6,
                'dibbling': 10
            },
            'cotton': {
                'broadcasting': 2,
                'line_sowing': 1.5,
                'transplanting': 1,
                'dibbling': 1.2
            },
            'sugarcane': {
                'broadcasting': 2500,  # kg/acre (sets)
                'line_sowing': 2000,
                'transplanting': 1800,
                'dibbling': 2200
            },
            'soybean': {
                'broadcasting': 40,
                'line_sowing': 30,
                'transplanting': 25,
                'dibbling': 35
            },
            'groundnut': {
                'broadcasting': 60,
                'line_sowing': 45,
                'transplanting': 40,
                'dibbling': 50
            },
            'sunflower': {
                'broadcasting': 4,
                'line_sowing': 2.5,
                'transplanting': 2,
                'dibbling': 3
            },
            'mustard': {
                'broadcasting': 3,
                'line_sowing': 2,
                'transplanting': 1.5,
                'dibbling': 2.5
            },
            'chickpea': {
                'broadcasting': 45,
                'line_sowing': 35,
                'transplanting': 30,
                'dibbling': 40
            },
            'pigeon_pea': {
                'broadcasting': 12,
                'line_sowing': 8,
                'transplanting': 6,
                'dibbling': 10
            },
            'black_gram': {
                'broadcasting': 20,
                'line_sowing': 15,
                'transplanting': 12,
                'dibbling': 18
            },
            'green_gram': {
                'broadcasting': 18,
                'line_sowing': 12,
                'transplanting': 10,
                'dibbling': 15
            },
            'onion': {
                'broadcasting': 4,
                'line_sowing': 3,
                'transplanting': 2,
                'dibbling': 3.5
            },
            'tomato': {
                'broadcasting': 0.5,
                'line_sowing': 0.3,
                'transplanting': 0.2,
                'dibbling': 0.4
            },
            'potato': {
                'broadcasting': 800,  # kg/acre (tubers)
                'line_sowing': 600,
                'transplanting': 500,
                'dibbling': 700
            },
            'cabbage': {
                'broadcasting': 0.8,
                'line_sowing': 0.5,
                'transplanting': 0.3,
                'dibbling': 0.6
            },
            'cauliflower': {
                'broadcasting': 0.6,
                'line_sowing': 0.4,
                'transplanting': 0.25,
                'dibbling': 0.5
            }
        }
        
        # Area conversion factors to acres
        self.area_conversions = {
            'acre': 1,
            'hectare': 2.47,
            'bigha': 0.62,  # Standard bigha
            'katha': 0.031  # Standard katha
        }
        
        # Seed cost per kg (approximate in INR)
        self.seed_costs = {
            'rice': 50,
            'wheat': 25,
            'maize': 80,
            'cotton': 2000,
            'sugarcane': 2,  # per kg of sets
            'soybean': 60,
            'groundnut': 80,
            'sunflower': 150,
            'mustard': 100,
            'chickpea': 70,
            'pigeon_pea': 90,
            'black_gram': 120,
            'green_gram': 110,
            'onion': 800,
            'tomato': 15000,
            'potato': 20,  # per kg of seed tubers
            'cabbage': 8000,
            'cauliflower': 10000
        }

    def calculate_seed_requirement(self, crop_data):
        """Calculate seed requirement based on input parameters"""
        try:
            crop_type = crop_data.get('crop_type')
            variety = crop_data.get('variety', 'standard')
            farm_area = float(crop_data.get('farm_area', 1))
            area_unit = crop_data.get('area_unit', 'acre')
            sowing_method = crop_data.get('sowing_method', 'line_sowing')
            soil_type = crop_data.get('soil_type', 'loam')
            season = crop_data.get('season', 'kharif')
            
            # Convert area to acres
            area_in_acres = farm_area * self.area_conversions.get(area_unit, 1)
            
            # Get base seed rate
            if crop_type not in self.seed_rates:
                return {'success': False, 'error': f'Crop {crop_type} not supported'}
            
            base_seed_rate = self.seed_rates[crop_type].get(sowing_method, 
                                                          self.seed_rates[crop_type]['line_sowing'])
            
            # Apply variety adjustments
            variety_factor = self._get_variety_factor(variety)
            
            # Apply soil type adjustments
            soil_factor = self._get_soil_factor(soil_type, crop_type)
            
            # Apply season adjustments
            season_factor = self._get_season_factor(season, crop_type)
            
            # Calculate adjusted seed rate
            adjusted_seed_rate = base_seed_rate * variety_factor * soil_factor * season_factor
            
            # Calculate total seed required
            total_seed_required = adjusted_seed_rate * area_in_acres
            
            # Add 10% extra for contingency
            extra_seed = total_seed_required * 0.1
            final_seed_required = total_seed_required + extra_seed
            
            # Calculate costs
            cost_analysis = self._calculate_costs(crop_type, final_seed_required, area_in_acres)
            
            # Get sowing information
            sowing_info = self._get_sowing_info(crop_type, sowing_method)
            
            # Get recommendations
            recommendations = self._get_recommendations(crop_type, variety, sowing_method, season)
            
            return {
                'success': True,
                'calculation': {
                    'crop_type': crop_type,
                    'variety': variety,
                    'farm_area': farm_area,
                    'area_unit': area_unit,
                    'area_in_acres': round(area_in_acres, 2),
                    'sowing_method': sowing_method,
                    'soil_type': soil_type,
                    'season': season,
                    'seed_rate': round(adjusted_seed_rate, 2),
                    'seed_required': round(final_seed_required, 2),
                    'extra_seed': round(extra_seed, 2),
                    'cost_analysis': cost_analysis,
                    'sowing_info': sowing_info,
                    'recommendations': recommendations
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_variety_factor(self, variety):
        """Get adjustment factor based on variety"""
        factors = {
            'standard': 1.0,
            'hybrid': 0.8,  # Hybrids usually need less seed
            'high_yield': 0.9,
            'drought_resistant': 1.1
        }
        return factors.get(variety, 1.0)

    def _get_soil_factor(self, soil_type, crop_type):
        """Get adjustment factor based on soil type"""
        # Different crops perform differently in different soils
        factors = {
            'clay': {
                'rice': 0.9,  # Rice does well in clay
                'wheat': 1.1,
                'default': 1.0
            },
            'loam': {
                'default': 1.0  # Ideal soil for most crops
            },
            'sandy': {
                'groundnut': 0.9,  # Groundnut prefers sandy soil
                'default': 1.1  # Most crops need more seed in sandy soil
            },
            'black': {
                'cotton': 0.9,  # Cotton does well in black soil
                'soybean': 0.9,
                'default': 1.0
            },
            'red': {
                'default': 1.05
            }
        }
        
        soil_factors = factors.get(soil_type, {'default': 1.0})
        return soil_factors.get(crop_type, soil_factors.get('default', 1.0))

    def _get_season_factor(self, season, crop_type):
        """Get adjustment factor based on season"""
        # Some crops need different seed rates in different seasons
        factors = {
            'kharif': {
                'rice': 1.0,
                'maize': 1.0,
                'cotton': 1.0,
                'soybean': 1.0,
                'default': 1.1
            },
            'rabi': {
                'wheat': 1.0,
                'chickpea': 1.0,
                'mustard': 1.0,
                'default': 1.05
            },
            'zaid': {
                'sunflower': 1.0,
                'default': 1.15  # Summer crops need more seed
            },
            'year_round': {
                'default': 1.0
            }
        }
        
        season_factors = factors.get(season, {'default': 1.0})
        return season_factors.get(crop_type, season_factors.get('default', 1.0))

    def _calculate_costs(self, crop_type, seed_required, area_in_acres):
        """Calculate cost analysis"""
        seed_cost_per_kg = self.seed_costs.get(crop_type, 50)
        seed_cost = seed_required * seed_cost_per_kg
        
        # Sowing cost (approximate)
        sowing_cost_per_acre = 500  # INR per acre
        sowing_cost = area_in_acres * sowing_cost_per_acre
        
        total_cost = seed_cost + sowing_cost
        
        return {
            'seed_cost': round(seed_cost),
            'sowing_cost': round(sowing_cost),
            'total_cost': round(total_cost),
            'cost_per_acre': round(total_cost / area_in_acres) if area_in_acres > 0 else 0
        }

    def _get_sowing_info(self, crop_type, sowing_method):
        """Get sowing information for the crop"""
        sowing_data = {
            'rice': {
                'depth': '2-3 सेमी',
                'row_spacing': '20-25 सेमी',
                'plant_spacing': '10-15 सेमी',
                'best_time': 'जून-जुलाई (खरीफ)'
            },
            'wheat': {
                'depth': '3-5 सेमी',
                'row_spacing': '18-23 सेमी',
                'plant_spacing': '5-7 सेमी',
                'best_time': 'नवंबर-दिसंबर (रबी)'
            },
            'maize': {
                'depth': '3-4 सेमी',
                'row_spacing': '60-75 सेमी',
                'plant_spacing': '20-25 सेमी',
                'best_time': 'जून-जुलाई (खरीफ)'
            },
            'cotton': {
                'depth': '2-3 सेमी',
                'row_spacing': '90-120 सेमी',
                'plant_spacing': '30-45 सेमी',
                'best_time': 'मई-जून (खरीफ)'
            },
            'soybean': {
                'depth': '3-4 सेमी',
                'row_spacing': '30-45 सेमी',
                'plant_spacing': '5-7 सेमी',
                'best_time': 'जून-जुलाई (खरीफ)'
            }
        }
        
        return sowing_data.get(crop_type, {
            'depth': '2-4 सेमी',
            'row_spacing': '30 सेमी',
            'plant_spacing': '10 सेमी',
            'best_time': 'मौसम के अनुसार'
        })

    def _get_recommendations(self, crop_type, variety, sowing_method, season):
        """Get recommendations based on inputs"""
        recommendations = []
        
        # General recommendations
        recommendations.append("प्रमाणित बीज का ही उपयोग करें")
        recommendations.append("बुवाई से पहले बीज उपचार करें")
        
        # Crop-specific recommendations
        if crop_type == 'rice':
            recommendations.append("नर्सरी में पौध तैयार करने के लिए 25-30 दिन का समय दें")
            recommendations.append("रोपाई के समय पानी की उचित व्यवस्था करें")
        elif crop_type == 'wheat':
            recommendations.append("देर से बुवाई करने पर बीज की मात्रा 25% बढ़ा दें")
            recommendations.append("सिंचाई की उचित व्यवस्था करें")
        elif crop_type == 'cotton':
            recommendations.append("बीज को कवकनाशी से उपचारित करें")
            recommendations.append("कतारों के बीच उचित दूरी बनाए रखें")
        
        # Variety-specific recommendations
        if variety == 'hybrid':
            recommendations.append("हाइब्रिड बीज महंगा है लेकिन उत्पादन अधिक मिलता है")
        elif variety == 'drought_resistant':
            recommendations.append("सूखा प्रतिरोधी किस्म कम पानी में भी अच्छा उत्पादन देती है")
        
        # Sowing method recommendations
        if sowing_method == 'line_sowing':
            recommendations.append("कतार में बुवाई से खरपतवार नियंत्रण आसान होता है")
        elif sowing_method == 'transplanting':
            recommendations.append("रोपाई विधि में पानी की अधिक आवश्यकता होती है")
        
        # Season-specific recommendations
        if season == 'kharif':
            recommendations.append("मानसून की शुरुआत के साथ बुवाई करें")
        elif season == 'rabi':
            recommendations.append("सर्दी के मौसम में ठंड से बचाव करें")
        elif season == 'zaid':
            recommendations.append("गर्मी के मौसम में अधिक सिंचाई की आवश्यकता होती है")
        
        return recommendations

# Create global instance
seed_calculator = SeedCalculator()