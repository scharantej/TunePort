
# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Initialize Flask application
app = Flask(__name__)

# Database connection
conn = sqlite3.connect('music_store.db')
c = conn.cursor()

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Music catalog route
@app.route('/music_catalog')
def music_catalog():
    albums = c.execute('SELECT * FROM albums').fetchall()
    return render_template('music_catalog.html', albums=albums)

# Buy now route
@app.route('/buy_now/<int:album_id>')
def buy_now(album_id):
    album = c.execute('SELECT * FROM albums WHERE album_id=?', (album_id,)).fetchone()
    return render_template('buy_now.html', album=album)

# Process purchase route
@app.route('/process_purchase', methods=['POST'])
def process_purchase():
    data = request.form
    album_id = data['album_id']
    name = data['name']
    card_number = data['card_number']
    exp_date = data['exp_date']
    cvv = data['cvv']
    # Payment processing logic goes here
    # After successful payment, generate download link and save transaction details
    download_link = 'http://example.com/download/' + album_id
    c.execute('INSERT INTO purchases (album_id, customer_name, download_link) VALUES (?, ?, ?)',
              (album_id, name, download_link))
    conn.commit()
    return redirect(url_for('confirmation', album_id=album_id))

# Confirmation route
@app.route('/confirmation/<int:album_id>')
def confirmation(album_id):
    download_link = c.execute('SELECT download_link FROM purchases WHERE album_id=?', (album_id,)).fetchone()[0]
    return render_template('confirmation.html', download_link=download_link)

# Download music route
@app.route('/download_music/<int:album_id>')
def download_music(album_id):
    # Logic to send the music file for download
    return "Downloading music..."

# Run the application
if __name__ == '__main__':
    app.run(debug=True)


**Note:** This code assumes you have a SQLite database named 'music_store.db' with a table called 'albums' and a table called 'purchases'. You will need to create these tables and populate them with data before running the application.