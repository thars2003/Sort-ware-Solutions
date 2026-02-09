def live_log(card_counter, name, color, type, price, sort_by, sort_value, bin,bin_mapping):
    yield {
            "card_counter": card_counter,
            "name": name,
            "subtype": "Color",
            "subtype_value": color,
            "type": type,
            "price": price,
            "sort_by": sort_by,
            "sort_value": sort_value,
            "bin": bin,
            "bin_mapping": bin_mapping
        }