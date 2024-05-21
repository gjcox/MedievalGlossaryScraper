import argparse, json, io
from typing import List, Dict

PLAINTEXT = 'plaintext'
MEANINGS = 'meanings'
SYNONYM = 'synonymOf'
MERGED = 'merged'
# The placeholder is to force unwanted entries to the end of the list
DELETION_PLACEHOLDER = "~"

def combine_entries(one: Dict[str,str], two: Dict[str, str]):
    combined_entry = {PLAINTEXT: one[PLAINTEXT], MERGED: True}
    # Each entry should have either a 'meanings' key or a 'synonymOf' key
    # If both entries have meanings then the list are combined
    # In the event that both only have synonymOf keys, the latter is lost
    # Otherwise the combined entry will have both meanings and one synonymOf
    try:
        combined_entry[MEANINGS] = one[MEANINGS]
        try: 
            combined_entry[MEANINGS] += two[MEANINGS]
        except: 
            combined_entry[SYNONYM] = two[SYNONYM]
            pass
    except KeyError:
        try:
            combined_entry[SYNONYM] = one[SYNONYM]
        except KeyError: 
            pass
        try: 
            combined_entry[MEANINGS] = two[MEANINGS]
        except KeyError: 
            print(f"{one[PLAINTEXT]} has lost synonymOf({two[SYNONYM]}): {combined_entry}")
            pass
    return combined_entry


def glossary_merge_sort_inner(arr: List[Dict[str, str]], l: int, m: int, r: int):
    n1 = m - l + 1
    n2 = r - m
 
    # create temp arrays
    L = [0] * (n1)
    R = [0] * (n2)
 
    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        L[i] = arr[l + i]
 
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
 
    # Merge the temp arrays back into arr[l..r]
    i = 0     # Initial index of first subarray
    j = 0     # Initial index of second subarray
    k = l     # Initial index of merged subarray
 
    while i < n1 and j < n2:
        if L[i][PLAINTEXT] < R[j][PLAINTEXT]:
            arr[k] = L[i]
            i += 1
        elif L[i][PLAINTEXT] == R[j][PLAINTEXT]:
            arr[k] = combine_entries(L[i], R[j])
            i += 1
            j += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
 
    # Copy the remaining elements of L[], if there
    # are any
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
 
    # Copy the remaining elements of R[], if there
    # are any
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

    # For each merged pair of entries there is a 
    # list element to be deleted from the array
    # Those elements are marked for deletion here 
    while k <= r: 
        arr[k] = {PLAINTEXT: DELETION_PLACEHOLDER}
        k += 1
 
# l is for left index and r is right index of the
# sub-array of arr to be sorted
def glossary_merge_sort(arr, l: int = 0, r: int | None = None):
    if r is None:
        r = len(arr) - 1
    if l < r:
 
        # Same as (l+r)//2, but avoids overflow for
        # large l and h
        m = l+(r-l)//2
 
        # Sort first and second halves
        glossary_merge_sort(arr, l, m)
        glossary_merge_sort(arr, m+1, r)
        glossary_merge_sort_inner(arr, l, m, r)

def merge_glossaries(one: io.TextIOWrapper, two: io.TextIOWrapper, output: io.TextIOWrapper):
    # Load JSON entries from source one
    entry_list_one = [json.loads(line) for line in one]
    # Load JSON entries from source two
    entry_list_two = [json.loads(line) for line in two]
    # Sort and merge glossaries  
    entry_list = [*entry_list_one, *entry_list_two] 
    glossary_merge_sort(entry_list)
    # Pop from the combined list to make up for merged entries 
    while entry_list[-1][PLAINTEXT] == DELETION_PLACEHOLDER:
        entry_list.pop()
    # Write processed entries to output file
    output.writelines(json.dumps(entry, ensure_ascii=False) + '\n' for entry in entry_list)

def main():
    parser = argparse.ArgumentParser(description='Process a JSON-lines glossary file.')
    parser.add_argument("source1", type=argparse.FileType('r', encoding='UTF-8'), 
                        help="the first glossary file")
    parser.add_argument("source2", type=argparse.FileType('r', encoding='UTF-8'), 
                        help="the second glossary file")
    parser.add_argument("output", type=argparse.FileType('w', encoding='UTF-8'),
                        help="the file to write the merged glossary to")
    args = parser.parse_args()

    merge_glossaries(args.source1, args.source2, args.output)

    args.source1.close()
    args.source2.close()
    args.output.close()


if __name__ == "__main__":
    main()