from modules.pajamu_irasas import PajamuIrasas
from modules.islaidu_irasas import IslaiduIrasas

class Biudzetas:
  zurnalas = []

  def prideti_irasa(self, irasas):
    self.zurnalas.append(irasas)

  def gauti_balansa(self):
    rezultatas = 0

    for irasas in self.zurnalas:
      if isinstance(irasas, PajamuIrasas):
        rezultatas += irasas.suma
      elif isinstance(irasas, IslaiduIrasas):
        rezultatas -= irasas.suma

    return rezultatas

  def gauti_ataskaita(self):
    for irasas in self.zurnalas:
      print(irasas)
