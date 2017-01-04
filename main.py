from ContentBasedFilter import ContentBasedFilter
from MysqlRepository import MysqlRepository
from config_loader import ConfigLoader

def main():

    # #load the app configuration
    # cfg = ConfigLoader()
    # config = cfg.get_config()
    #
    # print(config)

    # server = config.get('server')

    # run worker processes if conditions are met

    # start http server to serve incoming requests

    # generate CB-recommendations
    # implement age check
    recommender = ContentBasedFilter()
    repo = MysqlRepository()

    product_recommendations = recommender.generate_recommendations()

    for rec in product_recommendations:
        repo.populate_data(rec)

    # generate Association Rules
    # implement age check






if __name__ == "__main__":
    main()
