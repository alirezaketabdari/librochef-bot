"""
Simple web server to host the beautiful language selection page
Run this alongside your bot to serve the HTML interface
"""

from flask import Flask, render_template_string
import os

app = Flask(__name__)

@app.route('/welcome')
def welcome_page():
    """Serve the beautiful language selection page"""
    try:
        with open('templates/welcome.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return """
        <h1>Welcome to LibroChef Bot</h1>
        <p>Language selection page not found. Please ensure templates/welcome.html exists.</p>
        """

@app.route('/')
def index():
    """Simple index page"""
    return """
    <h1>LibroChef Bot Web Interface</h1>
    <p>Visit <a href="/welcome">/welcome</a> for the language selection page.</p>
    """

if __name__ == '__main__':
    print("🌐 Starting web server for LibroChef Bot...")
    print("📱 Language selection page will be available at: http://localhost:5000/welcome")
    print("🔗 Use this URL in your Telegram Web App configuration")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
