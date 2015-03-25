USE cs249;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS badges;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS postlinks;
DROP TABLE IF EXISTS votes;


CREATE TABLE users (
        ForumId INTEGER, 
        Id INTEGER,
        Reputation INTEGER,
        DisplayName VARCHAR(1000) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
        Views INTEGER,
        UpVotes INTEGER,
        DownVotes INTEGER,
        PRIMARY KEY(ForumId, Id)
);

CREATE TABLE posts
(
        ForumId INTEGER,
        Id INTEGER,
        PostTypeId INTEGER,
        ParentID INTEGER REFERENCES posts(Id),
        AcceptedAnswerId INTEGER REFERENCES posts(Id),
        Score INTEGER,
        ViewCount INTEGER,
        Body TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci,
        OwnerUserId INTEGER REFERENCES users(Id),
        LastEditorUserId INTEGER REFERENCES users(Id),
        LastEditorDisplayName VARCHAR(1000)  CHARACTER SET utf8 COLLATE utf8_unicode_ci,
        Title TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci,
        Tags VARCHAR(1000),
        AnswerCount INTEGER,
        CommentCount INTEGER,
        FavoriteCount INTEGER,

        PRIMARY KEY(ForumId, Id)
);

CREATE TABLE badges
(
        ForumId INTEGER,
        Id INTEGER,
        UserID INTEGER REFERENCES users(Id),
        Name VARCHAR(1000) CHARACTER SET utf8 COLLATE utf8_unicode_ci,

        PRIMARY KEY(ForumId, Id)
);

CREATE TABLE comments
(
        ForumId INTEGER,
        Id INTEGER,
        UserId INTEGER,
        PostID INTEGER REFERENCES posts(Id),
        Score INTEGER,
        Text TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci,

        PRIMARY KEY(ForumId, Id)
)ENGINE=MyISAM CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE postlinks
(
        ForumId INTEGER,
        Id INTEGER,
        PostID INTEGER REFERENCES posts(Id),
        RelatedPostId INTEGER REFERENCES posts(Id),
        LinkTypeId INTEGER,  -- 1, 3

        PRIMARY KEY(ForumId, Id)
);

CREATE TABLE votes
(
        ForumId INTEGER,
        Id INTEGER,
        PostID INTEGER REFERENCES posts(Id),
        VoteTypeId INTEGER, -- 1-13
        UserID INTEGER REFERENCES users(Id), -- only for VoteTypeId=5
        BountyAmount INTEGER,    -- only for VoteTypeId=9
        PRIMARY KEY(ForumId, Id)
);

CREATE INDEX idx_posts_forumid_id ON posts(ForumId, Id);
CREATE INDEX idx_posts_forumid_parentid ON posts(ForumId, ParentID);
CREATE INDEX idx_comments_forumid_postid ON comments(ForumId, PostID);
CREATE INDEX idx_users_forumid_id ON users(ForumId, Id);
