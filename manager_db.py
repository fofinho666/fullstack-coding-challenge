def add_title_translation_uids(item, unbabel_api, languages_list):
    try:
        text = item['title']
    except:
        return item
    
    item_result = item
    # Get translations uids for each language and added to item
    for language in languages_list:
        translation_uid = get_translation_uid(text, unbabel_api, language)
        if translation_uid:
            item_result.update(translation_uid)

    return item_result

def get_translation_uid(unbabel_api, text, language):
    try:
        uid = unbabel_api.request_translation(text, language)
        translate_uid = {
            'translation_{}_uid'.format(language) : uid,
            'translation_{}_status'.format(language) : 'translating',
            'translation_{}'.format(language) : None
        }
        return translate_uid
    except:
        translate_uid = {
            'translation_{}_uid'.format(language) : None,
            'translation_{}_status'.format(language) : 'error',
            'translation_{}'.format(language) : None
        }
        return translate_uid

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
                #add translation uis to storie
                storie = add_title_translation_uids(storie, self.unbabel, self.languages_list)
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
                storie = add_title_translation_uids(storie, self.unbabel, self.languages_list)
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
        key_status = 'translation_{}_status'.format(language)
        key_uid = 'translation_{}_uid'.format(language)
        key_ = 'translation_{}'.format(language)
        
        try:
            storie = self.database.find_one({key_status : 'translating'})
            uid = storie[key_uid]
            translation = self.unbabel.get_translation(uid)

            if translation['status'] == 'completed':
                storie[key_] = translation['translatedText']
                storie[key_status] = 'completed'
                self.database.update_one(
                    {'id' : storie['id']},
                    {'$set' : storie}
                )
            pass
        except:
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
            pass
        