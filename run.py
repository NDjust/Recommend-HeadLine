from DataHandler import ConfigHandler
import os

if __name__ == '__main__':
    config = ConfigHandler.loadFromFile("config.conf")

    if config == None or not ConfigHandler.check(config):
        if 'config.conf' in os.listdir():
            os.rename('config.conf', 'config.conf.old')
        ConfigHandler.get_default()
        print("Error occurred while loading 'config.conf'.")
        print("New 'config.conf' has been created. Please insert information in file 'config.conf'.")
        exit()

    print('Select your purpose: ')
    print('1. Prepare title data')
    print('2. Preprocess content data')
    print('3. Extract title without original title')
    print('4. Preprocess title and content pair data')
    print('5. Extract title from contents with origin title')
    print('6. Quit')

    purpose = input('Purpose: ')
    if purpose.strip() not in ['1', '2', '3', '4', '5', '6']:
        print('Please check your selection.')
        exit()

    purpose = int(purpose.strip())
    if purpose == 1:
        from TextPreprocessing.main import get_titles
        get_titles()
    elif purpose == 2:
        from TextPreprocessing.main import get_summarizes, clean_summarizes
        get_summarizes()
        clean_summarizes()
    elif purpose == 3:
        from Comparing.ExtractTitle import extract_from_given_title
        extract_from_given_title()
    elif purpose == 4:
        from TextPreprocessing.main import main
        main()
    elif purpose == 5:
        from Comparing.ExtractTitle import extract_from_origin_title
        extract_from_origin_title()
    else:
        exit()