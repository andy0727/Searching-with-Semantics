import parser
import db
import TMIndex
import os
import sys
import getopt

class Usage(Exception):
    def __init__(self, msg):
    	Usage.msg = msg

def main(argv, *args, **kwargs):
    # if argv is None:
    #     argv = sys.argv
    # try:
    #     try:
    #         opts, args = getopt.getopt(argv[1:], "k:i:n:",[])
    #         if opts[0][0] == "-k":
    #             keyword = opts[0][1]
    #         else:
    #             raise Usage("wrong options\n")
    #         if opts[1][0] == "-i":
    #             ForumId = opts[1][1]
    #         if opts[2][0] == "-n":
    #             SiteName = opts[2][1]
    #         #print opts
    #     except Exception, e:
    #         print >>sys.stderr ,e
    #         raise Usage(e) 
    # except Usage, err:
    #     print >>sys.stderr, "Must specify -k keyword"
    #     return 2
    import argparse
    arg_parser = argparse.ArgumentParser(description='Search data from database')
    arg_parser.add_argument('-k',  nargs='+',help='Keyword to search')
    args = arg_parser.parse_args()
    # print args
    if args.k is None:
        arg_parser.print_help()
        return
    keywords =args.k 
    print str(keywords)
    path = os.path.join('.', 'data', str(keywords))
    txtFilePath = os.path.join(path, str(keywords) + '.txt')
    csvFilePath = os.path.join(path, str(keywords) + '.csv')
    try:
        os.mkdir(path)
    except OSError:
        pass
    try:
        line_tuple = parser.create_corpus(keywords, None, txtFilePath)
        parser.create_csv(line_tuple, csvFilePath)
    except Exception, e:
        print >>sys.stderr, e, Exception
        return 2

if __name__ == "__main__":
    main(sys.argv)