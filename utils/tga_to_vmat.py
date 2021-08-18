# cmd command: python tga_to_vmat.py "C:\Program Files (x86)\Steam\steamapps\common\Half-Life Alyx\content\hl2\materials\"
# MUST run in the models folder

import re, sys, os

INPUT_FILE_EXT = '.tga'
OUTPUT_FILE_EXT = '.vmat'

# TODO: Move to args
NORMAL_SUFFIX = "_nm"
ROUGHNESS_SUFFIX = "_bump"

VMAT_BASE = '''// THIS FILE IS AUTO-GENERATED

Layer0
{
	shader "vr_complex.vfx"

	//---- Ambient Occlusion ----
	g_flAmbientOcclusionDirectDiffuse "0.000"
	g_flAmbientOcclusionDirectSpecular "0.000"
	TextureAmbientOcclusion "materials/default/default_ao.tga"

	//---- Color ----
	g_flModelTintAmount "1.000"
	g_vColorTint "[1.000000 1.000000 1.000000 0.000000]"
	TextureColor "<texture_color>"

	//---- Fade ----
	g_flFadeExponent "1.000"

	//---- Fog ----
	g_bFogEnabled "1"

	//---- Lighting ----
	g_flDirectionalLightmapMinZ "0.050"
	g_flDirectionalLightmapStrength "1.000"

	//---- Metalness ----
	g_flMetalness "0.000"

	//---- Normal ----
	TextureNormal "<texture_normal>"

	//---- Roughness ----
	TextureRoughness "<texture_roughness>"

	//---- Texture Coordinates ----
	g_nScaleTexCoordUByModelScaleAxis "0"
	g_nScaleTexCoordVByModelScaleAxis "0"
	g_vTexCoordOffset "[0.000 0.000]"
	g_vTexCoordScale "[1.000 1.000]"
	g_vTexCoordScrollSpeed "[0.000 0.000]"
}
'''

def text_parser(filepath, separator="="):
    return_dict = {}
    with open(filepath, "r") as f:
        for line in f:
            if not line.startswith("//") or line in ['\n', '\r\n'] or line.strip() == '':
                line = line.replace('\t', '').replace('\n', '')
                line = line.split(separator)
                return_dict[line[0]] = line[1]
    return return_dict

def walk_dir(dirname, file_ext):
    files = []

    for root, dirs, filenames in os.walk(dirname):
        for filename in filenames:
            if filename.lower().endswith(file_ext) and not filename.lower().endswith(NORMAL_SUFFIX + file_ext) and not filename.lower().endswith(ROUGHNESS_SUFFIX + file_ext):
                files.append(os.path.join(root,filename))

    return files

def putl(f, line, indent = 0):
    f.write(('\t' * indent) + line + '\r\n')

def strip_quotes(s):
    return s.strip('"').strip("'")

def fix_path(s):
    return strip_quotes(s).replace('\\', '/').replace('//', '/').strip('/')

def relative_path(s, base):
    base = base.replace(abspath, '')
    base = base.replace(os.path.basename(base), '')

    return fix_path(os.path.basename(abspath) + base + '/' + fix_path(s))

print('--------------------------------------------------------------------------------------------------------')
print('Source 2 VMAT Generator! By pack via Github.')
print('Initially forked by Alpyne, this version by caseytube and Rectus.')
print('--------------------------------------------------------------------------------------------------------')
abspath = ''
files = []

PATH_TO_CONTENT_ROOT = input("What folder would you like to convert? Valid Format: C:\\Program Files (x86)\\Steam\\steamapps\\common\\Half-Life Alyx\\content\\hl2\\materials\\: ").lower()
if not os.path.exists(PATH_TO_CONTENT_ROOT):
    print("Please respond with a valid folder or file path! Quitting Process!")
    quit()

# recursively search all dirs and files
abspath = os.path.abspath(PATH_TO_CONTENT_ROOT)
print(abspath)
if os.path.isdir(abspath):
    files.extend(walk_dir(abspath, INPUT_FILE_EXT))
#else:
#    if abspath.lower().endswith(INPUT_FILE_EXT):
#        files.append(abspath)

for filename in files:
    out_name = filename.replace(INPUT_FILE_EXT, OUTPUT_FILE_EXT)
    if os.path.exists(out_name): continue

    print('Importing', os.path.basename(filename))

    sourcePath = "materials" + filename.split("materials", 1)[1] # HACK?
    tga_path = fix_path(sourcePath)

    file_name_out_ext = os.path.basename(filename).replace(INPUT_FILE_EXT, "")

    normal_file = filename.replace(INPUT_FILE_EXT, NORMAL_SUFFIX + INPUT_FILE_EXT)
    roughness_file = filename.replace(INPUT_FILE_EXT, ROUGHNESS_SUFFIX + INPUT_FILE_EXT)

    with open(out_name, 'w') as out:
        out_content = VMAT_BASE
        out_content = out_content.replace('<texture_color>', tga_path)

        out_content = out_content.replace('<texture_normal>', fix_path("materials" + normal_file.split("materials", 1)[1]) if os.path.isfile( normal_file ) else "materials\default\default_normal.tga")
        out_content = out_content.replace('<texture_roughness>', fix_path("materials" + roughness_file.split("materials", 1)[1]) if os.path.isfile( roughness_file ) else "materials\default\default_rough.tga")

        out_content = out_content.replace((' ' * 4), '\t')

        putl(out, out_content)

input("Press the <ENTER> key to close...")