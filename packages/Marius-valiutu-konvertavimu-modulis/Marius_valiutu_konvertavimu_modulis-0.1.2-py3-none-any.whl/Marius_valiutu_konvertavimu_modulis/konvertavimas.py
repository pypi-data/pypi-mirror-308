from currency_converter import CurrencyConverter
def konvertuojam_valiuta(suma, is_valiutos, i_valiuta):
    konverteris = CurrencyConverter()
    return konverteris.convert(suma, is_valiutos, i_valiuta)