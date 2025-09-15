from decimal import Decimal

a = Decimal('0.3')
b = Decimal('0.2')
print(a - b)  # 0.1


def safe_sub(a: float, b: float):
    a_dec = Decimal(str(a))
    b_dec = Decimal(str(b))

    # Вычитание и округление
    result = a_dec - b_dec
    return float(result)