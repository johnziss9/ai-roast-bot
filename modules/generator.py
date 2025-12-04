import anthropic
import config

class RoastGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    
    def generate_roast(self, analysis_data=None):
        """
        Generate a witty roast based on image analysis data.
        
        Args:
            analysis_data: Dictionary with detected features
        
        Returns:
            String containing the roast text
        """
        # Build a personalized prompt based on analysis
        if analysis_data and analysis_data.get('has_face'):
            faces_count = analysis_data.get('faces_detected', 0)
            age_range = analysis_data.get('age_range', None)
            
            if faces_count == 0:
                context = "there's no face visible in this photo"
            elif faces_count == 1:
                context = "there's one person in this photo"
                if age_range:
                    context += f" who appears to be in the {age_range} age range"
            else:
                context = f"there are {faces_count} people in this photo"
            
            prompt = f"""You are a witty roast comedian. Generate a funny, lighthearted roast.
            Context: {context}
            
            Make the roast reference this context naturally. Keep it to 3-5 sentences.
            Be humorous but not mean-spirited."""
        else:
            # Fallback for when no analysis available
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
