import customtkinter as ctk
import re

def detect_xss(input_string):
    xss_patterns = {
        "Reflected XSS": [
            r'<script[^>]*>.*?</script[^>]*>',
            r'on\w+="[^"]*"',
            r'on\w+=\'[^\']*\'',
            r'javascript:',
            r'eval\((.*?)\)',
            r'expression\((.*?)\)',
            r'translate\((.*?)\)',
            r'background-image:[\s]*url\((.*?)\)',
            r'url\((.*?)\)',
            r'(-moz-|webkit-)?(radial-)?gradient\((.*?)\)',
            r'expression\((.*?)\)',
            r'-moz-binding:\s*url\((.*?)\)',
            r'vbscript:',
            r'\/\*.*?\*\/',
            r'alert\((.*?)\)',
            r'prompt\((.*?)\)',
            r'confirm\((.*?)\)'
        ],
        "Stored XSS": [
            r'<\s*script\s*',
            r'on\w+="[^"]*"',
            r'on\w+=\'[^\']*\'',
            r'javascript:',
            r'eval\((.*?)\)',
            r'expression\((.*?)\)',
            r'translate\((.*?)\)',
            r'background-image:[\s]*url\((.*?)\)',
            r'url\((.*?)\)',
            r'(-moz-|webkit-)?(radial-)?gradient\((.*?)\)',
            r'expression\((.*?)\)',
            r'-moz-binding:\s*url\((.*?)\)',
            r'vbscript:',
            r'\/\*.*?\*\/',
            r'alert\((.*?)\)',
            r'prompt\((.*?)\)',
            r'confirm\((.*?)\)'
        ],
        "DOM-based XSS": [
            r'<script[^>]*>.*?</script[^>]*>',
            r'on\w+="[^"]*"',
            r'on\w+=\'[^\']*\'',
            r'javascript:',
            r'eval\((.*?)\)',
            r'expression\((.*?)\)',
            r'translate\((.*?)\)',
            r'background-image:[\s]*url\((.*?)\)',
            r'url\((.*?)\)',
            r'(-moz-|webkit-)?(radial-)?gradient\((.*?)\)',
            r'expression\((.*?)\)',
            r'-moz-binding:\s*url\((.*?)\)',
            r'vbscript:',
            r'\/\*.*?\*\/',
            r'alert\((.*?)\)',
            r'prompt\((.*?)\)',
            r'confirm\((.*?)\)'
        ]
    }

    results = {}
    for attack_type, patterns in xss_patterns.items():
        for pattern in patterns:
            if re.search(pattern, input_string, re.IGNORECASE):
                results[attack_type] = "Detected"
                break
        else:
            results[attack_type] = "Not Detected"

    return results

def detect_and_show_results():
    input_string = input_entry.get().strip()
    if not input_string:
        ctk.CTkMessagebox.show_warning("Warning", "Please enter a URL or text.")
        return

    # Check if input is a URL or text
    if input_string.startswith("http://") or input_string.startswith("https://"):
        input_type = "URL"
    else:
        input_type = "Text"

    results = detect_xss(input_string)

    # Display results dynamically with colors
    output_text.configure(state="normal")
    output_text.delete("1.0", "end")
    output_text.insert("end", f"Input Type: {input_type}\n", "default")
    output_text.insert("end", "XSS Attack Detection Results:\n\n", "default")
    for attack_type, result in results.items():
        if result == "Detected":
            output_text.insert("end", f"{attack_type}: {result}\n", attack_type.lower())
        else:
            output_text.insert("end", f"{attack_type}: {result}\n", "skyblue")
    output_text.configure(state="disabled")

root = ctk.CTk()
root.title("XSS Attack Detection")
root.geometry("600x400")

# Configure customtkinter theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Styles
style = {
    "background": "#000000",  # Pure black background
    "foreground": "skyblue",  # Skyblue text color
    "detected_foreground": "red",  # Red text color for detected XSS
    "border_color": "#333333",  # Border color for box shadow effect
    "border_width": 1,
    "corner_radius": 10,
    "padding": 10
}

# Input
input_frame = ctk.CTkFrame(root, corner_radius=style["corner_radius"], fg_color=style["background"], border_color=style["border_color"], border_width=style["border_width"])
input_frame.pack(pady=style["padding"], padx=style["padding"], fill="x")
input_label = ctk.CTkLabel(input_frame, text="Enter URL or Text:", anchor="w", text_color=style["foreground"])
input_label.pack(fill="x", padx=style["padding"], pady=5)
input_entry = ctk.CTkEntry(input_frame, width=400, fg_color=style["background"], text_color=style["foreground"], border_color=style["border_color"], border_width=style["border_width"])
input_entry.pack(padx=style["padding"], pady=5)
input_entry.focus()

# Detect Button
detect_button = ctk.CTkButton(root, text="Detect XSS Attacks", command=detect_and_show_results, fg_color=style["background"], text_color=style["foreground"], border_color=style["border_color"], border_width=style["border_width"])
detect_button.pack(pady=5)

# Output
output_frame = ctk.CTkFrame(root, corner_radius=style["corner_radius"], fg_color=style["background"], border_color=style["border_color"], border_width=style["border_width"])
output_frame.pack(pady=style["padding"], padx=style["padding"], fill="both", expand=True)
output_text = ctk.CTkTextbox(output_frame, height=10, wrap="word", corner_radius=style["corner_radius"], fg_color=style["background"], text_color=style["foreground"], border_color=style["border_color"], border_width=style["border_width"])
output_text.pack(padx=style["padding"], pady=style["padding"], fill="both", expand=True)
output_text.tag_config("reflected xss", foreground=style["detected_foreground"])
output_text.tag_config("stored xss", foreground=style["detected_foreground"])
output_text.tag_config("dom-based xss", foreground=style["detected_foreground"])
output_text.tag_config("skyblue", foreground=style["foreground"])  # Define skyblue color tag
output_text.tag_config("default", foreground=style["foreground"])
output_text.configure(state="disabled")

# Exit Button
exit_button = ctk.CTkButton(root, text="Exit", command=root.destroy, fg_color=style["background"], text_color=style["foreground"], border_color=style["border_color"], border_width=style["border_width"])
exit_button.pack(pady=5)

root.mainloop()
