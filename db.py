import MySQLdb

class TMdb:
    db_user="cs249"
    db_passwd="cs249"
    db_name="cs249"
    db_host="localhost"

    def __init__(self):
        self.db = MySQLdb.connect(host=self.db_host,user=self.db_user,passwd=self.db_passwd,db=self.db_name,charset="utf8", use_unicode = True)
        self.db.set_character_set('utf8')
        #self.db.execute('SET NAMES utf8;')

    def insertBadges(self, ForumId, Id, UserId, Name):
        cursor = self.db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        query ="INSERT INTO badges(ForumId,Id, UserId, Name) VALUES(%s,%s,%s,%s)"
        args=(ForumId,Id, UserId, Name,)
        cursor.execute(query,args)
        self.db.commit()

    def insertComments(self, ForumId,Id, PostId, Score, Text, UserId):
        cursor = self.db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        query ="INSERT INTO comments(ForumId,Id, PostId, Score, Text, UserId) VALUES(%s,%s,%s,%s,%s,%s)"
        args=(ForumId,Id, PostId, Score, Text, UserId)
        cursor.execute(query,args)
        self.db.commit()

    def insertPosts(self, ForumId,Id, PostTypeId, ParentID, AcceptedAnswerId, Score, ViewCount, Body, OwnerUserId, LastEditorUserId, LastEditorDisplayName, Title, Tags, AnswerCount, CommentCount, FavoriteCount):
        cursor = self.db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        query ="INSERT INTO posts(ForumId,Id, PostTypeId, ParentID, AcceptedAnswerId, Score, ViewCount, Body, OwnerUserId, LastEditorUserId, LastEditorDisplayName, Title, Tags, AnswerCount, CommentCount, FavoriteCount) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        args=(ForumId,Id, PostTypeId, ParentID, AcceptedAnswerId, Score, ViewCount, Body, OwnerUserId, LastEditorUserId, LastEditorDisplayName, Title, Tags, AnswerCount, CommentCount, FavoriteCount)
        cursor.execute(query,args)
        self.db.commit()

    def insertPostlinks(self, ForumId,Id, PostId, RelatedPostId, PostLinkTypeId):
        cursor = self.db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        query ="INSERT INTO postlinks(ForumId,Id, PostId, RelatedPostId, LinkTypeId) VALUES(%s,%s,%s,%s,%s)"
        args=(ForumId,Id, PostId, RelatedPostId, PostLinkTypeId)
        cursor.execute(query,args)
        self.db.commit()

    def insertUsers(self, ForumId,Id, Reputation, DisplayName, Views, UpVotes, DownVotes):
        cursor = self.db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        query ="INSERT INTO users(ForumId,Id, Reputation, DisplayName, Views, UpVotes, DownVotes) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        args=(ForumId,Id, Reputation, DisplayName, Views, UpVotes, DownVotes)
        cursor.execute(query,args)
        self.db.commit()

    def insertVotes(self, ForumId,Id, PostId, VoteTypeId, UserId, BountyAmount):
        cursor = self.db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        query ="INSERT INTO votes(ForumId,Id, PostId, VoteTypeId, UserId, BountyAmount) VALUES(%s,%s,%s,%s,%s,%s)"
        args=(ForumId,Id, PostId, VoteTypeId, UserId, BountyAmount)
        cursor.execute(query,args)
        self.db.commit()

    def getAllPosts(self):
        """
        Get all posts.
        return type: tuple of dict"""
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        query = "SELECT * FROM posts"
        cursor.execute(query)
        results = cursor.fetchall()
        self.db.commit()
        return results

    def getAllComments(self):
        """return tuple of dict"""
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        query = "SELECT * FROM comments"
        cursor.execute(query)
        results = cursor.fetchall()
        self.db.commit()
        return results

    def getPost(self, ForumId, PostId):
        """
        Get a row of post (ForumId, PostId).
        Return dict{...}
        """
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        query = "SELECT Body, Id, OwnerUserId, Score, Title,ForumId FROM posts WHERE ForumId=%s AND Id=%s" % (ForumId, PostId)
        cursor.execute(query)
        row = cursor.fetchone()
        self.db.commit()
        return row

    def getAnsInPost(self, ForumId, PostId):
        """
        Get all ans posts whose question is (ForumId, PostId).
        Return tuple of dict{"ForumId", "Id", "OwnerUserId"}
        """
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        query = "SELECT Body,Id,OwnerUserId, Score,ForumId FROM posts WHERE ForumId=%s AND ParentID=%s" % (ForumId, PostId)
        cursor.execute(query)
        results = cursor.fetchall()
        self.db.commit()
        return results

    def getCommentsInPost(self, ForumId, PostId):
        """
        Get all comments of (ForumId, PostId).
        Return tuple of dict{"ForumId", "Id", "UserId"}
        """
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        query = "SELECT Text FROM comments WHERE ForumId=%s AND PostId=%s" % (ForumId, PostId)
        cursor.execute(query)
        results = cursor.fetchall()
        self.db.commit()
        return results



    def getUserInPost(self, ForumId, Id):
        """
        Get all comments of (ForumId, PostId).
        Return tuple of dict{"ForumId", "Id", "UserId"}
        """
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        query = "SELECT Reputation FROM users WHERE ForumId=%s AND Id=%s" % (ForumId,Id)
        cursor.execute(query)
        results = cursor.fetchall()
        self.db.commit()
        return results

    def getPostByTag(self, tag):
        """
        Get post has tag of keyword
        Return tuple of dict
        """
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        query = "SELECT * FROM posts WHERE Tags LIKE '<%s>'" % (tag)
        cursor.execute(query)
        results = cursor.fetchall()
        self.db.commit()
        return results
