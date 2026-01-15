from submissions import create_app  # absolute import
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
