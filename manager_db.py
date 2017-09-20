def add_translation_data_to_title(item, unbabel_api, languages_list):
    """
    This function add translation data to the item object
    """
    item_result = item
    try:
        text = item['title']
        # Get translations uids for each language and added to item
        for language in languages_list:
            translation_data = get_translation_data( unbabel_api, text, language)
            item_result.update(translation_data)
    except:
        return item
    return item_result

def get_translation_data(unbabel_api, text, language):
    key_uid = 'translation_{}_uid'.format(language)
    key_status = 'translation_{}_status'.format(language)
    key_ = 'translation_{}'.format(language)
    translation_data = {
        key_uid : None,
        key_status : 'error',
        key_ : None
    }

    try:
        res = unbabel_api.request_translation(text, language)
        if res:
            translation_data[key_uid] = res['uid']
            translation_data[key_status] = 'translating'
            translation_data[key_] = None
        
        return translation_data
    except:
        return translation_data
    
class DatabaseManager(object):
    """
    Class to manage database
    """
    def __init__(self, collection, hackernews_api, unbabel_api, languages_list):
        self.database = collection
        self.harckernews = hackernews_api
        self.unbabel = unbabel_api
        self.languages_list = languages_list
        self.top_stories = []

        try:
            #Clean database
            self.database.delete_many({})

            #Get top stories into database
            self.top_stories = self.harckernews.get_top_stories()
            self.database.insert({'tops' : self.top_stories})

            #Get sotries into database
            for id_ in self.top_stories:
                storie = self.harckernews.get_item(id_)
                #add translation data to storie
                storie = add_translation_data_to_title(storie, self.unbabel, self.languages_list)
                self.database.insert(storie)
        except:
            pass

    def update_top_stories(self):
        try:
            new_top_stories = self.harckernews.get_top_stories()
            remove_top_stories = set(self.top_stories) - set(new_top_stories)
            add_top_stories = set(new_top_stories) - set(self.top_stories)

            #remove old top stories
            for id_ in remove_top_stories:
                print ("remove ", str(id_))
                self.database.delete_many({'id' : id_})

            #add new top stories
            for id_ in add_top_stories:
                storie = self.harckernews.get_item(id_)
                #add translation uis to storie
                storie = add_translation_data_to_title(storie, self.unbabel, self.languages_list)
                self.database.insert(storie)

            #update top in db (order may has changed)
            self.database.update_one(
                {'tops' : {'$exists' : 'true'}},
                {'$set' : {'tops' : new_top_stories}}
            )
            self.top_stories=new_top_stories   
        except:
            pass
        
    def update_a_random_translation(self,language):
        key_uid = 'translation_{}_uid'.format(language)
        key_status = 'translation_{}_status'.format(language)
        key_ = 'translation_{}'.format(language)

        try:
            storie = self.database.find_one({key_status : 'translating'})
            if storie:
                uid = storie[key_uid]
                translation = self.unbabel.get_translation(uid)
                
                if translation['status'] == 'completed':                    
                    storie[key_] = translation['translatedText']
                    storie[key_status] = 'completed'
                    self.database.update_one(
                        {'id' : storie['id']},
                        {'$set' : storie}
                    )
        except:
            """
            #APAGAR!!!
            storie = self.database.find_one({key_status : 'error'})
            uid = storie[key_uid]
            #translation = self.unbabel.get_translation(uid)

            #if translation['status'] == 'completed':
            storie[key_] = 'test {} translation'.format(language)
            storie[key_status] = 'completed'
            self.database.update_one(
                {'id' : storie['id']},
                {'$set' : storie}
            )
            """
            pass
        