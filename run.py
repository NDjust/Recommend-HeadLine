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
    print('1. Preprocess data')
    print('2. Extract title')
    print('3. Quit')

    purpose = input('Purpose: ')
    if purpose.strip() not in ['1', '2', '3']:
        print('Please check your selection.')
        exit()

    purpose = int(purpose.strip())
    if purpose == 1:
        from TextPreprocessing.main import main
        main()
        pass
    elif purpose == 2:
        from Comparing.ExtractTitle import main
        main()
        pass
    else:
        exit()