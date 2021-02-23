_Author_ = 'Halfi Hamza'
_Gol_ = 'Scraping Cerba pdf'

import fitz, io, json


def select_pages(start_page, end_page):
    # read pdf fitz like objects
    doc = fitz.open("Catalogue_des_examens_spécialisés_.pdf")

    # load pages
    for page_number in range(start_page, end_page):
        page = doc.loadPage(page_number)
        # convert page to text
        page_text = page.getText("text")
        # write output to text file
        with io.open("output.txt", 'a+', encoding="utf-8") as text:
            text.write(page_text)


def generate_data(array):
    # variables
    technique = 0
    volume = 0
    sous_type = 0
    
    data = {"examen":'', "sous type d'examen":'', "type de prélèvement":'', "technique":'', "volume minimale":'', "fréquence":'', "délai":''}
    
    # get array value
    for i, value in enumerate(array):
        # remove new line char
        result = value.replace('\n', '')
        # examen
        data["examen"] = array[0].replace('\n', '').replace('\ufeff', '')
        
        # type de prélèvement
        if result.startswith('✓ '):
            data["type de prélèvement"] = result.replace('✓ ', '')
            technique = i + 1
            sous_type = i - 1
            
            # sous type d'examen
            if sous_type == 0:
                data["sous type d'examen"] = ''
            else:
                data["sous type d'examen"] = array[sous_type].replace('\n', '')
        
        # volume minimale
        if result.endswith(' ml'):
            data['volume minimale'] = result
            volume = i
        
        # fréquence
        if result.endswith('/s'):
            data['fréquence'] = result
        
        # technique
        data['technique'] = ''.join(array[technique:volume]).replace('\n', '')
        
        # délai
        if result.endswith(' j'):
            data['délai'] = result
            
            # dump data to json file
            with open('cerba.json', 'a', encoding='utf-8') as j:
                json.dump(data, j, ensure_ascii=False, indent=4)

def parsing():
    # Variables
    start_point = 0
    end_point = 0

    # read output and generate data
    with io.open("output.txt", 'r', encoding="utf-8") as f:
        lines = f.readlines()
    
        for i, line in enumerate(lines):
            value = line.replace('\ufeff', '').replace("\n", "")
            if value.startswith("AC") and len(value) > 3:
                start_point = i
            if value.endswith(' j'):
                end_point = i + 1
                generate_data(lines[start_point:end_point])

parsing()
