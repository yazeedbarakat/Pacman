from config_parser import read_config

con = read_config('config.json')
print(con)
level_index = 0
def get_level_config():
    global level_index
    level = con['levels'][level_index]
    width = level['width']
    height = level['height']
    print(width, height)
    level_index += 1
for i in range(len(con)):
    get_level_config()
