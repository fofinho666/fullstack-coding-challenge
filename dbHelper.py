from hackerNewsAPI import HackerNewsAPI

class DbHelper(HackerNewsAPI):
    tops=[]
    def __init__(self,topNum,collection):
        HackerNewsAPI.__init__(self, topNum)
        self.collection=collection
    
    def initCollection(self):
        """Inicialize db with content
        """
        self.tops=self.topStories()
        self.collection.delete_many({})
        self.collection.insert({ 'tops' : self.tops })
        for id in self.tops:
            self.collection.insert(self.item(id))
    
    def updateCollection(self):
        """Check if the Top stories has change and update the db with new content
        """
        newTops = self.topStories()

        removeFromTop = set(self.tops) - set(newTops)
        addToTop = set(newTops) - set(self.tops)

        #remove not top stories
        for id in removeFromTop:
            print ("remove ",str(id))
            self.collection.delete_many({ 'id' : id })

        #add new top stories
        for id in addToTop:
            print ("add ",str(id))
            self.collection.insert(self.item(id))

        #update top in db (order may changed)
        self.collection.update_one(
            { 'tops' : { '$exists' : 'true' } },
            { '$set' : { 'tops' : newTops } }
        )
        self.tops=newTops

        if(len(addToTop)>0) : return True
        return False
        

        