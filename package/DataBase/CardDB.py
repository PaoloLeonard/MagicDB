import logging
import psycopg2

# Name constants
CARD_ID = "card_id"
CARD_NAME = "card_name"
CARD_FOIL = "card_foil"
CARD_PROXY = "card_proxy"
CARD_FORMAT = "card_format"
CARD_EDITION = "card_edition"
CARD_TOTAL = "card_total"
CARD_ARG = [CARD_ID, CARD_NAME, CARD_FOIL, CARD_PROXY, CARD_FORMAT, CARD_EDITION, CARD_TOTAL]


class CardDB:
    """
    Class handling calls to the card database
    """
    def __init__(self, params):
        """
        Open the connection to the CardDB database
        :param params parameters used to open the database
        """
        self._conn = None
        try:
            # connect to the PostgreSQL server
            self._conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_table_cards(self):
        """Create tables in the PostgreSQL database"""
        command = (
            """
            CREATE TABLE cards (
                card_id SERIAL PRIMARY KEY, 
                card_name VARCHAR(255) NOT NULL,
                card_foil BOOLEAN NOT NULL,
                card_proxy BOOLEAN NOT NULL,
                card_format TEXT [] NOT NULL,
                card_edition VARCHAR(255) NOT NULL,
                card_total INTEGER DEFAULT 0,
                UNIQUE (card_id)
            )
            """
        )
        try:
            cur = self._conn.cursor()
            # create table one by one
            cur.execute(command)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            self._conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_card(self, card_name, card_foil, card_proxy, card_format, card_edition, nb_of_card):
        """Insert a card in the cardDB"""
        command = (
            """
                INSERT INTO cards(card_name, card_foil, card_proxy, card_format, card_edition, card_total)
                VALUES(%s, %s, %s, %s, %s, %s) RETURNING card_id;
                """
        )
        try:
            cur = self._conn.cursor()
            # add a row
            params = (card_name, card_foil, card_proxy, card_format, card_edition, nb_of_card,)
            cur.execute(command, params)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            self._conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_card_id(self, card_name, card_foil, card_proxy):
        """
        Get the id of the card specified with the name, the foilitude and if it is a proxy or not
        :param card_name the name of the card
        :param card_foil a boolean of whether the card is foil or not
        :param card_proxy a boolean of whether the card is a proxy or not
        """

        command = (
            """
                SELECT card_id
                FROM cards
                WHERE card_name = %s AND card_foil = %s AND card_proxy = %s
            """
        )
        card_id = None
        try:
            cur = self._conn.cursor()
            params = (card_name, card_foil, card_proxy,)
            cur.execute(command, params)
            card_id = cur.fetchone()
            logging.info("Card with ID {}".format(card_id))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)

        return card_id

    def get_card_info_by_id(self, card_id: int):
        """
        Get the info of a card specified by its ID
        :param card_id: id of the card
        :return: a dict with the info of the card
        """

        command = (
            """
                SELECT *
                FROM cards
                WHERE card_id = %s
            """
        )
        card_info = dict()
        try:
            cur = self._conn.cursor()
            cur.execute(command, (card_id,))
            card_info_tup = cur.fetchone()

            for i, arg in enumerate(CARD_ARG):
                card_info[arg] = card_info_tup[i]
            logging.info("Info of {} fetched".format(card_info["card_name"]))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)

        return card_info

    def get_card_info_by_name(self, card_name: str):
        """
        Get the info of a card specified by its name
        :param card_name: name of the card
        :return: a dict with the info of the card
        """

        command = (
            """
                SELECT *
                FROM cards
                WHERE cards.card_name = %s
            """
        )
        list_of_cards = list()
        card_info = dict()
        try:
            cur = self._conn.cursor()
            cur.execute(command, (card_name,))
            card_info_tup = cur.fetchone()

            while card_info_tup is not None:
                for i, arg in enumerate(CARD_ARG):
                    card_info[arg] = card_info_tup[i]
                list_of_cards.append(card_info.copy())
                card_info.clear()
                card_info_tup = cur.fetchone()

            logging.info("Info of {} fetched".format(card_name))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)

        return list_of_cards

    def add_total_card(self, card_id, quantity):
        """
        Add the quantity of the specified card
        :param card_id: id of the card
        :param quantity: quantity to add
        :return: True if updated, False otherwise
        """

        command = (
            """
                UPDATE cards
                SET card_total = %s
                WHERE cards.card_id = %s
            """
        )

        updated_nb = self.get_card_info_by_id(card_id)[CARD_TOTAL] + quantity

        try:
            cur = self._conn.cursor()
            cur.execute(command, (updated_nb, card_id,))

            logging.info("Quantity of {} updated to {}".format(card_id, updated_nb))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            return False

        return True

    def sub_total_card(self, card_id, quantity):
        """
        Substract the quantity of the specified card
        :param card_id: id of the card
        :param quantity: quantity to sub
        :return: True if updated, False otherwise
        """

        command = (
            """
                UPDATE cards
                SET cards.card_total = %s
                WHERE cards.card_id = %s
            """
        )

        updated_nb = self.get_card_info_by_id(card_id)[CARD_TOTAL] - quantity

        try:
            cur = self._conn.cursor()
            cur.execute(command, (updated_nb, card_id,))

            logging.info("Quantity of {} updated to {}".format(card_id, updated_nb))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            return False

        return True

    def close_connection(self):
        if self._conn is not None:
            self._conn.close()
            logging.info("CardDB connection closed.")
