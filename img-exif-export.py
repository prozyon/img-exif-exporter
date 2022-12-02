 #TODO:
    #implement rename_img

# imports
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import pathlib
import shutil
import csv

# script

def main():

    print("Enter the path to the images")
    folderpath = input()
    print("The folder you have chosen is '" +
          folderpath + "'. Is that correct?")
    bool1 = input("y/n | ")
    if (bool1 == "y"):
        exif_extract(folderpath)
    else:
        print("Exiting.....")

        SystemExit()

#currently unused, will be used in later version of script
def img_copy(path):
    #lists all files in dir,filters out folders
    print("Listing contents of folder:")
    content = os.listdir(path)
    content = [f for f in files if os.path.isfile(path+'/'+f)]
    print(content)
    print("copying all images to folder to rename....")
    #filter for compatible file types
    a_f = [".JPG", ".png"]
    #checks if dir is existing, if not creates it
    if not os.path.isdir(path + "/renamed_images"):
        os.mkdir(path + "/renamed_images")
    #while loop copies files to renamed-images
    i = 0
    print("Copying files...")
    while i < len(content):
        f_ext = pathlib.Path(content[i]).suffix
        if f_ext in a_f:
            src = path + "/" + content[i]
            dst = path + "/renamed_images/" + content[i]
            shutil.copyfile(src, dst)
            if not f_ext in a_f:
                print("Filetype '" + f_ext + "' is not compatible. Skipping...")

        i += 1
    #execs exif_extract to extract exif info to csv files
    exif_extract(path)


def exif_extract(path):
    #checks if dir is existing, if not creates it
    if not os.path.isdir(path + "/exported-exif"):
        os.mkdir(path + "/exported-exif")
    #changes working dir to path of image folder
    cwd = os.chdir(path)
    #lists all files in dir, filters out folders
    files = os.listdir()
    files = [f for f in files if os.path.isfile(path+'/'+f)]
    #counts files and outputs number to user
    print(str(len(files)) + " files avaiable")
    #creates reverse dictionary for exif tags
    _TAGS_r = dict(((v, k) for k, v in TAGS.items()))
    #filter for compatible file types
    a_f = [".JPG", ".jpg"]
    #numerates through files in directory of path
    for i in files:
        #checks if file is compatible
        f_ext = pathlib.Path(i).suffix
        if f_ext in a_f:
            #loads image
            img = Image.open(i)
            #loads exif data of image
            img_exif = img._getexif()
            #set path to 'name of image.csv' file for clarity
            file_name = "./exported-exif/"+ str(i) + ".csv"
            """ print("Writing exif data from " + i + " to csv file...") """
            #checks if exif data is avaiable
            if img_exif is None:
                print("Sorry, image " + i + " has no exif data.")
            else:
                #list of all exif keys in PIL
                keys = list(img_exif.keys())
                #filters out keys which are eg to long or incompatible
                keys.remove(_TAGS_r["MakerNote"])
                keys.remove(_TAGS_r["UserComment"])
                #lists keys as numerated list
                keys = [k for k in keys if k in TAGS]
                #lists key with data attached
                exif_out = [str((TAGS[k], img_exif[k])) for k in keys]
                #lists key names as strings
                header = [str((TAGS[k])) for k in keys]
                #lists data as strings
                rows = [str((img_exif[k])) for k in keys]
                #opens csv file to write
                with open(file_name, 'w') as f: 
                    write = csv.writer(f) 
                    #adds header
                    write.writerow(header) 
                    #adds data
                    write.writerow(rows)
        #if file is incompatible, script is exited.     
        else:
            
            print("File " + i + " not compatible, skipping...")
    print("DONE!")
    
    return
    
                
if __name__ == '__main__':
    main()
