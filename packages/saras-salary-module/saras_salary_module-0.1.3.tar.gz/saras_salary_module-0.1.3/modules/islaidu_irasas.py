from modules.irasas import Irasas

class IslaiduIrasas(Irasas):
  def __init__(self, suma, atsiskaitimo_budas, isigyta_preke_paslauga):
    super().__init__(suma)
    self.atsiskaitimo_budas = atsiskaitimo_budas
    self.isigyta_preke_paslauga = isigyta_preke_paslauga

  def __str__(self):
    return f'Islaidos - Suma {self.suma}; Atsiskaitymo budas: {self.atsiskaitimo_budas}; Isigyta preke/paslauga: {self.isigyta_preke_paslauga}'