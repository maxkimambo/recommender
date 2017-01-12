from BackgroundWorker import BackgroundWorker
from UserRecommender import UserRecommender
import threading
from multiprocess import Process
from log import Logger
import sys
import getopt


def usage():
    print("-------------------------------------------------------------------")
    print('usage..')
    print('      -u or --update to rebuild the similarity model')
    print('      -r or --recommend to rebuild the recommendations database')
    print('      -h or --help to display this message')
    print("-------------------------------------------------------------------")


def main(sargs):
    bgw = BackgroundWorker()
    ur = UserRecommender()

    def start_cb_background_worker():
        log.debug("Started CB based model generation in the background process")
        cb_process = Process(target=bgw.calculate_content_based_similarity)
        cb_process.start()

    def start_ar_background_worker():
        log.debug("Started Association rules mining in the background process.")
        ar_process = Process(target=bgw.generate_associative_rules)
        ar_process.start()

    def update_recommendations_cb():
        log.debug("Started updating recommendations based on  Collaborative Filtering in the background process.")
        cb = Process(target=ur.process_cb_recommendations)
        cb.start()

    def update_recommendations_ar():
        log.debug("Started updating recommendations based on  Association rules mining in the background process.")
        ar = Process(target=ur.process_ar_recommendations)
        ar.start()

    log = Logger()

    ## Parsing command line options
    long_options = ["update", "ar", "cb", "recommend=", "help"]
    short_options = "urh"
    try:
        opts, arg = getopt.getopt(sargs, short_options, long_options)
        for opt in opts:
            if opt[0] in ('-u', '--update'):
                start_cb_background_worker()
                start_ar_background_worker()
            elif opt[0] in ('-r', '--recommend'):
                update_recommendations_cb()
                update_recommendations_ar()
            elif opt[0] in ('-h', '--help'):
                usage()
            elif opt[0] in ('--ar'):
                start_ar_background_worker()
            elif opt[0] in ('--cb'):
                start_cb_background_worker()
            else:
                usage()
    except getopt.GetoptError:
        print('error')
        usage()
        sys.exit(2)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
