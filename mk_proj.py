from Cheetah.Template import Template
import argparse
import uuid
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('name')
parser.add_argument('--main', default='main')
parser.add_argument('--number', '-n', type=int, default=1)
parser.add_argument('--template', '-t')
parser.add_argument('--vscode', action='store_true') # vscode mode instead of msvc

# by default the project just supports x64 - use these flags to override that setting
parser.add_argument('--x86', action='store_true')
parser.add_argument('--x64', action='store_true')
args = parser.parse_args()

# make the required uuids

# in filters
source_folder_guid = uuid.uuid4()
header_folder_guid = uuid.uuid4()

# in sln
solution_guid = uuid.uuid4()
project_guid = uuid.uuid4()
vcxproj_guid = uuid.uuid4()

gen_x86 = True
gen_x64 = True

if args.x86:
    gen_x64 = 'x64' in args and args.x64
if args.x64:
    gen_x86 = 'x86' in args and args.x86

num_files = args.number

if num_files == 1:
    main_cpp = args.main
else:
    main_cpp = 'a.cpp'

searchlist = {
    'main': main_cpp,
    'gen_x86': gen_x86,
    'gen_x64': gen_x64,
    'project_name': args.name,
    'project_guid': project_guid,
    'vcxproj_guid': vcxproj_guid,
    'solution_guid': solution_guid,
    'source_folder_guid': source_folder_guid,
    'header_folder_guid': header_folder_guid,
}

# create the output directory
output_dir = args.name
vscode_dir = os.path.join(output_dir, '.vscode')
project_name = args.name

dirs = [output_dir]
if args.vscode:
    dirs.append(vscode_dir)
for d in dirs:
    try:
        os.mkdir(d)
    except:
        pass

# create the template files

script_dir = os.path.dirname(os.path.realpath(__file__))

if args.number == 1:
    # create the main.cpp
    t = Template(file=os.path.join(script_dir, 'templates/project.cpp.template'), searchList=searchlist)
    open(os.path.join(output_dir, main_cpp + '.cpp'), 'wt').write(str(t))
else:
    t = Template(file=os.path.join(script_dir, 'templates/project.cpp.template'), searchList=searchlist)
    for i in range(args.number):
        open(os.path.join(output_dir, chr(ord('a')+i) + '.cpp'), 'wt').write(str(t))

if args.vscode:
    for base in ['launch.json', 'tasks.json']:
        src = os.path.join(script_dir, 'templates', base + '.template')
        dst = os.path.join(vscode_dir, base)
        print('Parsing: %s to %s' % (src, dst))
        t = Template(file=src, searchList=searchlist)
        open(dst, 'wt').write(str(t))
else:
    # create additional project files
    for base in ['project.sln', 'project.vcxproj', 'project.vcxproj.filters', 'project.vcxproj.user']:
        src = os.path.join(script_dir, 'templates', base + '.template')
        dst = os.path.join(output_dir, base.replace('project', project_name))
        print('Parsing: %s to %s' % (src, dst))
        t = Template(file=src, searchList=searchlist)
        open(dst, 'wt').write(str(t))


print('Created: %s' % (os.path.join(output_dir, project_name)))
