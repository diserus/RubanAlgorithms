import random

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j + 1]:
                print(f"  Меняем arr[{j}] = {arr[j]} с arr[{j+1}] = {arr[j+1]}")
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                print(arr,'\n')
                swapped = True
        if not swapped:
            break
    return arr

def select_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        print(f"  Меняем arr[{i}] = {arr[i]} с arr[{min_idx}] = {arr[min_idx]}")
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        print(arr,'\n')
    return arr

def format_blocks(arr, block_size):
    blocks = [" ".join(map(str, arr[i:i + block_size])) for i in range(0, len(arr), block_size)]
    return " | ".join(blocks)


def merge_sort(arr):
    n = len(arr)
    print(f"Исходный массив: {arr}")
    print("По 1: ",format_blocks(arr, 1))

    width = 1
    while width < n:
        for left in range(0, n, 2 * width):
            mid = min(left + width, n)
            right = min(left + 2 * width, n)

            left_block = arr[left:mid]
            right_block = arr[mid:right]

            merged = []
            i, j = 0, 0
            while i < len(left_block) and j < len(right_block):
                if left_block[i] <= right_block[j]:
                    merged.append(left_block[i])
                    i += 1
                else:
                    merged.append(right_block[j])
                    j += 1
            merged.extend(left_block[i:])
            merged.extend(right_block[j:])
            arr[left:right] = merged

        width *= 2
        print(f"По {width}: ",format_blocks(arr, width))

    print()
    return arr


random_array = [random.randint(0, 100) for _ in range(10)]

print("Исходный массив:", random_array)

sorted_array = bubble_sort(random_array.copy())
print("\nBubble Sort:\n\n", sorted_array)

sorted_array2 = select_sort(random_array.copy())
print("\nSelect Sort:\n",sorted_array2)
print("\n\n")
sorted_array3 = merge_sort(random_array.copy())
print("\nMerge Sort:\n",sorted_array3)