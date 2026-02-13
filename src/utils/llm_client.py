import os
from groq import Groq
from config.settings import GROQ_API_KEY, GROQ_MODEL, TEMPERATURE, MAX_TOKENS

class GroqClient:
    """Wrapper for Groq API interactions"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GroqClient, cls).__new__(cls)
            cls._instance.client = Groq(api_key=GROQ_API_KEY)
        return cls._instance
    
    def generate(self, prompt, system_message="You are a helpful assistant."):
        """
        Generates a response from Groq API with automatic failover for rate limits.
        """
        from config.settings import GROQ_FALLBACK_MODELS
        models_to_try = [GROQ_MODEL] + GROQ_FALLBACK_MODELS
        
        last_error = None
        
        for model in models_to_try:
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt}
                    ],
                    model=model,
                    temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS,
                )
                return chat_completion.choices[0].message.content
            except Exception as e:
                last_error = e
                err_msg = str(e).lower()
                
                # Triggers for failover to next model
                failover_triggers = [
                    "rate_limit", 
                    "429", 
                    "decommissioned", 
                    "not_found", 
                    "model_not_found",
                    "503",
                    "service_unavailable"
                ]
                
                found_trigger = next((t for t in failover_triggers if t in err_msg), "error")
                
                if any(trigger in err_msg for trigger in failover_triggers):
                    print(f"⚠️ Failover trigger detected on {model}: {found_trigger}. Trying next fallback...")
                    continue
                
                # For other errors, log and return
                print(f"❌ Groq API Error on {model}: {e}")
                break
                
        return f"ERROR_LLM_GEN_FAILED: {last_error}"

if __name__ == "__main__":
    # verification
    try:
        client = GroqClient()
        print("Testing connection...")
        response = client.generate("Say 'Hello, World!' if you can hear me.")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Failed to connect: {e}")
