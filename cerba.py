_Author_ = 'Halfi Hamza'
_Gol_ = 'Scraping Cerba pdf'

import fitz, io, json, sys, argparse
from sys import stdout
from os import remove
from os.path import isfile


def select_pages(first, last):
    # read pdf fitz like objects
    doc = fitz.open("Catalogue_des_examens_spécialisés_.pdf")
    
    # load pages
    for page_number in range(first, last):
        stdout.write("\rLoad Page N°: %i page" % page_number)
        stdout.flush()
        page = doc.loadPage(page_number)
        # convert page to text
        page_text = page.getText("text")
        # write output to text file
        with io.open("output.txt", mode='a+', encoding="utf-8") as text:
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
            with open('cerba_ouput.json', mode='a+', encoding='utf-8') as j:
                json.dump(data, j, ensure_ascii=False, indent=4)
                

def parsing():
    # Variables
    start_point = 0
    end_point = 0

    # read output and generate data
    with io.open("output.txt", 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            stdout.write("\rGenerate Lines: %i line" % i)
            stdout.flush()
            value = line.replace('\ufeff', '').replace("\n", "")
            if value.startswith("AC") and len(value) > 3:
                start_point = i
            if value.endswith(' j'):
                end_point = i + 1
                generate_data(lines[start_point:end_point])


if __name__ == "__main__":
    # command line argument input
    parser = argparse.ArgumentParser()
    parser.add_argument('-F', '--first_page', default=40, help='number of first page', type=int)
    parser.add_argument('-L', '--last_page', default=50, help='number of last page', type=int)
    args = parser.parse_args()

    # remove files befor
    if isfile('output.txt'):
        remove('output.txt')
    if isfile('cerba_ouput.json'):
        remove('cerba_ouput.json')

    print('\nStart Reading pages\n')
    select_pages(first=args.first_page, last=args.last_page)
    print('\n')
    parsing()
