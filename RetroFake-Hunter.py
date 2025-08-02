# =============================================
# IMPORTS SECTION
# =============================================
import tkinter as tk
from tkinter import ttk, messagebox, font
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
import pandas as pd
import numpy as np
import threading
from datetime import datetime
import json


# =============================================
# MAIN APPLICATION CLASS
# =============================================
class RealTimeFakeNewsDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Fake News Detector v1.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize configuration
        self.initialize_config()
        
        # Setup UI
        self.setup_ui()
        
        # Load model in background
        self.load_model_in_background()


# =============================================
# CONFIGURATION SECTION
# =============================================
    def initialize_config(self):
        """Initialize application configuration"""
        # API configuration
        self.news_api_key = "d31d455af75240d888bdbc70b29fdbab"
        self.news_sources = ["bbc-news", "cnn", "reuters", "the-verge", "breitbart-news"]
        
        # Initialize model
        self.vectorizer = None
        self.classifier = None
        self.model_loaded = False


# =============================================
# UI SETUP SECTION
# =============================================
    def setup_ui(self):
        """Setup the main user interface"""
        self.set_win2000_theme()
        self.create_widgets()

    def set_win2000_theme(self):
        """Configure Windows 2000 style theme"""
        self.root.configure(bg='#ece9d8')
        
        # Custom style to mimic Windows 2000
        self.style = ttk.Style()
        self.style.theme_use('default')
        
        # Configure colors and fonts
        self.default_font = ('Tahoma', 8)
        self.title_font = ('Tahoma', 10, 'bold')
        self.button_font = ('Tahoma', 8)
        self.branding_font = ('Tahoma', 10, 'bold')
        
        # Configure styles for various widgets
        self.configure_widget_styles()

    def configure_widget_styles(self):
        """Configure styles for all widgets"""
        # Base style
        self.style.configure('.', 
                           background='#ece9d8', 
                           foreground='#000000',
                           font=self.default_font)
        
        # Frame styles
        self.style.configure('TFrame', background='#ece9d8')
        self.style.configure('TLabel', background='#ece9d8', foreground='#000000')
        
        # Button styles
        self.style.configure('TButton', 
                           background='#ece9d8', 
                           foreground='#000000',
                           font=self.button_font,
                           relief=tk.RAISED,
                           bordercolor='#808080',
                           lightcolor='#ffffff',
                           darkcolor='#808080',
                           padding=2)
        
        self.style.map('TButton',
                      background=[('active', '#316ac5'), ('pressed', '#316ac5')],
                      foreground=[('active', '#ffffff')])
        
        # Notebook (Tab) styles
        self.style.configure('TNotebook', background='#ece9d8', bordercolor='#808080')
        self.style.configure('TNotebook.Tab', 
                           background='#ece9d8', 
                           foreground='#000000',
                           lightcolor='#ffffff',
                           darkcolor='#808080',
                           padding=[5, 2],
                           font=self.default_font)
        
        # Other widget styles
        self.style.configure('TEntry', 
                          fieldbackground='#ffffff', 
                          foreground='#000000',
                          bordercolor='#808080',
                          lightcolor='#ffffff',
                          darkcolor='#808080')
        
        self.style.configure('TScrollbar', 
                          background='#ece9d8',
                          troughcolor='#ece9d8',
                          bordercolor='#808080',
                          arrowcolor='#000000',
                          gripcount=0)
        
        self.style.configure('Treeview', 
                           background='#ffffff',
                           foreground='#000000',
                           fieldbackground='#ffffff',
                           bordercolor='#808080',
                           lightcolor='#ffffff',
                           darkcolor='#808080')
        
        # Branding style
        self.style.configure('Branding.TLabel',
                          background='#ece9d8',
                          foreground='#800000',
                          font=self.branding_font,
                          padding=(10, 5, 10, 5))


