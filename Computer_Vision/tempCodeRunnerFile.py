
    if isinstance(text_lines, list):
        combined = " ".join(text_lines)
    else:
        combined = str(text_lines)

    # --- Collector number detection ---
    num_match = re.search(r"\b(\d{1,4})\s*/\s*\d{1,4}\b", combined)  # e.g. 131/272
    if not num_match:
        num_match = re.search(r"[CUHRMT]\s*0*(\d{1,4})", combined)  # e.g. C 0210
    col_num = int(num_match.group(1)) if num_match else None

    # --- Set code detection (line containing capital 'EN') ---
    set_code = "UNKNOWN"
    for line in reversed(text_lines):
        if "EN" in line:
            clean_line = re.sub(r"[^A-Z0-9]", "", line.upper())  # keep letters and digits
            if "EN" in clean_line:
                set_code = clean_line[:3]  # first 3 characters (preserving digits)
                break

    print(f"✅ Set Code: {set_code}, Collector Number: {col_num}")
    return set_code, col_num