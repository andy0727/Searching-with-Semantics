import parser
import os
import TMIndex


ForumId = 0
LastForumId = 0
mydirs = []
for root, dirs, files in os.walk("./"):
	for file in files:
		if file.endswith(".xml"):
			filename= file
			mydir = os.path.dirname(os.path.join(root, file))
			if mydir not in mydirs:
				ForumId += 1
				mydirs.append(mydir) 

			print filename, ForumId
			print mydir
			if ForumId <= LastForumId:
				continue
			parser.parse(os.path.join (root,file), ForumId)

if LastForumId == 0:
	TMIndex.init()
TMIndex.create(LastForumId)