import os
import re

# Defining CSS variables to replace
css_variables = {
    # VARIABLES, are added here. This means you can adjust appearance and styling fast, all the following main css can 
        # then be considered relative to each other. Eg. if you change t5 you change all line types, cuts etc. with a slightly thicker
        # line than normal, and --green you change for all concrete insitu materials. 
        # So in many ways this is a configuration file where sized are defined compared to each other, if you want to just change a size
        # or color, do it here in the beginning, want to dive deep into which exact thickness is used when, modify the variable or statics in main
    
    # VARIABLES, DK STANDARD COLORS RELATED TO MATERIALS */
        # where colors don't relate to materials they are hardcoded */
        # Green, Concrete insitu
        # cyan, Concrete precast
        # green toned Concrete light
        # brown red Masonry
        # yellow Insulation soft, The color is actually curry, but the closest one to yellow in the system.
        # orange Insulation hard
        # gray Expanded clay, eg. leca og letklinker
        # brown dark Wood element, color is actually called curry 3
        # brown Wood, both structural and laminated timber
        # red Steel
        # brown light Gypsum, color is actually called curry 4
        # brown black Terrain
        # yellow toned Filling eg. sand etc.
    '--concrete-color': 'rgb(0, 255, 0)',
    '--concrete-precast-color': 'rgb(0, 255, 255)',
    '--concrete-light-color': 'rgb(0, 200, 0)',
    '--masonry-color': 'rgb(129, 64, 0)',
    '--insulation-soft-color': 'rgb(255, 191, 0)',
    '--insulation-hard-color': 'rgb(255, 128, 0)',
    '--exspandedclay-color': 'rgb(195, 175, 165)',
    '--wood-element-color': 'rgb(129, 96, 0)',
    '--wood-color': 'rgb(153, 102, 0)',
    '--steel-color': 'rgb(255, 0, 0)',
    '--gypsom-color': 'rgb(189, 173, 126)',
    '--terrain-color': 'rgb(97, 75, 62)',
    '--filling-color': 'rgb(204, 153, 0)',
    
    # VARIABLES, DK STANDARD LINE-THICKNESS/STROKE-WIDTH
        # for lines we toughly divide with 2 to get proper thickness eg. 0.35mm/2=0.175, final thickness is measured in 1:1 on the printed drawing
        # t1 0.06mm = 0.06/2 = 0.03 VERY THIN
        # t2 0.12mm = 0.12/2 = 0.06
        # t3 0.18mm = 0.18/2 = 0.09 USED for eg. cuts on secondary materials
        # t4 0.25mm = 0.25/2 = 0.125 GENERAL LINE TYPE
        # t5 0.35mm = 0.35/2 = 0.175 USED for eg. cuts on main materials
        # t6 0.50mm = 0.50/2 = 0.25 
        # t7 0.70mm = 0.70/2 = 0.35 
        # t8 1.00mm = 1.00/2 = 0.5 VERY THICK
    '--t1': '0.03px',
    '--t2': '0.06px',
    '--t3': '0.09px',
    '--t4': '0.125px',
    '--t5': '0.175px',
    '--t6': '0.25px',
    '--t7': '0.35px',
    '--t8': '0.5px'
}

def replace_css_variables(css_content, variables):
    def replacer(match):
        var_name = match.group(1)
        return variables.get(f'--{var_name}', match.group(0))
    
    pattern = re.compile(r'var\(--([a-zA-Z0-9-]+)\)')
    return pattern.sub(replacer, css_content)

def remove_duplicate_classes(default_css, dk_css):
    # Extract class names from DK CSS
    dk_classes = set(re.findall(r'\.([a-zA-Z0-9-]+)\s*{', dk_css))
    
    # Remove classes from default CSS if they are present in DK CSS
    def replacer(match):
        class_name = match.group(1)
        if class_name in dk_classes:
            return ''
        return match.group(0)
    
    pattern = re.compile(r'\.([a-zA-Z0-9-]+)\s*{[^}]*}')
    return pattern.sub(replacer, default_css)

def clean_css(css_content):
    # Remove empty class definitions
    css_content = re.sub(r'\.[a-zA-Z0-9-]+\s*{\s*}', '', css_content)
    # Remove extra blank lines
    css_content = re.sub(r'\n\s*\n', '\n', css_content)
    # Remove duplicate lines
    lines = css_content.split('\n')
    seen = set()
    cleaned_lines = []
    for line in lines:
        if line.strip() and line not in seen:
            seen.add(line)
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def process_css_files(default_path, dk_path, output_path, variables):
    with open(default_path, 'r', encoding='utf-8') as file:
        default_css = file.read()
    
    with open(dk_path, 'r', encoding='utf-8') as file:
        dk_css = file.read()
    
    # Remove duplicate classes from default CSS
    default_css_no_duplicates = remove_duplicate_classes(default_css, dk_css)
    
    # Combine the CSS contents, ensuring DK-specific styles come last
    combined_css = f"{default_css_no_duplicates}\n\n/* --------------------DK OVERRIDES-------------------- */\n{dk_css}"
    
    # Replace CSS variables with their actual values
    processed_css = replace_css_variables(combined_css, variables)
    
    # Clean up the CSS content
    cleaned_css = clean_css(processed_css)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_css)

# Example usage
script_dir = os.path.dirname(os.path.abspath(__file__))
default_css_path = os.path.join(script_dir, 'default_RAW.css')
dk_css_path = os.path.join(script_dir, 'default_DK_RAW.css')
output_css_path = os.path.join(script_dir, 'default_DK.css')

process_css_files(default_css_path, dk_css_path, output_css_path, css_variables)