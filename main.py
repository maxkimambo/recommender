from BackgroundWorker import BackgroundWorker
import threading
import logging
import time
def main():

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                        )

    # server = config.get('server')
    # run worker processes if conditions are met
    bgw = BackgroundWorker()
    # generate CB-recommendations
    # implement age check
    #cb_thread = threading.Thread(name="CB filter thread", target=bgw.calculate_content_based_similarity)

    # generate Association Rules
    # implement age check
    ar_thread = threading.Thread(name="AR thread", target=bgw.generate_associative_rules)

    #cb_thread.start()
    ar_thread.start()
    # start http server to serve incoming requests

if __name__ == "__main__":
    main()
