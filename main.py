from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

def money(x: Decimal) -> Decimal:
    # Round to nearest cent
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def parse_decimal(prompt: str, allow_exit: bool = True):
    while True:
        s = input(prompt).strip().lower()
        if allow_exit and s in {"done", "exit"}:
            return None
        # Allow "$", commas
        s_clean = s.replace("$", "").replace(",", "")
        try:
            return Decimal(s_clean)
        except (InvalidOperation, AttributeError):
            print("Please enter a valid number, or type 'done'.")

def main():
    print("Enter the names to split the check with. Type 'done' when finished.")
    customers = []
    while True:
        name = input("Enter a name (or 'done'): ").strip()
        if not name:
            continue
        if name.lower() in {"done", "exit"}:
            break
        customers.append({"name": name, "subtotal": Decimal("0.00")})

    if not customers:
        print("No participants entered. Exiting.")
        return

    print("\nFor each person, enter each item price. Type 'done' when finished with that person.")
    for c in customers:
        while True:
            val = parse_decimal(f"  {c['name']} item price (or 'done'): ")
            if val is None:
                break
            if val < 0:
                print("  Price cannot be negative.")
                continue
            c["subtotal"] += val

    # Guard against all-zero subtotals
    total_subtotal = sum(c["subtotal"] for c in customers)
    if total_subtotal == 0:
        print("\nAll subtotals are zero. Nothing to split.")
        return

    # Tax rate
    tax_rate = None
    while tax_rate is None:
        tr = input("\nEnter the tax rate as a decimal (e.g., 0.1025 for 10.25%): ").strip()
        try:
            tax_rate = Decimal(tr)
            if tax_rate < 0:
                print("Tax rate cannot be negative.")
                tax_rate = None
        except InvalidOperation:
            print("Please enter a valid decimal tax rate.")

    # Tip total (absolute amount for the whole bill)
    tip_total = None
    while tip_total is None:
        t = input("Enter the TOTAL tip amount for the bill (e.g., 20): ").strip()
        t_clean = t.replace("$", "").replace(",", "")
        try:
            tip_total = Decimal(t_clean)
            if tip_total < 0:
                print("Tip cannot be negative.")
                tip_total = None
        except InvalidOperation:
            print("Please enter a valid number.")

    print("\n--- Amounts Owed ---")
    for c in customers:
        subtotal = c["subtotal"]
        tax = money(subtotal * tax_rate)
        # Tip allocated proportionally to pre-tax subtotal
        tip_share = money((subtotal / total_subtotal) * tip_total)
        total_owed = money(subtotal + tax + tip_share)
        print(f"{c['name']} owes ${total_owed}  "
              f"(subtotal ${money(subtotal)}, tax ${tax}, tip ${tip_share})")

if __name__ == "__main__":
    main()
