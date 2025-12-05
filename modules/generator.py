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
            gender = analysis_data.get('gender', None)
            is_smiling = analysis_data.get('is_smiling', None)
            
            if faces_count == 0:
                context = "there's no face visible in this photo"
            elif faces_count == 1:
                context = "there's one person in this photo"
                if gender:
                    context += f" who appears to be {gender}"
                if age_range:
                    context += f" in the {age_range} age range"
                if is_smiling is not None:
                    if is_smiling:
                        context += ", and they're smiling"
                    else:
                        context += ", and they're not smiling"
            else:
                context = f"there are {faces_count} people in this photo"            
            prompt = f"""You are writing comedy roast material for adults. Using these details: {context}

Here are examples of the roast style I want:
- "Jesus fucking Christ, you look like you'd lose a fight with a steep incline. Your body has the same energy as a participation trophy that someone tried to return."
- "You have the charisma of a wet fart in an elevator. Seriously, your personality is so bland it makes unseasoned chicken breast seem exciting as fuck."
- "Your face looks like God hit 'randomize' and then said 'fuck it, good enough.' You're what happens when the gene pool needs more chlorine."
- "You dress like a blind person having a mental breakdown at a Goodwill. Your outfit screams 'I've given up' louder than your dating profile ever could."
- "Looking at you is like watching someone fail in slow motion. You have the confidence of someone who's never looked in a mirror and the appearance of someone who definitely should."

Now create an absolutely savage roast (3-5 sentences) using the context provided. Use profanity freely. Be brutally honest, creatively insulting, and pull absolutely no punches. This is consensual roast comedy - go ALL OUT."""
        else:
            # Fallback for when no analysis available
            prompt = """You are writing comedy roast material for adults.

Here are examples of the roast style I want:
- "You look like disappointment became a person and then gave up halfway through. Your vibe is 'gave up on life before life gave up on you.'"
- "Holy shit, your personality is so boring it makes watching paint dry seem like a fucking thrill ride."
- "You have the fashion sense of someone who shops exclusively from 'clothes I found on the floor.' Tragic doesn't even begin to cover it."
- "Your face looks like someone described 'average' to an AI and it glitched halfway through. Nature really said 'fuck this guy in particular.'"

Now create an absolutely savage roast (3-5 sentences). Use profanity freely. Be brutally honest and creatively insulting. This is consensual roast comedy - go ALL OUT."""
        
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
