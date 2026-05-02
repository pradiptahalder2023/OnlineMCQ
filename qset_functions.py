import os
import glob, shutil, random
from enum import Enum
from pathlib import Path

def fileExists(filename):
    if os.path.exists(filename) and os.path.isfile(filename):
        return True
    else:
       return False
    
def deleteAllFiles(destination_directory,file_pattern):
    full_path_pattern = os.path.join(destination_directory, file_pattern)
    
    files_to_delete = glob.glob(full_path_pattern)
   
    if files_to_delete:
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                # print(f"Deleted: {file_path}")
            except OSError as e:
                # print(f"Error deleting {file_path}: {e}")
                return False
        return True
    else:
        return True

def fileCopy(noofSet,destination_directory,source_file):
    no_of_set = int(noofSet)
    class Set(Enum):
        SET_A = 1
        SET_B = 2
        SET_C = 3
        SET_D = 4
    
    i=1
    try:
        while(i<=no_of_set):
            filename = Set(i).name + ".json"
            destination_file = os.path.join(destination_directory, filename)
            shutil.copy2(source_file, destination_file)
            # flash(f"File '{source_file}' copied successfully to '{destination_file}'","success")
            i=i+1
        return True
    except IOError as e:
            # flash(f"Error copying file: {e}","danger")
            return False

def get_file_list(destination_directory,file_pattern):
    full_path_pattern = os.path.join(destination_directory, file_pattern)
    files = glob.glob(full_path_pattern)
    return files

def suffleQuestions(selalgo, data_read):
    match selalgo:
        # Using random.shuffle() function
        
        case '1':
            random.shuffle(data_read)
            return data_read
        
        # Using random.sample() function
        case '2':
            suffled_data = random.sample(data_read, len(data_read))
            return suffled_data

        # Using Fisher-Yates shuffle Algorithm
        case '3':
            # traversing from the end of the list(In reverse order)
            for p in range(len(data_read)-1, 0, -1):
                # getting a random index from 0 to the current index
                q = random.randint(0, p + 1)
                # Swap the current index element with the element at a random index
                data_read[p], data_read[q] = data_read[q], data_read[p]

            suffled_data = data_read
            return suffled_data
        
        # Using random.randint() and pop() function
        case '4':
            listLength = len(data_read)
            # repeating the loop till the length of the list
            for i in range(listLength):
                # getting a random index in the range 0 and list Length - 1
                randomIndex = random.randint(0, listLength-1)
                # deleting the element at that corresponding index from the list
                ele= data_read.pop(randomIndex)
                # appending the above-deleted element to the input list(adding the element at last)
                data_read.append(ele)
            
            suffled_data = data_read
            return suffled_data

def chooseRandomSet(destination_directory,file_pattern):
    full_path_pattern = os.path.join(destination_directory, file_pattern)
    files = glob.glob(full_path_pattern)
    random_set = random.choice(files)
    return random_set

def getSetName(fullFileName):

    # Create a Path object
    file_path = Path(fullFileName)

    # Get the filename without its extension
    filename_without_extension = file_path.stem
    return filename_without_extension


        
  