# =============================================
# WIDGET CREATION SECTION
# =============================================
    def create_widgets(self):
        """Create all application widgets"""
        self.create_header()
        self.create_tabs()
        self.create_branding()
        self.create_status_bar()

    def create_header(self):
        """Create the header with gradient"""
        header_frame = ttk.Frame(self.root, style='TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.header_canvas = tk.Canvas(header_frame, height=80, bg='#ece9d8', 
                                     highlightthickness=0)
        self.header_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.draw_gradient()
        self.root.bind('<Configure>', self.on_window_resize)

    def create_tabs(self):
        """Create the notebook tabs"""
        self.tab_control = ttk.Notebook(self.root, style='TNotebook')
        
        # Manual Analysis Tab
        self.manual_tab = ttk.Frame(self.tab_control, style='TFrame')
        self.tab_control.add(self.manual_tab, text="Manual Analysis")
        self.create_manual_tab()
        
        # Live News Tab
        self.live_tab = ttk.Frame(self.tab_control, style='TFrame')
        self.tab_control.add(self.live_tab, text="Live News Analysis")
        self.create_live_tab()
        
        self.tab_control.pack(expand=1, fill="both", padx=8, pady=(0, 8))

    def create_branding(self):
        """Create the branding footer"""
        branding_frame = ttk.Frame(self.root, style='TFrame')
        branding_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 2))
        
        separator = ttk.Separator(branding_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=4)
        
        branding_text = "   Made with 💗 by Y7X   "
        branding_label = ttk.Label(
            branding_frame, 
            text=branding_text,
            style='Branding.TLabel'
        )
        branding_label.pack(side=tk.RIGHT, padx=10, pady=5)

    def create_status_bar(self):
        """Create the status bar"""
        self.status_frame = ttk.Frame(self.root, style='TFrame', relief=tk.SUNKEN)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar()
        self.status_var.set(" Loading model... Please wait")
        ttk.Label(self.status_frame, textvariable=self.status_var, 
                anchor='w', style='TLabel').pack(side=tk.LEFT)
        
        # Add resize grip
        grip = ttk.Label(self.status_frame, text="↘", font=('Wingdings', 10))
        grip.pack(side=tk.RIGHT, padx=2)


