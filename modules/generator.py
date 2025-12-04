import anthropic
import config

class RoastGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    
    def generate_roast(self, analysis_data=None):
        """
        Generate a witty roast based on image analysis data.
        
        Args:
            analysis_data: Dictionary with detected features (optional for now)
        
        Returns:
            String containing the roast text
        """
        # For now, we'll use a simple prompt
        # Later we'll make this more sophisticated with real analysis data
        
        prompt = """You are a witty roast comedian. Generate a funny, lighthearted roast 
        that's humorous but not mean-spirited. Keep it to 3-5 sentences. 
        Make it creative and unexpected."""
        
        try:
            message = self.client.messages.create(
                model=config.ROAST_MODEL,
                max_tokens=config.ROAST_MAX_TOKENS,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract the text from Claude's response
            roast_text = message.content[0].text
            return roast_text
            
        except Exception as e:
            print(f"Error generating roast: {e}")
            return "Error generating roast. Please try again!"
