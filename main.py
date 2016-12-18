from tfidfRecommender import TfidfRecommender
from MysqlRepo import MysqlRepo

def main():

    recommender = TfidfRecommender()
    repo = MysqlRepo()

    product_recommendations = recommender.generate_recommendations()

    for rec in product_recommendations:
        repo.populate_data(rec)




if __name__ == "__main__":
    main()
