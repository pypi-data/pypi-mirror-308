import pkg_resources
 
def update_dockerfile(dockerfile_template, new_dockerfile_name, app_port, app_entrypoint):
    # updating
    new_dockerfile_content = pkg_resources.resource_filename(__name__, dockerfile_template)
    with open(new_dockerfile_content, 'r') as read_file:
        filedata = read_file.read()
        filedata = filedata.replace("PORT", app_port)
        filedata = filedata.replace("APP_ENTRY", app_entrypoint)
    with open(new_dockerfile_name, 'w') as write_file:
        write_file.write(filedata)


def main_dockerfile(new_dockerfile_name, dockerfile_template, app_port, app_entrypoint):
    update_dockerfile(dockerfile_template, new_dockerfile_name, app_port, app_entrypoint)

# main()