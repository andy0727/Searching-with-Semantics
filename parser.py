import db
import xml.etree.ElementTree as ET
import os
import TMIndex
import sys

def parse(f, ForumId):
    var = "NULL"
    var1 = "-1"
    tree = ET.parse(f)
    root = tree.getroot()
    try:
        mydb = db.TMdb()
    except Exception,e:
        print "error: cannot make connection\n", e
        return

    if f.endswith("Badges.xml"):
        for row in root.findall("row") :
            Id = row.get("Id")
            UserId = row.get("UserId")
            Name = row.get("Name")
            #print "ID:"+ UserId + "\n"

            if UserId == None:
                UserId = var1
            if Name == None:
                Name = var
            try:
                mydb.insertBadges(ForumId,Id,UserId, Name)
            except Exception,e:
                print "error: Badges insertion\n",e 
                mydb.db.close()
                return

    elif f.endswith("Comments.xml"):
        for row in root.findall("row"):
            Id = row.get("Id")
            PostId = row.get("PostId")
            Score = row.get("Score")
            Text = row.get("Text")
            UserId = row.get("UserId")

            if Id == None:
                Id = var
            if PostId ==None:
                PostId = var1
            if Score == None:
                Score = "0"
            if Text == None:
                Text =var
            if UserId == None:
                UserId = var1
            try:    
                mydb.insertComments(ForumId,Id,PostId,Score,Text,UserId)
            except Exception,e:
                print "error: Comments Insertion\n",e
                mydb.db.close()
                return

    elif f.endswith("PostHistory.xml"):
        pass

    elif f.endswith("PostLinks.xml"):   
        for row in root.findall("row") :
            Id = row.get("Id")
            PostId = row.get("PostId")
            RelatedPostId = row.get("RelatedPostId")
            LinkTypeId = row.get("LinkTypeId")

            if Id == None:
                Id = var1
            if PostId ==None:
                PostId = var1
            if RelatedPostId == None:
                RelatedPostId = var1
            if LinkTypeId == None:
                LinkTypeId =var1
            try:
                mydb.insertPostlinks(ForumId,Id,PostId,\
                    RelatedPostId,LinkTypeId)
            except Exception,e:
                print "error: PostLinks Insertion\n",e
                mydb.db.close()
                return

    elif f.endswith ("Posts.xml"):  
        for row in root.findall("row"):
            Id = row.get("Id")
            PostTypeId = row.get("PostTypeId")
            ParentId = row.get("ParentId")
            #(only present if PostTypeId is 1)
            AcceptedAnswerId = row.get("AcceptedAnswerId") 
            Score = row.get("Score")
            ViewCount = row.get("ViewCount")
            Body = row.get("Body")
            OwnerUserId = row.get("OwnerUserId")
            LastEditorUserId = row.get("LastEditorUserId")
            LastEditorDisplayName= row.get("LastEditorDisplayName")
            Title= row.get("Title")
            Tags= row.get("Tags")
            AnswerCount = row.get("AnswerCount")
            CommentCount = row.get("CommentCount")
            FavoriteCount = row.get("FavoriteCount")

            if Id == None:
                Id = var1
            if PostTypeId ==None:
                PostTypeId = var1
            if ParentId == None:
                ParentId = var1
            if AcceptedAnswerId == None:
                AcceptedAnswerId =var1
            if Score == None:
                Score = "0"
            if ViewCount == None:
                ViewCount = var1
            if Body == None:
                Body = var
            if OwnerUserId == None:
                OwnerUserId = var1
            if LastEditorUserId == None:
                LastEditorUserId =var1
            if LastEditorDisplayName == None:
                LastEditorDisplayName = var
            if Title == None:
                Title = var
            if Tags ==None:
                Tags = var
            if AnswerCount == None:
                AnswerCount = "0"
            if CommentCount == None:
                CommentCount = "0"
            if FavoriteCount == None:
                FavoriteCount = "0"     

            try:
                mydb.insertPosts(ForumId,Id,PostTypeId,ParentId, \
                    AcceptedAnswerId, Score, ViewCount, \
                    Body, OwnerUserId, LastEditorUserId, \
                    LastEditorDisplayName, Title, Tags, \
                    AnswerCount, CommentCount, FavoriteCount)

            except Exception,e:
                print "error: Posts Insertion\n",e
                mydb.db.close()
                return

    elif f.endswith("Users.xml"):
        for row in root.findall("row"):
            Id = row.get("Id")
            Reputation = row.get("Reputation")
            DisplayName = row.get("DisplayName")
            Views = row.get("Views")
            UpVotes = row.get("UpVotes")
            DownVotes = row.get("DownVotes")

            if Id == None:
                Id = var1
            if Reputation == None:
                Reputation = "0"
            if DisplayName == None:
                DisplayName = var
            if Views == None:
                Views = "0"
            if UpVotes == None:
                UpVotes = "0"
            if DownVotes == None:
                DownVotes = "0"

            try:
                mydb.insertUsers(ForumId,Id, Reputation,DisplayName, Views,\
                 UpVotes, DownVotes)
            except Exception,e:
                print "error: Users Insertion\n",e  
                mydb.db.close()
                return

    elif f.endswith("Votes.xml"):
        for row in root.findall("row"):
            Id = row.get("Id")
            PostId = row.get("PostId")
            VoteTypeId = row.get("VoteTypeId")
            UserId = row.get("UserId")
            BountyAmount = row.get("BountyAmount")

            if Id == None:
                Id = var1
            if PostId == None:
                PostId = var1
            if VoteTypeId == None:
                VoteTypeId = var
            if UserId == None:
                UserId = var1
            if BountyAmount == None:
                BountyAmount = "0"

            try:
                mydb.insertVotes(ForumId,Id,PostId,VoteTypeId,UserId,BountyAmount)
            except Exception,e:
                print "error: Votes Insertion\n",e
                mydb.db.close()
                return
    else:
        pass

    mydb.db.close()


