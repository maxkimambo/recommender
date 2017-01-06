from BackgroundWorker import BackgroundWorker


def main():

    # #load the app configuration
    # cfg = ConfigLoader()
    # config = cfg.get_config()
    #
    # print(config)

    # server = config.get('server')

    # run worker processes if conditions are met
    bgw = BackgroundWorker()
    # generate CB-recommendations
    # implement age check
    bgw.calculate_content_based_similarity()

    # generate Association Rules
    # implement age check
    bgw.generate_associative_rules()

    # start http server to serve incoming requests


if __name__ == "__main__":
    main()
