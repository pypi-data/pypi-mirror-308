import random

# @hint: pyfiglet (channel=pypi)
from pyfiglet import Figlet
# @hint: gradio (channel=pypi, version=3.20.1)
import gradio as gr

def generate_random_sentence(words_count=5):
    """Generate a random sentence with a specified number of words."""
    words = [
        "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog",
        "cat", "hat", "sun", "moon", "star", "sky", "sea", "land"
    ]
    sentence = ' '.join(random.choices(words, k=words_count))
    return sentence.capitalize() + '.'

def text_to_ascii(text, font="slant"):
    """Convert text to ASCII art using a specified font."""
    figlet = Figlet(font=font)
    ascii_art = figlet.renderText(text)
    return ascii_art

def reverse_text(text):
    """Reverse the given text."""
    return text[::-1]

def shuffle_text(text):
    """Shuffle the characters in the text randomly."""
    char_list = list(text)
    random.shuffle(char_list)
    return ''.join(char_list)

def default(action="generate_sentence", **kwargs):
    """
    Default entry point for the library.
    
    Parameters:
        action (str): The action to perform. Options include:
                      - 'generate_sentence': Generate a random sentence.
                      - 'text_to_ascii': Convert text to ASCII art.
                      - 'reverse_text': Reverse the given text.
                      - 'shuffle_text': Shuffle the characters in the text.
        
        kwargs: Additional keyword arguments for the chosen action.
    """
    if action == "generate_sentence":
        return generate_random_sentence(**kwargs)
    elif action == "text_to_ascii":
        return text_to_ascii(**kwargs)
    elif action == "reverse_text":
        return reverse_text(kwargs.get("text", ""))
    elif action == "shuffle_text":
        return shuffle_text(kwargs.get("text", ""))
    else:
        raise ValueError(f"Unknown action: {action}")

def create_gradio_interface():
    """Create a Gradio interface for the library."""
    with gr.Blocks() as demo:
        with gr.Tabs():
            with gr.TabItem("Generate Random Sentence"):
                words_count = gr.Slider(1, 20, value=5, label="Number of Words")
                generate_sentence_output = gr.Textbox(label="Generated Sentence")
                generate_sentence_button = gr.Button("Generate")
                generate_sentence_button.click(
                    fn=lambda wc: default(action="generate_sentence", words_count=int(wc)),
                    inputs=words_count,
                    outputs=generate_sentence_output
                )
            
            with gr.TabItem("Text to ASCII Art"):
                text_input_ascii = gr.Textbox(label="Enter Text")
                font_choice = gr.Dropdown(["slant", "3-d", "5lineoblique", "alphabet"], value="slant", label="Font")
                ascii_art_output = gr.Textbox(label="ASCII Art", lines=20)
                ascii_art_button = gr.Button("Convert")
                ascii_art_button.click(
                    fn=lambda t, f: default(action="text_to_ascii", text=t, font=f),
                    inputs=[text_input_ascii, font_choice],
                    outputs=ascii_art_output
                )
            
            with gr.TabItem("Reverse Text"):
                text_input_reverse = gr.Textbox(label="Enter Text")
                reverse_text_output = gr.Textbox(label="Reversed Text")
                reverse_button = gr.Button("Reverse")
                reverse_button.click(
                    fn=lambda t: default(action="reverse_text", text=t),
                    inputs=text_input_reverse,
                    outputs=reverse_text_output
                )
            
            with gr.TabItem("Shuffle Text"):
                text_input_shuffle = gr.Textbox(label="Enter Text")
                shuffle_text_output = gr.Textbox(label="Shuffled Text")
                shuffle_button = gr.Button("Shuffle")
                shuffle_button.click(
                    fn=lambda t: default(action="shuffle_text", text=t),
                    inputs=text_input_shuffle,
                    outputs=shuffle_text_output
                )
    
    demo.launch()

# Uncomment the line below to run the Gradio interface when this script is executed.
# create_gradio_interface()
