import DataManager as dm
import mongo_repo as mr

def main():
    mongo_repo = mr()
    worker = dm(mongo_repo)
    worker.get_data()


if __name__ == "__main__":
    main()
