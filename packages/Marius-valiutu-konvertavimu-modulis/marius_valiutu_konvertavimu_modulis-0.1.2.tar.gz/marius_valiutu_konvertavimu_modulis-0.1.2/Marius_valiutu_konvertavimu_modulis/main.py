from Marius_currency_converter_module.convert import konvertuojam_valiuta

if __name__ == '__main__':
    suma = float(input("Įveskite sumą: "))
    is_valiutos = input("Įveskite valiutą, iš kurios konvertuosite (pvz., 'EUR'): ")
    i_valiuta = input("Įveskite valiutą, į kurią konvertuosite (pvz., 'USD'): ")
    converted_amount = konvertuojam_valiuta(suma, is_valiutos, i_valiuta)
    print(f"{suma} {is_valiutos} yra lygu {converted_amount:.2f} {i_valiuta}.")