import os

from whoosh.fields import Schema, ID, KEYWORD, TEXT
from whoosh.index import create_in, open_dir
from whoosh.query import Or,Term
from whoosh.qparser import MultifieldParser
from db import TMdb

INDEX_DIR = "TMIndexes"     # directory for index
POST_INDEX = "POST_INDEX"   # index for posts
COMMENT_INDEX = "COMMENT_INDEX" # index for comments

# post index schema
Post_Schema = Schema(ForumId=ID(stored=True), Id=ID(stored=True), Body=TEXT, OwnerUserId=ID(stored=True), Title=TEXT, Tags=TEXT)
# comment index schema
Comment_Schema = Schema(ForumId=ID(stored=True), Id=ID(stored=True), PostID=ID(stored=True), Text=TEXT, UserID=ID(stored=True))


def init():
    """create directory and files for index"""
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)

    ix = create_in(INDEX_DIR, Post_Schema, indexname=POST_INDEX)
    ix = create_in(INDEX_DIR, Comment_Schema, indexname=COMMENT_INDEX)

#def update():
#    ix = index.open_dir(INDEX_DIR)

def create(start):
    """create indexes for posts and comments from scratch"""

    init()
    db = TMdb()

    # write posts index
    ix = open_dir(INDEX_DIR, indexname=POST_INDEX)
    writer = ix.writer()
    posts = db.getAllPosts()
    for post in posts:
        if post["PostTypeId"] == 1 and post["ForumId"] > start:
            tags = u" ".join(post["Tags"])
            writer.add_document(ForumId=unicode(post["ForumId"]), Id=unicode(post["Id"]), Title=unicode(post["Title"]), Body=unicode(post["Body"]),Tags=unicode(tags))  #DEBUG
    writer.commit()

    # comment index
    # ix = open_dir(INDEX_DIR, indexname=COMMENT_INDEX)
    # writer= ix.writer()
    # comments = db.getAllComments()
    # for comment in comments:
    #     writer.add_document(ForumId=unicode(post["ForumId"]),Id=unicode(comment["Id"]), PostID=unicode(comment["PostID"]), Text=unicode(comment["Text"]))   #DEBUG
    # writer.commit()

def searchPost(keyword, ForumId=None):
    """
        Search posts with keyword
        [IN]: keyword
        [OUT]: list of post IDs
    """
    # q = Or([Term("Title", unicode(keyword)), Term("Body", unicode(keyword))])
    parser = MultifieldParser(["Title", "Body", "Tags"], schema=Post_Schema)
    s_parser = parser.parse("Title OR beta gamma")
    words=""
    for k in keyword:
        words += k+" and "

    q = parser.parse(words[0:-5])
    allow_q = Term("ForumId", str(ForumId)) if ForumId else None
    print q
    ix = open_dir(INDEX_DIR, indexname=POST_INDEX)
    results = []
    with ix.searcher() as searcher:
        hits = searcher.search(q, filter=allow_q, limit=None)
        for hit in hits:
            results.append((hit["ForumId"], hit["Id"]))
    return results

# def searchComment(keyword):
#     """
#         Search comments with keyword
#         [IN]: keyword
#         [OUT]: list of comment IDs
#     """
#     q = Term("Text", unicode(keyword))
#     ix = open_dir(INDEX_DIR, indexname=COMMENT_INDEX)
#     results = []
#     with ix.searcher() as searcher:
#         hits = searcher.search(q,limit=None)
#         for hit in hits:
#             results.append(hit["Id"])
#     return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Build Indexes')
    parser.add_argument('-s', default=0, help='Begin Forum Id')
    args = parser.parse_args()
    #print args

    if args.s == 0:
        init()
    create(args.s)
