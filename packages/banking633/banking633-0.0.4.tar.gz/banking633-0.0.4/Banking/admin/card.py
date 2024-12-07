class Card(object):
    def __init__(self, cardId, cardPasswd, cardMoney, cardLock=False):
        self.cardId = cardId
        self.cardPasswd = cardPasswd
        self.cardMoney = cardMoney
        self.cardLock = cardLock
      

    def to_dict(self):
        return {
            'cardId': self.cardId,
            'cardPasswd': self.cardPasswd,
            'cardMoney': self.cardMoney
        }


class User(object):
    def __init__(self, name, idCard, phone, card):
        self.name = name
        self.idCard = idCard
        self.phone = phone
        self.card = card

    def to_dict(self):
        return {
            'name': self.name,
            'idCard': self.idCard,
            'phone': self.phone,
            'card': self.card.to_dict()
        }