import pickle

def save(path, file_name, obj):
    # obj = ['write blog post', 'reply to email', 'read in a book']
    with open(path+'\\'+file_name, 'wb') as file:
        pickle.dump(obj, file)
    print('save: ' + str(obj))

def load(path, file_name):
    with open(path+'\\'+file_name, "rb") as file:
        obj = pickle.load(file)
    print('load: ' + str(obj))
    return obj

class Project():

    def __init__(self, data_files_manager, data_sets_manager,
                 models_manager):
        self.data_files_manager = data_files_manager
        self.data_sets_manager = data_sets_manager
        # self.models_manager = models_manager