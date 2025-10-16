import qrcode
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser, simpledialog
from PIL import Image, ImageTk, ImageOps, ImageDraw
import re
import webbrowser
import json
import os
from datetime import datetime
import logging
import sys

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced QR Code Generator - Free & Open Source")
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        # Setup logging
        self.setup_logging()
        
        self.bg_color = "#f0f0f0"
        self.root.config(bg=self.bg_color)
        
        # Customization variables
        self.qr_fg_color = "black"
        self.qr_bg_color = "white"
        self.logo_path = None
        self.history = []
        self.history_file = "qr_history.json"
        
        self.logger.info("QR Code Generator started")
        
        # Load history
        self.load_history()

        # Create main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.generator_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)
        self.history_frame = ttk.Frame(self.notebook)
        self.debug_frame = ttk.Frame(self.notebook)
        self.about_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.generator_frame, text="🎯 Generator")
        self.notebook.add(self.settings_frame, text="🎨 Customize")
        self.notebook.add(self.history_frame, text="📚 History")
        self.notebook.add(self.debug_frame, text="🐛 Debug")
        self.notebook.add(self.about_frame, text="ℹ️ About")

        self.setup_generator_tab()
        self.setup_settings_tab()
        self.setup_history_tab()
        self.setup_debug_tab()
        self.setup_about_tab()

    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('qr_generator.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_about_tab(self):
        """Setup about tab with project information"""
        about_text = """
🚀 Advanced QR Code Generator

Version: 1.0.0
License: MIT - Free and Open Source

✨ Features:
• Multiple QR code types (Website, Email, Phone, WiFi, vCard, Text)
• Custom colors and logo support
• Batch QR code generation
• History tracking
• Real-time debugging

🛠️ Built With:
• Python 3
• Tkinter (GUI)
• QRCode library
• Pillow (Image processing)

📖 How to Use:
1. Select QR type in Generator tab
2. Enter your content
3. Customize appearance in Settings
4. Generate and save your QR code!

🤝 Contributing:
This is open source! Feel free to:
• Report issues
• Suggest features
• Submit pull requests
• Share with others

📄 License:
MIT License - Free to use, modify, and distribute

Developed with ❤️ for the community
        """
        
        about_label = tk.Label(self.about_frame, text=about_text, justify=tk.LEFT, 
                              font=("Arial", 11), padx=20, pady=20)
        about_label.pack(fill=tk.BOTH, expand=True)

        # GitHub button
        github_btn = tk.Button(self.about_frame, text="⭐ Star on GitHub", 
                              command=lambda: webbrowser.open("https://github.com"),
                              bg="#2d3748", fg="white", font=("Arial", 12, "bold"),
                              padx=20, pady=10)
        github_btn.pack(pady=10)

    def setup_debug_tab(self):
        """Setup debug console"""
        console_frame = ttk.Frame(self.debug_frame)
        console_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.console_text = tk.Text(console_frame, height=15, bg='black', fg='lightgreen', 
                                   font=('Consolas', 9), wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(console_frame, orient=tk.VERTICAL, command=self.console_text.yview)
        self.console_text.configure(yscrollcommand=scrollbar.set)
        
        self.console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Control buttons
        btn_frame = ttk.Frame(self.debug_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(btn_frame, text="Clear Console", command=self.clear_console).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Test Domain Detection", command=self.test_domain_detection).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Show System Info", command=self.show_system_info).pack(side=tk.LEFT, padx=2)

        self.redirect_stdout()

    def redirect_stdout(self):
        """Redirect stdout to console"""
        class ConsoleRedirector:
            def __init__(self, text_widget):
                self.text_widget = text_widget
            def write(self, message):
                self.text_widget.insert(tk.END, message)
                self.text_widget.see(tk.END)
            def flush(self):
                pass
        sys.stdout = ConsoleRedirector(self.console_text)

    def clear_console(self):
        self.console_text.delete(1.0, tk.END)

    def show_system_info(self):
        """Show system information"""
        import platform
        print(f"\n=== SYSTEM INFORMATION ===")
        print(f"Python: {sys.version}")
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Tkinter: {tk.TkVersion}")
        print(f"Current Directory: {os.getcwd()}")

    def test_domain_detection(self):
        """Test domain detection"""
        test_inputs = ["playerkomona.top", "google.com", "test.org", "ac.ke", "example.com"]
        print("\n=== DOMAIN DETECTION TEST ===")
        for test_input in test_inputs:
            result, input_type = self.detect_input_type(test_input)
            print(f"'{test_input}' -> {input_type}: {result}")

    def setup_generator_tab(self):
        # Header
        header_frame = tk.Frame(self.generator_frame, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=10)
        
        title = tk.Label(header_frame, text="🎯 QR Code Generator", 
                        font=("Arial", 18, "bold"), bg=self.bg_color, fg="#2d3748")
        title.pack()

        subtitle = tk.Label(header_frame, text="Create custom QR codes for free!", 
                           font=("Arial", 11), bg=self.bg_color, fg="#666")
        subtitle.pack()

        # Input section
        input_frame = tk.LabelFrame(self.generator_frame, text="QR Code Content", 
                                   font=("Arial", 11, "bold"), padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # QR Type selection
        type_frame = tk.Frame(input_frame, bg=self.bg_color)
        type_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(type_frame, text="Type:", font=("Arial", 10), 
                bg=self.bg_color).pack(side=tk.LEFT)
        
        self.qr_type = tk.StringVar(value="website")
        types = [("Website", "website"), ("Email", "email"), ("Phone", "phone"), 
                ("Text", "text"), ("WiFi", "wifi"), ("vCard", "vcard")]
        
        for text, mode in types:
            tk.Radiobutton(type_frame, text=text, variable=self.qr_type, 
                          value=mode, bg=self.bg_color, command=self.on_type_change).pack(side=tk.LEFT, padx=5)

        # Main input field
        self.input_field = tk.Entry(input_frame, font=("Arial", 12), relief=tk.GROOVE, bd=2)
        self.input_field.pack(fill=tk.X, pady=10, ipady=5)
        self.input_field.bind("<Return>", lambda e: self.generate())
        self.input_field.insert(0, "https://github.com")

        # Specialized input frames
        self.setup_special_frames(input_frame)

        # Action buttons
        self.setup_action_buttons()

        # QR Display
        self.setup_qr_display()

        self.on_type_change()

    def setup_special_frames(self, parent):
        """Setup specialized input frames"""
        # WiFi frame
        self.wifi_frame = tk.Frame(parent, bg=self.bg_color)
        tk.Label(self.wifi_frame, text="SSID:", bg=self.bg_color, font=("Arial", 10)).pack(side=tk.LEFT)
        self.ssid_entry = tk.Entry(self.wifi_frame, font=("Arial", 10), width=20)
        self.ssid_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(self.wifi_frame, text="Password:", bg=self.bg_color, font=("Arial", 10)).pack(side=tk.LEFT, padx=(10,0))
        self.password_entry = tk.Entry(self.wifi_frame, font=("Arial", 10), width=15, show="*")
        self.password_entry.pack(side=tk.LEFT)

        # vCard frame
        self.vcard_frame = tk.Frame(parent, bg=self.bg_color)
        tk.Label(self.vcard_frame, text="Name:", bg=self.bg_color, font=("Arial", 10)).pack(side=tk.LEFT)
        self.vcard_name = tk.Entry(self.vcard_frame, font=("Arial", 10), width=15)
        self.vcard_name.pack(side=tk.LEFT, padx=2)
        tk.Label(self.vcard_frame, text="Phone:", bg=self.bg_color, font=("Arial", 10)).pack(side=tk.LEFT, padx=(5,0))
        self.vcard_phone = tk.Entry(self.vcard_frame, font=("Arial", 10), width=15)
        self.vcard_phone.pack(side=tk.LEFT, padx=2)
        tk.Label(self.vcard_frame, text="Email:", bg=self.bg_color, font=("Arial", 10)).pack(side=tk.LEFT, padx=(5,0))
        self.vcard_email = tk.Entry(self.vcard_frame, font=("Arial", 10), width=20)
        self.vcard_email.pack(side=tk.LEFT, padx=2)

    def setup_action_buttons(self):
        """Setup action buttons"""
        btn_frame = tk.Frame(self.generator_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)

        buttons = [
            ("🚀 Generate QR", self.generate, "#4CAF50"),
            ("💾 Save QR", self.save_qr_code, "#2196F3"),
            ("🖼️ Add Logo", self.choose_logo, "#FF9800"),
            ("🔁 Batch Generate", self.batch_generate, "#9C27B0"),
        ]

        for text, command, color in buttons:
            btn = tk.Button(btn_frame, text=text, command=command, font=("Arial", 10, "bold"),
                          bg=color, fg="white", padx=15, pady=8, relief=tk.RAISED, bd=2)
            btn.pack(side=tk.LEFT, padx=3)

        self.info_label = tk.Label(self.generator_frame, text="Ready to generate QR codes!", 
                                  font=("Arial", 10), bg=self.bg_color, fg="#666")
        self.info_label.pack(pady=5)

    def setup_qr_display(self):
        """Setup QR code display area"""
        display_frame = tk.LabelFrame(self.generator_frame, text="QR Code Preview", 
                                     font=("Arial", 11, "bold"), padx=10, pady=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.qr_frame = tk.Frame(display_frame, bg="white", relief=tk.SUNKEN, bd=1)
        self.qr_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.qr_label = tk.Label(self.qr_frame, bg="white", 
                                text="Your QR code will appear here\n\nSelect type, enter content, and click 'Generate QR'", 
                                font=("Arial", 11), wraplength=400, justify=tk.CENTER)
        self.qr_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=20)

    def setup_settings_tab(self):
        """Setup customization settings"""
        # Colors
        color_frame = tk.LabelFrame(self.settings_frame, text="🎨 Colors", 
                                   font=("Arial", 11, "bold"), padx=10, pady=10)
        color_frame.pack(fill=tk.X, padx=10, pady=5)

        self.fg_btn = tk.Button(color_frame, text="QR Color", command=self.choose_fg_color,
                 bg=self.qr_fg_color, fg="white", font=("Arial", 10), padx=15, pady=5)
        self.fg_btn.pack(side=tk.LEFT, padx=5)
        
        self.bg_btn = tk.Button(color_frame, text="Background", command=self.choose_bg_color,
                 bg=self.qr_bg_color, fg="black", font=("Arial", 10), padx=15, pady=5)
        self.bg_btn.pack(side=tk.LEFT, padx=5)

        # Logo settings
        logo_frame = tk.LabelFrame(self.settings_frame, text="🖼️ Logo Settings", 
                                  font=("Arial", 11, "bold"), padx=10, pady=10)
        logo_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(logo_frame, text="Logo Size (%):", font=("Arial", 10)).pack(side=tk.LEFT)
        self.logo_size = tk.IntVar(value=25)
        tk.Scale(logo_frame, from_=10, to=40, variable=self.logo_size, 
                orient=tk.HORIZONTAL, length=150).pack(side=tk.LEFT, padx=10)

        self.logo_status = tk.Label(logo_frame, text="No logo selected", font=("Arial", 9), fg="gray")
        self.logo_status.pack(pady=5)

    def setup_history_tab(self):
        """Setup history tab"""
        controls = tk.Frame(self.history_frame)
        controls.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(controls, text="Load Selected", command=self.load_from_history, 
                 font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        tk.Button(controls, text="Clear History", command=self.clear_history,
                 font=("Arial", 9)).pack(side=tk.LEFT, padx=2)

        self.history_listbox = tk.Listbox(self.history_frame, font=("Arial", 10))
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.refresh_history()

    # ... (Keep all your existing methods from the previous version: 
    # on_type_change, choose_fg_color, choose_bg_color, detect_input_type, 
    # generate, save_to_history, load_history, save_history, refresh_history,
    # load_from_history, clear_history, batch_generate, choose_logo, save_qr_code)
    # These remain exactly the same as in the previous working version

    def detect_input_type(self, user_input):
        user_input = user_input.strip()
        original_input = user_input

        domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$'
        if re.match(domain_pattern, user_input, re.IGNORECASE) and ' ' not in user_input:
            return f"https://{user_input}", "website"

        if user_input.startswith(('http://', 'https://')):
            return user_input, "website"

        if user_input.startswith('www.'):
            return f"https://{user_input}", "website"

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, user_input, re.IGNORECASE):
            return f"mailto:{user_input}", "email"

        phone_pattern = r'^[\+]?[0-9\s\-\(\)]{10,}$'
        clean_phone = re.sub(r'[\s\-\(\)]', '', user_input)
        if re.match(phone_pattern, user_input) and len(clean_phone) >= 10:
            return f"tel:{clean_phone}", "phone"

        if user_input.startswith('@'):
            handle = user_input[1:]
            return f"https://instagram.com/{handle}", "social media"

        return original_input, "text"

    def generate(self):
        qr_type = self.qr_type.get()
        
        if qr_type == "wifi":
            ssid = self.ssid_entry.get().strip()
            password = self.password_entry.get().strip()
            if not ssid:
                messagebox.showwarning("Input Required", "Please enter WiFi SSID")
                return
            data = f"WIFI:S:{ssid};T:WPA;P:{password};;"
            input_type = "wifi"
            
        elif qr_type == "vcard":
            name = self.vcard_name.get().strip()
            phone = self.vcard_phone.get().strip()
            email = self.vcard_email.get().strip()
            if not name:
                messagebox.showwarning("Input Required", "Please enter name for vCard")
                return
            data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"
            input_type = "vcard"
            
        else:
            user_input = self.input_field.get().strip()
            if not user_input:
                messagebox.showwarning("Input Required", "Please enter content for QR code")
                return
            data, input_type = self.detect_input_type(user_input)

        try:
            self.current_qr_data = data
            display_data = data if len(data) < 60 else data[:57] + "..."
            self.info_label.config(text=f"Type: {input_type.title()} | Content: {display_data}", fg="#4CAF50")

            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color=self.qr_fg_color, back_color=self.qr_bg_color).convert("RGB")

            if self.logo_path:
                try:
                    logo = Image.open(self.logo_path)
                    logo_size = min(img.size) * self.logo_size.get() // 100
                    logo = ImageOps.contain(logo, (logo_size, logo_size))
                    
                    mask = Image.new('L', logo.size, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)
                    
                    pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
                    img.paste(logo, pos, mask=mask)
                except Exception as e:
                    print(f"Logo error: {e}")

            img_display = img.copy()
            img_display.thumbnail((350, 350), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img_display)

            self.qr_label.config(image=photo, text="")
            self.qr_label.image = photo
            self.current_qr_image = img
            
            self.save_to_history(data, input_type)
            print(f"✓ Generated {input_type} QR code")

        except Exception as e:
            error_msg = f"Error generating QR code: {e}"
            print(f"✗ {error_msg}")
            messagebox.showerror("Error", error_msg)
            self.info_label.config(text="Error generating QR code", fg="#f44336")

    def save_to_history(self, data, qr_type):
        history_item = {
            "data": data,
            "type": qr_type,
            "timestamp": datetime.now().isoformat()
        }
        self.history.insert(0, history_item)
        self.history = self.history[:10]
        self.save_history()
        self.refresh_history()

    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
        except:
            self.history = []

    def save_history(self):
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except:
            pass

    def refresh_history(self):
        self.history_listbox.delete(0, tk.END)
        for i, item in enumerate(self.history):
            display_text = f"{i+1}. {item['type']}: {item['data'][:40]}..."
            self.history_listbox.insert(tk.END, display_text)

    def load_from_history(self):
        selection = self.history_listbox.curselection()
        if selection:
            item = self.history[selection[0]]
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, item['data'])
            self.notebook.select(0)

    def clear_history(self):
        self.history = []
        self.save_history()
        self.refresh_history()

    def batch_generate(self):
        text = simpledialog.askstring("Batch Generate", "Enter multiple items (one per line):")
        if text:
            items = [item.strip() for item in text.split('\n') if item.strip()]
            folder = filedialog.askdirectory(title="Select folder to save batch QR codes")
            if folder:
                success_count = 0
                for i, item in enumerate(items):
                    try:
                        data, input_type = self.detect_input_type(item)
                        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H)
                        qr.add_data(data)
                        qr.make(fit=True)
                        img = qr.make_image(fill_color=self.qr_fg_color, back_color=self.qr_bg_color)
                        filename = f"qr_batch_{i+1:02d}.png"
                        img.save(os.path.join(folder, filename))
                        success_count += 1
                    except Exception as e:
                        print(f"Batch error for '{item}': {e}")
                messagebox.showinfo("Batch Complete", f"Generated {success_count} QR codes!")

    def choose_logo(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")],
            title="Select Logo"
        )
        if path:
            self.logo_path = path
            self.logo_status.config(text=f"Logo: {os.path.basename(path)}", fg="green")

    def save_qr_code(self):
        if not self.current_qr_image:
            messagebox.showwarning("No QR Code", "Please generate a QR code first")
            return

        try:
            if self.current_qr_data.startswith(('http://', 'https://')):
                domain = self.current_qr_data.replace('https://', '').replace('http://', '').split('/')[0]
                default_name = f"qrcode_{domain}.png"
            else:
                default_name = "qrcode.png"

            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Save QR Code",
                initialfile=default_name
            )

            if filename:
                self.current_qr_image.save(filename)
                messagebox.showinfo("Success", f"QR code saved as:\n{filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Error saving QR code: {e}")

    def on_type_change(self):
        qr_type = self.qr_type.get()
        self.wifi_frame.pack_forget()
        self.vcard_frame.pack_forget()
        
        if qr_type == "website":
            self.input_field.pack(fill=tk.X, pady=10, ipady=5)
            self.input_field.config(show="")
        elif qr_type == "wifi":
            self.input_field.pack_forget()
            self.wifi_frame.pack(fill=tk.X, pady=10)
            self.ssid_entry.focus()
        elif qr_type == "vcard":
            self.input_field.pack_forget()
            self.vcard_frame.pack(fill=tk.X, pady=10)
            self.vcard_name.focus()
        else:
            self.input_field.pack(fill=tk.X, pady=10, ipady=5)
            self.input_field.config(show="")

    def choose_fg_color(self):
        color = colorchooser.askcolor(title="Choose QR Code Color", initialcolor=self.qr_fg_color)[1]
        if color:
            self.qr_fg_color = color
            self.fg_btn.config(bg=color, fg="white" if color == "black" else "black")

    def choose_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color", initialcolor=self.qr_bg_color)[1]
        if color:
            self.qr_bg_color = color
            self.bg_btn.config(bg=color, fg="black" if color == "white" else "white")

def main():
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