def create_corpus(keyword, targetForumId, filePath):
    p_list = TMIndex.searchPost(keyword, targetForumId)
    #print "p list is:"
    match = 0
    temp = []
    with open(filePath, 'w') as txt:
        try:
            mydb = db.TMdb()
        except Exception,e:
            print "error: cannot make connection\n", e
            return
        try:
            for (ForumId, Id) in p_list:
                #print ForumId
                #print type(ForumId), type(targetForumId)
                if targetForumId is None or int(ForumId) == targetForumId:
                    txt.write('@INFINITYTEAMBIGTHREAD@\n')

                    ques_dic = mydb.getPost(ForumId, Id)
                    #print ques_dic["Title"].encode('cp1252','ignore')
                    txt.write(ques_dic["Title"].encode('cp1252','ignore') + '\n')

                    # print "@INFINITYTEAMSMALLPOST@"
                    txt.write('@INFINITYTEAMSMALLPOST@\n')

                    # print ques_dic["Body"].encode('cp1252','ignore')
                    txt.write(ques_dic["Body"].encode('cp1252','ignore') + '\n')
                    temp.append((ques_dic["ForumId"],ques_dic["Id"], ques_dic["OwnerUserId"], ques_dic["Score"]))
                	
                    comments = mydb.getCommentsInPost(ForumId, Id)

                    for comment in comments:
                        # print comment["Text"].encode('cp1252', 'ignore')
                        txt.write(comment["Text"].encode('cp1252', 'ignore') + '\n')
                    match += 1

                    tuple_dic = mydb.getAnsInPost(ForumId,Id)
                    for dic in tuple_dic:
                        # print "@INFINITYTEAMSMALLPOST@\n"
                        txt.write('@INFINITYTEAMSMALLPOST@\n')
                        # print dic["Body"].encode('cp1252','ignore')
                        txt.write(dic["Body"].encode('cp1252','ignore') + '\n')
                        temp.append((dic["ForumId"], dic["Id"], dic["OwnerUserId"], dic["Score"]))

                        ans_comments = mydb.getCommentsInPost(ForumId, dic["Id"])
                        for ans_comment in ans_comments:
                            # print ans_comment["Text"].encode('cp1252','ignore')
                            txt.write(ans_comment["Text"].encode('cp1252','ignore') + '\n')
                        match += 1
            # print "@INFINITYTEAMSMALLPOST@\n"
            txt.write('@INFINITYTEAMSMALLPOST@\n')
        except Exception, e:
            print >>sys.stderr, "still out sync"
            raise Exception(e);

        line_tuple = []
        
        for (fid, postid, author, score) in temp:
            rep_dics = mydb.getUserInPost(fid, author)
            for rep_dic in rep_dics:
                line_tuple.append((postid, score, rep_dic["Reputation"]))
        print "total documents are:"+str(match)
        txt.write(str(match) + '\n')
        mydb.db.close()
    return line_tuple

def create_csv(line_tuple, csvFilePath):
    with open(csvFilePath, 'w') as csv:
        for (postid, score, reputation) in line_tuple:
            line = str(postid) + ',' + str(score) + ',' + str(reputation) + '\n'
            csv.write(line)
