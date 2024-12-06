import shutil
from pathlib import Path
import pkg_resources

def copy_chart(chart_template_path, helmchart_name):
    shutil.copytree(chart_template_path, helmchart_name)

def update_chart(helmchart_name):
    for item in Path(helmchart_name).rglob('*'):
        if item.is_file():
            # updating
            with open(item, 'r') as read_file:
                filedata = read_file.read()
                filedata = filedata.replace('helm_template', helmchart_name)
            with open(item, 'w') as write_file:
                write_file.write(filedata)

chart_template_name = 'templates/helm_template'

def main_helmchart(helmchart_name):
    chart_template_path_content = pkg_resources.resource_filename(__name__, chart_template_name)
    copy_chart(chart_template_path_content, helmchart_name)
    update_chart(helmchart_name)

# main()