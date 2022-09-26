from application import app

# a simple page that says hello
@app.route('/')
def main():
    return 'Hello, World!'