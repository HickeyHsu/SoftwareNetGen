from subprocess import call
import os


dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def extractCK(source_directory:str,out_dir:str):
    out_dir=out_dir.replace("\\","/")
    if not out_dir.endswith("/" ):
        out_dir+="/"
    jar = os.path.join(dir_path,"libs","ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar")
    # jar = dir_path + r'\libs\ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar'
    call(['java ', '-jar', jar,source_directory,"False","0","False",out_dir])
if __name__ == '__main__':
    source_directory=r"D:\data_sci\dataset_jira\src\activemq\activemq-5.0.0"
    out_dir="D:/temp/out/"
    extractCK(source_directory,out_dir)