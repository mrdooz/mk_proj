from Cheetah.Template import Template
import argparse
import uuid
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('name')
parser.add_argument('--main', default='main')

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

searchlist = {
    'main': args.main,
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
main = args.main
output_dir = args.name
project_name = args.name

try:
    os.mkdir(output_dir)
except:
    pass

# create the template files

# create the main.cpp
t = Template(file='templates/project.cpp.template', searchList=searchlist)
open(os.path.join(output_dir, main + '.cpp'), 'wt').write(str(t))

# create additional project files
for base in ['project.sln', 'project.vcxproj', 'project.vcxproj.filters', 'project.vcxproj.user']:
    src = os.path.join('templates', base + '.template')
    dst = os.path.join(output_dir, base.replace('project', project_name))
    print('Parsing: %s to %s' % (src, dst))
    t = Template(file=src, searchList=searchlist)
    open(dst, 'wt').write(str(t))

print('Created: %s' % (os.path.join(output_dir, project_name)))