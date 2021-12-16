import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")


@app.command()
def db(user: str = typer.Option(...), 
    password=typer.Option(...)):
    print (f"{user} {password}")



if __name__ == "__main__":
    app()