class DataInterface():

    def __init__(self):
        raise NotImplementedError

    def log_initial(self, uuid, symbol, is_vowel):
        raise NotImplementedError

    def log_folowup(self, uuid):
        raise NotImplementedError

    def symbol_aggregates(self, symbol):
        raise NotImplementedError

    def range_aggregates(self, lower, upper):
        raise NotImplementedError


class NullInterface(DataInterface):

    def __init__(self):
        pass

    def log_initial(self, uuid, symbol, is_vowel):
        pass

    def log_followup(self, uuid):
        pass

    def symbol_aggregates(self, symbol):
        pass

    def range_aggregates(self, lower, upper):
        pass
