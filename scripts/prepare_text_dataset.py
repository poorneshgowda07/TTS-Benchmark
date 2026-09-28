import sys
from pathlib import Path

# Add src to python path
sys.path.append(str(Path(__file__).parent.parent))

from src.benchmark.dataset import DatasetManager

def main():
    manager = DatasetManager()
    
    # 1. Conversational & Agent Personas
    conversational = [
        {"id": manager.get_text_hash("Hi there! How can I help you today?"), "text": "Hi there! How can I help you today?"},
        {"id": manager.get_text_hash("Got it. I'll check that for you right now."), "text": "Got it. I'll check that for you right now."},
        {"id": manager.get_text_hash("Mhm, please go on."), "text": "Mhm, please go on."},
        {"id": manager.get_text_hash("I completely understand your frustration, and I am here to assist you."), "text": "I completely understand your frustration, and I am here to assist you."}
    ]
    
    # 2. Formatting & Normalization
    formatting = [
        {"id": manager.get_text_hash("Please call 1-800-555-0199."), "text": "Please call 1-800-555-0199."},
        {"id": manager.get_text_hash("Your meeting is at 14:30 on 12/10/2026."), "text": "Your meeting is at 14:30 on 12/10/2026."},
        {"id": manager.get_text_hash("Your balance is $4,599.99."), "text": "Your balance is $4,599.99."},
        {"id": manager.get_text_hash("The API returns JSON from the AWS EC2 instance."), "text": "The API returns JSON from the AWS EC2 instance."},
        {"id": manager.get_text_hash("Here are the points: * One * Two 😊"), "text": "Here are the points: * One * Two 😊"}
    ]
    
    # 3. Hinglish & Indian Languages
    hinglish = [
        {"id": manager.get_text_hash("Sir, aapka loan approve ho gaya hai, amount is fifty thousand."), "text": "Sir, aapka loan approve ho gaya hai, amount is fifty thousand."},
        {"id": manager.get_text_hash("Kya aapko credit card features ke baare mein janna hai?"), "text": "Kya aapko credit card features ke baare mein janna hai?"},
        {"id": manager.get_text_hash("Thank you for calling. Aapka din shubh ho."), "text": "Thank you for calling. Aapka din shubh ho."}
    ]
    
    # 4. Emotion
    emotion = [
        {"id": manager.get_text_hash("Are you sure you want to delete this?"), "text": "Are you sure you want to delete this?"},
        {"id": manager.get_text_hash("I am so sorry for the inconvenience caused!"), "text": "I am so sorry for the inconvenience caused!"},
        {"id": manager.get_text_hash("Wow, that is amazing news!"), "text": "Wow, that is amazing news!"}
    ]
    
    manager.save_dataset("conversational", conversational)
    manager.save_dataset("formatting", formatting)
    manager.save_dataset("hinglish", hinglish)
    manager.save_dataset("emotion", emotion)
    
    print("Datasets prepared successfully in data/datasets/")

if __name__ == "__main__":
    main()
