# Method 1: Using set()
def find_duplicates_using_set(arr):
    return list(set([x for x in arr if arr.count(x) > 1]))

# Method 2: Using count method
def find_duplicates_using_count(arr):
    duplicates = []
    for i in range(len(arr)):
        if arr[i] not in duplicates:  # Agar element already duplicates list mein nahi hai
            if arr.count(arr[i]) > 1:  # Check karo ki element ki frequency 1 se jyada hai
                duplicates.append(arr[i])
    return duplicates

# Testing the code
if __name__ == "__main__":
    # Test array
    arr = [1, 2, 3, 2, 4, 5, 5, 6, 3]
    
    print("Original Array:", arr)
    print("Duplicates using set method:", find_duplicates_using_set(arr))
    print("Duplicates using count method:", find_duplicates_using_count(arr))
    print("lubna")
    print("obaid")