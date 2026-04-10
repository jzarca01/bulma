import typer
from services.label import Label
from services.psd import PSDService

app = typer.Typer()
psd_service = PSDService()

@app.command()
def hello(file_path: str):
    print(f"Hello {file_path}")
    psd_service.process_psd(file_path)
    if len(psd_service.layers) > 0:
        print("PSD file processed successfully.")
        label = Label(width=400, height=200, base64="")
        label.add_text("Hello World", y=50, font_size=30)
        label.save("example_label.json")



@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
