from ContentBasedFilter import ContentBasedFilter
from MysqlRepo import MysqlRepo
import json
from config_loader import ConfigLoader

def main():

    #load the app configuration
    cfg = ConfigLoader()
    config = cfg.get_config()
    server = config.get('server').get('host')
    port = config.get('server').get('port')
    print(port)

    # server = config.get('server')

    # run worker processes if conditions are met

    # start http server to serve incoming requests

    # recommender = ContentBasedFilter()
    # repo = MysqlRepo()
    #
    # product_recommendations = recommender.generate_recommendations()
    #
    # for rec in product_recommendations:
    #     repo.populate_data(rec)




if __name__ == "__main__":
    main()
