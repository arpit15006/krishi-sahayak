import logging
from PIL import Image

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

logger = logging.getLogger(__name__)

def analyze_plant_with_huggingface(image_path):
    """Analyze plant image using Hugging Face models"""
    if not TORCH_AVAILABLE:
        return {
            'diagnosis': "PyTorch not available",
            'treatment': "AI analysis requires PyTorch. Using fallback analysis.",
            'error': 'Missing PyTorch dependency'
        }
    
    try:
        # Try to import transformers
        from transformers import pipeline, AutoImageProcessor, AutoModelForImageClassification
        
        # Load plant disease classification model
        model_name = "nateraw/vit-base-beans"  # Plant disease model
        
        # Create classifier
        classifier = pipeline("image-classification", model=model_name)
        
        # Load and process image
        image = Image.open(image_path).convert('RGB')
        
        # Get predictions
        results = classifier(image)
        
        # Format results
        top_result = results[0]
        confidence = top_result['score'] * 100
        
        diagnosis = f"Disease detected: {top_result['label']} (Confidence: {confidence:.1f}%)"
        
        # Generate treatment based on detected disease
        treatment = generate_treatment_advice(top_result['label'], confidence)
        
        return {
            'diagnosis': diagnosis,
            'treatment': treatment,
            'confidence': f"{confidence:.1f}%",
            'model': 'Hugging Face Vision Transformer'
        }
        
    except ImportError:
        return {
            'diagnosis': "Hugging Face not installed",
            'treatment': "Please install: pip install transformers torch torchvision pillow",
            'error': 'Missing dependencies'
        }
    except Exception as e:
        logger.error(f"Hugging Face analysis error: {str(e)}")
        return {
            'diagnosis': "Local AI analysis failed",
            'treatment': f"Error: {str(e)}. Please try again or check image format.",
            'error': str(e)
        }

def generate_treatment_advice(disease_label, confidence):
    """Generate treatment advice based on detected disease"""
    
    treatments = {
        'angular_leaf_spot': """
**ORGANIC TREATMENT:**
• Neem oil spray (10ml per liter water)
• Copper sulfate solution (2g per liter)
• Remove affected leaves immediately

**CHEMICAL TREATMENT:**
• Mancozeb fungicide (2g per liter)
• Copper oxychloride spray
• Apply every 7-10 days

**PREVENTION:**
• Avoid overhead watering
• Ensure good air circulation
• Crop rotation recommended
        """,
        
        'bean_rust': """
**ORGANIC TREATMENT:**
• Baking soda spray (5g per liter water)
• Neem oil application twice weekly
• Garlic-chili extract spray

**CHEMICAL TREATMENT:**
• Propiconazole fungicide
• Tebuconazole spray (1ml per liter)
• Systemic fungicide application

**PREVENTION:**
• Plant resistant varieties
• Avoid wet foliage
• Morning watering only
        """,
        
        'healthy': """
**PLANT APPEARS HEALTHY:**
• Continue current care routine
• Monitor for early disease signs
• Maintain proper watering schedule

**PREVENTIVE CARE:**
• Weekly neem oil spray
• Balanced fertilization
• Regular inspection for pests

**GENERAL TIPS:**
• Water at soil level, not leaves
• Ensure adequate spacing
• Remove dead plant material
        """
    }
    
    # Get specific treatment or default advice
    treatment = treatments.get(disease_label.lower(), treatments['healthy'])
    
    if confidence < 70:
        treatment += f"\n\n**NOTE:** Low confidence ({confidence:.1f}%). Consider getting expert opinion."
    
    return treatment.strip()