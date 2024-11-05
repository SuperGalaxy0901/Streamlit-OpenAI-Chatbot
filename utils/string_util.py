
def find_positions_multiple(text, start_substring, end_substring):  
    positions = []  
    start_idx = 0  
    while True:  
        start = text.find(start_substring, start_idx)  
        if start == -1:  
            break  
        end = text.find(end_substring, start + len(start_substring))  
        if end == -1:  
            break  
        positions.append((start, end + len(end_substring)))  # Adjust end position to include end_substring  
        start_idx = end + len(end_substring)  
    return positions  