import os

# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue, crawled and robots files (if not created)
def create_data_files(project_name, base_url, robots_url):
    queue = os.path.join(project_name , "queue.txt")
    crawled = os.path.join(project_name, "crawled.txt")
    robots = os.path.join(project_name, "robots.txt")

    if not os.path.isfile(robots):
        write_file(robots, robots_url)
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

def create_data_robo_file(project_name, date):
    robots = os.path.join(project_name, "robots.txt")
    
    if not os.path.isfile(robots):
        write_file(robots, date)


# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()                         #Um conjunto para acelerar e remover repeticoes
    with open(file_name, 'rt') as f:        #Rt vai ler cada linha do codigo
        for line in f:
            results.add(line.replace('\n', ''))
    return results

# Read a file in robots.txt
#   Disallow: /header-institucional -> # /header-institucional
def file_to_set_robots(file_name, base_url):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            if "Disallow: " in line:
                line = line.replace('/\n', "")
                results.add(base_url + '/' + line.replace("Disallow: /", ""))
    return results


# Eh nesse momento que voce devera adicionar uma heuristica aqui para ordenar seu crawler
def set_to_file(links, file_name):
    with open(file_name,"w") as f:
        for l in links:
            f.write(l+"\n")