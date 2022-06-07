from subprocess import call
import os,csv


dir_path = os.path.dirname(os.path.realpath(__file__))


def extract(currentFile, previousFile, previousExists):

    jar = dir_path + '/ck-0.2.1-SNAPSHOT-jar-with-dependencies.jar'
    res = list()

    file_name_current = currentFile
    current = os.path.dirname(file_name_current)
    current_out = dir_path + '/current/results.csv'
    call(['java ', '-jar', jar, current, current_out])
    current_res = parse(current_out, file_name_current)

    if previousExists:
        file_name_previous = previousFile
        previous = os.path.dirname(file_name_previous)
        previous_out = dir_path + '/previous/results.csv'
        call(['java', '-jar', jar, previous, previous_out])    
        previous_res = parse(previous_out, file_name_previous)

        diff_res = dict()
        for (k, v) in current_res.items():
            diff = float(v) - float(previous_res[k])
            diff_res[k] = diff
            
        res.append(diff_res)
        res.append(current_res)
        res.append(previous_res)
        
    else:
        res.append(current_res)
   
    deleteFolderContents(dir_path+'/current')
    deleteFolderContents(dir_path+'/previous')

    return res


def deleteFolderContents(folderName):
    folder = folderName
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
def parse(fileLoc, fileName):
    data = list()
    with open(fileLoc, 'r', newline='') as csv_file:
        csvReader = csv.reader(csv_file)
        for line in csvReader:
            data.append(line)

    res = dict()
    res_keys = data[0][3:]
    res_values = list()
    for line in data:
        if line[0] == fileName.replace('/', '\\'):
            res_values = line[3:]
    
    res = dict(zip(res_keys, res_values))
    return res
def test(source_directory,out_dir):
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    
    jar = dir_path + r'\libs\ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar'
    call(['java ', '-jar', jar,source_directory,"False","0","True",out_dir])
if __name__ == '__main__':
    pass