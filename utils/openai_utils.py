"""
OpenAI ChatGPT Integration for Project Details Auto-Generation
Generates project descriptions based on selected products
"""

import os
import json
from typing import Optional


def generate_project_description(product_list: list, api_key: str) -> Optional[str]:
    """
    Generate project description using OpenAI ChatGPT based on selected products.
    
    Args:
        product_list: List of product dictionaries with 'description' and 'qty' keys
        api_key: OpenAI API key
        
    Returns:
        Generated project description string or None if API call fails
    """
    
    if not api_key or api_key.strip() == "":
        return None
    
    try:
        import openai
        openai.api_key = api_key
        
        # Build product summary
        products_text = "\n".join([
            f"- {prod.get('description', 'Unknown')} (Qty: {int(prod.get('qty', 1))})"
            for prod in product_list if prod.get('description')
        ])
        
        if not products_text:
            return None
        
        prompt = f"""Generate a professional project description for a smart home installation project.
        
Selected Products:
{products_text}

Create a brief, professional project description (2-3 sentences) that:
1. Summarizes what smart home systems/devices will be installed
2. Mentions the scope of work
3. Is suitable for a formal invoice

Be concise and professional."""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional smart home project manager writing project descriptions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except ImportError:
        return None
    except Exception as e:
        print(f"Error generating project description: {e}")
        return None
