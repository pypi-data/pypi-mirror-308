from modules.irasas import Irasas

class PajamuIrasas(Irasas):
  def __init__(self, suma, siuntejas, papildoma_informacija):
    super().__init__(suma)
    self.siuntejas = siuntejas
    self.papildoma_informacija = papildoma_informacija

  def __str__(self):
    return f'Pajamos - Suma {self.suma}; Siuntejas: {self.siuntejas}; Papildoma info: {self.papildoma_informacija}'