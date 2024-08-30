def calculate_monthly_payment(amount, interest_rate, years):
    monthly_rate = interest_rate / 12 / 100
    total_payments = years * 12
    monthly_payment = (amount * monthly_rate) / (
        1 - (1 + monthly_rate) ** -total_payments
    )
    return round(monthly_payment, 2)
