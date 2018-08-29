import ast
import os
import collections
import nltk
import help_function as hf

global Path


def get_file_names():
    file_names = []
    for dir_name, dirs, files in os.walk(Path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                file_names.append(os.path.join(dir_name, file))
                if len(file_names) >= 100:
                    break
    print('total %s files' % len(file_names))
    return file_names


def get_trees(_path, with_file_names=False, with_file_content=False):
    trees = []
    file_names = get_file_names()

    for filename in file_names:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print("Error while parsing file: %s" % e)
            tree = None
        if with_file_names:
            if with_file_content:
                trees.append((filename, main_file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)
    print('Trees generated')
    return trees


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_top_verbs_by_path(path, top_size=10):
    global Path
    Path = path
    trees = [t for t in get_trees(None) if t]
    fncs = []
    for f in hf.make_flat([[node.name.lower()
                            for node in ast.walk(t)
                            if isinstance(node, ast.FunctionDef)]
                           for t in trees]):
        if not (f.startswith('__') and f.endswith('__')):
            fncs.append(f)
    print('functions extracted')
    verbs = hf.make_flat([hf.get_verbs_from_function_name(function_name)
                          for function_name in fncs])
    return collections.Counter(verbs).most_common(top_size)


wds = []
projects = [
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
]

nltk.download('averaged_perceptron_tagger')

for project in projects:
    path = os.path.join('.', project)
    wds += get_top_verbs_by_path(path)

top_size = 200
print('total %s words, %s unique' % (len(wds), len(set(wds))))
for word, occurence in collections.Counter(wds).most_common(top_size):
    print(word, occurence)
