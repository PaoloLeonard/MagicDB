if __name__ == '__main__':

    from package.DataBase.CardDB import CardDB
    from package.DataBase.config import config
    config = config()
    cardDB = CardDB(config)
    print(cardDB.insert_card("unsettled-mariner", True, False, ['Modern'], 'MH1', 1))
    cardDB.close_connection()
