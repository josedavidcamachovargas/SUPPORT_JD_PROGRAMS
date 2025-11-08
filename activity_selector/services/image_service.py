"""
Image generation and caching service for the Activity Selector application.
"""

import os
from pathlib import Path
from PIL import Image, ImageTk
import requests
from io import BytesIO
from utils.constants import IMAGE_SIZE, IMAGE_CACHE_DIR


class ImageService:
    """Handles image generation, caching, and retrieval."""
    
    def __init__(self, config_manager, cache_dir=None):
        self.config_manager = config_manager
        self.cache_dir = Path(cache_dir or IMAGE_CACHE_DIR)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_activity_image(self, activity_name, category):
        """Get or generate an image for the activity."""
        # Create a safe filename
        safe_name = "".join(c for c in activity_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        cache_file = self.cache_dir / f"{safe_name}.png"
        
        # Check cache first
        if cache_file.exists():
            try:
                img = Image.open(cache_file)
                img = img.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading cached image: {e}")
        
        # Generate new image
        if not self.config_manager.get("openai_api_key"):
            return None
        
        try:
            # Generate image using OpenAI DALL-E
            image_url = self._generate_dalle_image(activity_name, category)
            
            if image_url:
                # Download and cache the image
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                
                # Save to cache
                img.save(cache_file, 'PNG')
                
                # Resize and return
                img = img.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
        
        except Exception as e:
            print(f"Error generating image: {e}")
            raise Exception(f"Could not generate image: {str(e)}")
        
        return None
    
    def _generate_dalle_image(self, activity_name, category):
        """Generate image using OpenAI DALL-E API with plot/description context."""
        try:
            import openai
        except ImportError:
            raise Exception("Please install OpenAI package: pip install openai")
        
        api_key = self.config_manager.get("openai_api_key")
        if not api_key:
            return None
        
        try:
            client = openai.OpenAI(api_key=api_key)
            
            # Step 1: Get plot/description from ChatGPT
            plot_prompt = self._build_plot_prompt(activity_name, category)
            
            # Get description from ChatGPT
            chat_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant that provides concise, family-friendly, artistic descriptions of movies, games, and TV shows for image generation. Focus on visual elements, settings, and themes. Avoid graphic violence, horror, or mature content descriptions."
                    },
                    {"role": "user", "content": plot_prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            plot_description = chat_response.choices[0].message.content.strip()
            print(f"Generated description: {plot_description}")
            
            # Step 2: Generate image using the plot description
            image_prompt = self._build_image_prompt(activity_name, category, plot_description)
            print(f"Image prompt: {image_prompt}")
            
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=image_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                return response.data[0].url
            
            except openai.BadRequestError as e:
                # Check if it's a content policy violation
                if "content_policy_violation" in str(e):
                    print(f"Content policy violation detected. Retrying with sanitized prompt...")
                    # Retry with a more generic, safe prompt
                    safe_prompt = self._build_safe_fallback_prompt(activity_name, category)
                    print(f"Fallback prompt: {safe_prompt}")
                    
                    response = client.images.generate(
                        model="dall-e-3",
                        prompt=safe_prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                    )
                    return response.data[0].url
                else:
                    raise
        
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _build_plot_prompt(self, activity_name, category):
        """Build the prompt for getting plot description."""
        category_lower = category.lower()
        
        if category_lower == "videogame":
            return f"In 2-3 sentences, describe the gameplay and setting of the videogame: {activity_name}"
        elif category_lower == "series":
            return f"In 2-3 sentences, describe the plot and atmosphere of the TV series: {activity_name}"
        elif category_lower == "movie":
            return f"In 2-3 sentences, describe the plot and key scenes of the movie: {activity_name}"
        else:
            return f"In 2-3 sentences, describe the plot or main theme of: {activity_name}"
    
    def _build_image_prompt(self, activity_name, category, plot_description):
        """Build the prompt for image generation."""
        style = self.config_manager.get("image_style", "vibrant digital art")
        category_lower = category.lower()
        
        if category_lower == "movie":
            return f"A cinematic scene inspired by the film '{activity_name}'. {plot_description}. Artistic style: {style}, movie poster aesthetic, professional illustration, family-friendly"
        elif category_lower == "series":
            return f"A scene from the TV series '{activity_name}'. {plot_description}. Artistic style: {style}, television poster design, professional illustration"
        elif category_lower == "videogame":
            return f"Game artwork for '{activity_name}'. {plot_description}. Artistic style: {style}, video game cover art, professional digital art"
        else:
            return f"Artistic representation of '{activity_name}'. {plot_description}. Style: {style}, professional illustration"
    
    def _build_safe_fallback_prompt(self, activity_name, category):
        """Build a safe, generic prompt as fallback for content policy violations."""
        style = self.config_manager.get("image_style", "vibrant digital art")
        category_lower = category.lower()
        
        # Remove specific names and use generic descriptions
        if category_lower == "movie":
            return f"A cinematic movie poster in {style} style. Professional illustration showing an exciting adventure scene with dramatic lighting. Family-friendly, artistic, colorful composition suitable for all ages."
        elif category_lower == "series":
            return f"A TV series promotional poster in {style} style. Professional illustration with engaging characters in a story-driven scene. Artistic, vibrant colors, suitable for all audiences."
        elif category_lower == "videogame":
            return f"Video game cover art in {style} style. Professional digital illustration showing an exciting gameplay scene with dynamic action. Colorful, family-friendly, artistic design."
        else:
            return f"An artistic illustration in {style} style. Professional artwork with vibrant colors and engaging composition. Family-friendly, suitable for all ages."

    
    def delete_cached_image(self, activity_name):
        """Delete a cached image."""
        safe_name = "".join(c for c in activity_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        cache_file = self.cache_dir / f"{safe_name}.png"
        
        if cache_file.exists():
            cache_file.unlink()
            return True
        return False
    
    def clear_cache(self):
        """Clear all cached images."""
        count = 0
        for file in self.cache_dir.glob("*.png"):
            file.unlink()
            count += 1
        return count
