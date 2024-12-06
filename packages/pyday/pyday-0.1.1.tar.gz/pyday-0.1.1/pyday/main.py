import typer
from opencc import OpenCC

from .changelang import change_json_value
from .utils.fileIO import input_file, output_file

app = typer.Typer(no_args_is_help=True)

@app.command()
def changelang(file:str, lang:str, output_name:str=None, output:str = "./dist"):
    data = input_file(file)
    if isinstance(data, dict):
        data = change_json_value(data, lang)
    else:
        data = OpenCC(lang).convert(data)
    
    if not output_name:
        output_name = file.split('/')[-1]
    output_file(output_name, data, output)