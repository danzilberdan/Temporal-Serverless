import typer
from tsm import function

app = typer.Typer()
app.add_typer(function.app, name="function")


def main():
    app()


if __name__ == '__main__':
    main()
