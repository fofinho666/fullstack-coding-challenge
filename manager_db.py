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

    def start(self):
        """
        Starts filling the database
        """
        try:
            #Clean database
            self.database.delete_many({})

            #Get top stories into database
            self.top_stories = self.harckernews.get_top_stories()
            self.database.insert({'tops' : self.top_stories})

            #Get sotries into database
            for id_ in self.top_stories:
                self.add_storie_to_databbase(id_)
        except:
            pass
        
    def add_storie_to_databbase(self, id_):
        """
        Get stories and initialize translation
        """
        try:
            storie = self.harckernews.get_item(id_)

            for language in self.languages_list:

                translation = self.unbabel.request_translation(storie['title'], language)

                if translation is not None :
                    translation['id'] = id_
                else:
                    translation = {
                        "status": "request_translation_failed",
                        "target_language": language,
                        "text": storie['title'],
                        "id": id_
                    }
                self.database.insert(translation)

            self.database.insert(storie)
        except:
            pass

    def update_top_stories(self):
        """
        See if the top has changed and update the database
        """
        try:
            new_top_stories = self.harckernews.get_top_stories()
            remove_top_stories = set(self.top_stories) - set(new_top_stories)
            add_top_stories = set(new_top_stories) - set(self.top_stories)

            #remove old top stories
            for id_ in remove_top_stories:
                self.database.delete_many({'id' : id_})

            #add new top stories
            for id_ in add_top_stories:                
                self.add_storie_to_databbase(id_)

            #update top in db (order may has changed)
            self.database.update_one(
                {'tops' : {'$exists' : 'true'}},
                {'$set' : {'tops' : new_top_stories}}
            )
            self.top_stories = new_top_stories
        except:
            pass

    def update_a_translation(self, language):
        """
        Check if the state of a translation has changed and save it in the database
        """
        try:
            trans_status = self.database.find_one(
                {'$or' : [
                    {'status' : 'new', 'target_language' : language},
                    {'status' : 'translating', 'target_language' : language}]}
            )

            uid = trans_status['uid']            
            new_trans_status = self.unbabel.get_translation(uid)

            if new_trans_status['status'] != trans_status['status']:

                new_trans_status['id'] = trans_status['id']

                self.database.update_one(
                    {'uid' : uid, 'status' : trans_status['status']},
                    {'$set' : new_trans_status}
                )
        except:
            pass
