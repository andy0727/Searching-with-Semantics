import argparse
import process as ps
import os
import re
import sys
def main(argv, *args, **kwargs):

    arg_parser = argparse.ArgumentParser(description='Topic Modeling on StackExchange Data')
    arg_parser.add_argument('-r',type = int,help='rebuild the corpus')
    #arg_parser.add_argument('-k',  nargs='+',help='Keyword to search')
    
    args = arg_parser.parse_args()
    if args.r is None:
        arg_parser.print_help()
        return

    file_name= raw_input("Please enter something:")   
    keywords = file_name.split();
    print keywords

    # extract the topics
    
    ps.extract_topics(keywords, args.r)
    path = os.path.join('.', 'data', file_name)
    models_topics_list= ps.save_top_words_for_models(path, file_name)
    two_topic = models_topics_list[0]

    not_done = True  

    while not_done:
        path = os.path.join('.', 'data', file_name)
        txtFilePath = os.path.join(path, file_name+ '.txt')
        for topic in two_topic:
            print topic

        option = raw_input("type the keyword or choose the topic:\n")

        if option == '-1':
            not_done = False

        else: 
            if (option in two_topic[0]) or (option in two_topic[1]):
                #keywords.append(option)  
                #file_name += " "+ option
                print "find the exact keyword: "+ file_name+ " "+ option
                ps.update_corpus(txtFilePath, [option])
                ps.extract_topics(keywords, 0)
                models_topics_list= ps.save_top_words_for_models(path, file_name)
                two_topic = models_topics_list[0]

            if option == "1":
                two_topic = ps.group_topics(file_name, two_topic[0])
                ps.update_corpus(txtFilePath, two_topic[0])
                
                
            if option == "2":
                two_topic = ps.group_topics(file_name,  two_topic[1])
                ps.update_corpus(txtFilePath, two_topic[1])

     
            #print "invalid input, try again"
        
    #make_lda_model(corpus, 100, os.path.join(path, 'models', file_name + '_k=100,a=0.5'), alpha=50.0/100)

if __name__ == '__main__':
    main(sys.argv)