# =============================================
# TAB CONTENT CREATION SECTION
# =============================================
    def create_manual_tab(self):
        """Create content for manual analysis tab"""
        # Input Section
        input_frame = ttk.LabelFrame(self.manual_tab, text="Enter News Text", padding=6,
                                   style='TLabelframe')
        input_frame.pack(pady=8, padx=8, fill=tk.BOTH, expand=True)
        
        self.text_input = tk.Text(input_frame, height=15, wrap=tk.WORD, 
                                bg='#ffffff', fg='#000000',
                                insertbackground='#000000',
                                selectbackground='#316ac5', selectforeground='#ffffff',
                                relief=tk.SUNKEN, bd=2)
        self.text_input.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.text_input, style='TScrollbar')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_input.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_input.yview)
        
        # Button Section
        button_frame = ttk.Frame(self.manual_tab, style='TFrame')
        button_frame.pack(pady=8, padx=8)
        
        self.analyze_btn = ttk.Button(button_frame, text="Analyze", 
                                    command=self.analyze_text, state=tk.DISABLED,
                                    style='TButton')
        self.analyze_btn.pack(side=tk.LEFT, padx=4)
        
        ttk.Button(button_frame, text="Clear", command=self.clear_text,
                  style='TButton').pack(side=tk.LEFT, padx=4)
        
        # Result Section
        result_frame = ttk.LabelFrame(self.manual_tab, text="Analysis Result", padding=6,
                                     style='TLabelframe')
        result_frame.pack(pady=8, padx=8, fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(result_frame, height=5, wrap=tk.WORD, state=tk.DISABLED,
                                 bg='#ffffff', fg='#000000',
                                 relief=tk.SUNKEN, bd=2)
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def create_live_tab(self):
        """Create content for live news analysis tab"""
        # Source Selection
        source_frame = ttk.LabelFrame(self.live_tab, text="News Sources", padding=6,
                                    style='TLabelframe')
        source_frame.pack(fill=tk.X, padx=8, pady=8)
        
        self.source_vars = []
        for i, source in enumerate(self.news_sources):
            var = tk.BooleanVar(value=True)
            self.source_vars.append(var)
            cb = ttk.Checkbutton(source_frame, text=source, variable=var,
                               style='TCheckbutton')
            cb.grid(row=i//3, column=i%3, sticky="w", padx=8, pady=2)
        
        # Fetch Controls
        fetch_frame = ttk.Frame(self.live_tab, style='TFrame')
        fetch_frame.pack(fill=tk.X, padx=8, pady=8)
        
        ttk.Button(fetch_frame, text="Fetch Latest News", 
                  command=self.fetch_latest_news, style='TButton').pack(side=tk.LEFT, padx=4)
        
        # News Display
        news_frame = ttk.LabelFrame(self.live_tab, text="Latest News", padding=6,
                                  style='TLabelframe')
        news_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        self.news_tree = ttk.Treeview(news_frame, columns=("source", "title", "date", "status"), 
                                     show="headings", height=10, style='Treeview')
        self.news_tree.heading("source", text="Source")
        self.news_tree.heading("title", text="Title")
        self.news_tree.heading("date", text="Date")
        self.news_tree.heading("status", text="Status")
        self.news_tree.column("source", width=100, anchor='w')
        self.news_tree.column("title", width=300, anchor='w')
        self.news_tree.column("date", width=100, anchor='w')
        self.news_tree.column("status", width=100, anchor='w')
        
        scrollbar = ttk.Scrollbar(news_frame, orient="vertical", command=self.news_tree.yview,
                                 style='TScrollbar')
        self.news_tree.configure(yscrollcommand=scrollbar.set)
        
        self.news_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click to analyze
        self.news_tree.bind("<Double-1>", self.analyze_selected_news)
        
        # Analysis Result
        live_result_frame = ttk.LabelFrame(self.live_tab, text="Analysis Result", padding=6,
                                         style='TLabelframe')
        live_result_frame.pack(fill=tk.BOTH, padx=8, pady=8)
        
        self.live_result_text = tk.Text(live_result_frame, height=5, wrap=tk.WORD, state=tk.DISABLED,
                                      bg='#ffffff', fg='#000000',
                                      relief=tk.SUNKEN, bd=2)
        self.live_result_text.pack(fill=tk.BOTH, expand=True)


# =============================================
# UI HELPER METHODS
# =============================================
    def draw_gradient(self):
        """Draw the Windows 2000 style gradient"""
        width = self.header_canvas.winfo_width()
        height = 80
        
        self.header_canvas.delete("all")
        
        if width > 1 and height > 1:
            for i in range(height):
                r = int(236 - (236 - 49) * i / height)
                g = int(233 - (233 - 108) * i / height)
                b = int(216 - (216 - 197) * i / height)
                color = f'#{r:02x}{g:02x}{b:02x}'
                self.header_canvas.create_line(0, i, width, i, fill=color)
            
            # Add title
            self.header_canvas.create_text(10, height//2, anchor='w', 
                                         text="Real-Time Fake News Detector v1.0",
                                         font=('Tahoma', 14, 'bold'), fill='#000080')
            
            # Add logo
            self.header_canvas.create_text(width-20, height//2, anchor='e', text="☯", 
                                         font=('Wingdings', 18), fill='#000080')

    def on_window_resize(self, event):
        """Handle window resize events"""
        if event.widget == self.root:
            self.draw_gradient()


# =============================================
# MODEL HANDLING SECTION
# =============================================
    def load_model_in_background(self):
        """Load the ML model in a background thread"""
        def load_model():
            try:
                data = {
                    'text': [
                        "Scientists confirm climate change is accelerating",
                        "Study shows vaccines are safe and effective",
                        "5G towers are causing COVID-19 outbreaks",
                        "Government secretly controlling weather",
                        "New economic policy shows positive results",
                        "Celebrity death hoax spreads on social media"
                    ],
                    'label': [1, 1, 0, 0, 1, 0]
                }
                
                df = pd.DataFrame(data)
                
                self.vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
                X = self.vectorizer.fit_transform(df['text'])
                
                self.classifier = PassiveAggressiveClassifier(max_iter=50)
                self.classifier.fit(X, df['label'])
                
                self.model_loaded = True
                self.status_var.set(" Ready")
                self.analyze_btn.config(state=tk.NORMAL)
                
            except Exception as e:
                self.status_var.set(f" Error: {str(e)}")
                messagebox.showerror("Error", f"Failed to load model: {str(e)}", icon='error')
        
        threading.Thread(target=load_model, daemon=True).start()


# =============================================
# NEWS FETCHING SECTION
# =============================================
    def fetch_latest_news(self):
        """Fetch latest news from selected sources"""
        if not all([self.model_loaded, self.news_api_key != "YOUR_NEWSAPI_KEY"]):
            messagebox.showwarning("Warning", "Please configure your NewsAPI key first", icon='warning')
            return
        
        selected_sources = [source for source, var in zip(self.news_sources, self.source_vars) if var.get()]
        if not selected_sources:
            messagebox.showwarning("Warning", "Please select at least one news source", icon='warning')
            return
        
        self.status_var.set(" Fetching latest news...")
        
        def fetch_thread():
            try:
                url = f"https://newsapi.org/v2/top-headlines?sources={','.join(selected_sources)}&apiKey={self.news_api_key}"
                response = requests.get(url)
                data = response.json()
                
                if data['status'] != 'ok':
                    raise ValueError(data.get('message', 'Unknown error from NewsAPI'))
                
                self.news_tree.delete(*self.news_tree.get_children())
                
                for article in data['articles']:
                    source = article['source']['name']
                    title = article['title']
                    date = article['publishedAt'][:10]
                    self.news_tree.insert("", "end", values=(source, title, date, "Not analyzed"), 
                                         tags=("unanalyzed",))
                
                self.news_tree.tag_configure("unanalyzed", foreground="#000000")
                self.news_tree.tag_configure("real", foreground="#000080")
                self.news_tree.tag_configure("fake", foreground="#800000")
                
                self.status_var.set(f" Fetched {len(data['articles'])} articles")
                
            except Exception as e:
                self.status_var.set(f" Error: {str(e)}")
                messagebox.showerror("Error", f"Failed to fetch news: {str(e)}", icon='error')
        
        threading.Thread(target=fetch_thread, daemon=True).start()


# =============================================
# ANALYSIS SECTION
# =============================================
    def analyze_selected_news(self, event):
        """Analyze the selected news item"""
        selected_item = self.news_tree.selection()
        if not selected_item:
            return
        
        item_data = self.news_tree.item(selected_item)
        title = item_data['values'][1]
        
        self.live_result_text.config(state=tk.NORMAL)
        self.live_result_text.delete("1.0", tk.END)
        self.live_result_text.insert(tk.END, f"Analyzing: {title}\n\n")
        
        try:
            text_vectorized = self.vectorizer.transform([title])
            prediction = self.classifier.predict(text_vectorized)
            prediction_proba = self.classifier._predict_proba_lr(text_vectorized)
            confidence = np.max(prediction_proba) * 100
            
            if prediction[0] == 1:
                result = "REAL NEWS"
                color = "#000080"
                tag = "real"
            else:
                result = "FAKE NEWS"
                color = "#800000"
                tag = "fake"
            
            self.live_result_text.insert(tk.END, f"Prediction: {result}\n", ("bold", color))
            self.live_result_text.insert(tk.END, f"Confidence: {confidence:.2f}%\n\n")
            
            self.live_result_text.insert(tk.END, "Analysis:\n")
            if any(word in title.lower() for word in ["urgent", "breaking", "shocking", "unbelievable"]):
                self.live_result_text.insert(tk.END, "- Uses sensational language (common in fake news)\n")
            if len(title.split()) > 15:
                self.live_result_text.insert(tk.END, "- Long headline (more likely to be real news)\n")
            
            self.news_tree.item(selected_item, values=(
                item_data['values'][0],
                item_data['values'][1],
                item_data['values'][2],
                result
            ), tags=(tag,))
            
            self.live_result_text.tag_config("bold", font=('Tahoma', 8, 'bold'))
            self.live_result_text.tag_config("blue", foreground="#000080")
            self.live_result_text.tag_config("red", foreground="#800000")
            
        except Exception as e:
            self.live_result_text.insert(tk.END, f"Error: {str(e)}", "red")
        
        self.live_result_text.config(state=tk.DISABLED)

    def analyze_text(self):
        """Analyze manually entered text"""
        if not self.model_loaded:
            messagebox.showwarning("Warning", "Model is still loading. Please wait.", icon='warning')
            return
        
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to analyze.", icon='warning')
            return
        
        try:
            text_vectorized = self.vectorizer.transform([text])
            
            prediction = self.classifier.predict(text_vectorized)
            prediction_proba = self.classifier._predict_proba_lr(text_vectorized)
            confidence = np.max(prediction_proba) * 100
            
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)
            
            if prediction[0] == 1:
                result = "REAL NEWS"
                color = "#000080"
            else:
                result = "FAKE NEWS"
                color = "#800000"
            
            self.result_text.insert(tk.END, f"Prediction: {result}\n", ("bold", color))
            self.result_text.insert(tk.END, f"Confidence: {confidence:.2f}%\n\n")
            
            self.result_text.insert(tk.END, "Analysis:\n")
            if "http" in text.lower() or ".com" in text.lower():
                self.result_text.insert(tk.END, "- Contains links (verify source reliability)\n")
            if any(word in text.lower() for word in ["urgent", "breaking", "shocking"]):
                self.result_text.insert(tk.END, "- Uses sensational language (common in fake news)\n")
            if len(text.split()) > 300:
                self.result_text.insert(tk.END, "- Detailed article (more likely to be real news)\n")
            
            self.result_text.tag_config("bold", font=('Tahoma', 8, 'bold'))
            self.result_text.tag_config("blue", foreground="#000080")
            self.result_text.tag_config("red", foreground="#800000")
            self.result_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}", icon='error')


# =============================================
# UTILITY METHODS
# =============================================
    def clear_text(self):
        """Clear the manual analysis text fields"""
        self.text_input.delete("1.0", tk.END)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state=tk.DISABLED)


# =============================================
# MAIN ENTRY POINT
# =============================================
if __name__ == "__main__":
    root = tk.Tk()
    
    # Set classic Windows 2000 icon
    try:
        root.iconbitmap(default='system.ico')
    except:
        pass
    
    app = RealTimeFakeNewsDetector(root)
    root.mainloop()