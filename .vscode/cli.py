import subprocess

import typer

app = typer.Typer()


@app.command()
def gitf():
  for i in range(2):
    try:
      subprocess.run("git add -A", check=True)
      subprocess.run("git commit -m f", check=True)
      break
    except Exception:
      if i:
        raise
      continue
  subprocess.run("git push", check=False)


@app.command()
def _():
  pass


if __name__ == "__main__":
  app()
