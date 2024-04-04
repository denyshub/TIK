import math


def convert_file_to_bits(file_name):
    with open(file_name, "r") as file:
        text = file.read()

    binary_representation = []
    for char in text:
        ascii_code = ord(char)
        binary_code = bin(ascii_code)[2:].zfill(8)
        for bit in binary_code:
            binary_representation.append(int(bit))

    return binary_representation


def coder(binary_representation):
    check_bits_indexes = []
    for i in range(1, len(binary_representation)):
        if math.log2(i).is_integer():
            check_bits_indexes.append(i)

    # print(check_bits_indexes)

    check_bits_values = {key: 0 for key in check_bits_indexes}  # Initialize values to 0
    # print("Initial check bit values:", check_bits_values)

    for i in check_bits_indexes:
        for j in range(i - 1, len(binary_representation), i * 2):
            for k in range(i):
                if j + k < len(binary_representation):
                    check_bits_values[i] ^= binary_representation[j + k]

    text = ''.join(str(part) for part in binary_representation)
    print('Primary text: ', binary_to_words(text))

    for key, value in check_bits_values.items():
        binary_representation.insert(key, value)

    return binary_representation


def binary_to_words(binary_string):
    bytes_list = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
    ascii_list = [chr(int(byte, 2)) for byte in bytes_list]
    return ''.join(ascii_list)


def write_code_to_file(file_name, data):
    string_data = ''.join(str(bit) for bit in data)
    with open(file_name, 'w') as file:
        file.write(string_data)


def decoder(file_name):
    with open(file_name, "r") as file:
        text = file.read()

    bits_array = []
    for char in text:
            bits_array.append(int(char))

    check_bits_indexes = [] # [1,2,4,8,16,32,64,128,256]
    for i in range(1, len(bits_array) + 1):
        if math.log2(i).is_integer():
            check_bits_indexes.append(i)

    array_to_check = []
    dad = []

    for i, bit in enumerate(bits_array):
        if i not in check_bits_indexes:
            array_to_check.append(bit)
        else:
            dad.append(bit)

    string = ''.join(str(nums) for nums in array_to_check)
    print('Test: ', binary_to_words(string))

    check_bits_values = {key: 0 for key in check_bits_indexes}  # Initialize values to 0

    for i in check_bits_indexes:
        for j in range(i - 1, len(array_to_check), i * 2):
            for k in range(i):
                if j + k < len(array_to_check):
                    check_bits_values[i] ^= array_to_check[j + k]

    error_bit = []
    for i in range(len(dad)):
        if dad[i] != check_bits_values[check_bits_indexes[i]]:
            print(check_bits_indexes[i])
            error_bit.append(check_bits_indexes[i])

    sum = 0
    for errors in error_bit:
        sum += errors
    print("error index: ", sum)
    # Correcting the error
    if sum:
        print("Errors detected at positions:", sum)
        array_to_check[sum - 1] = 1 if array_to_check[sum - 1] == 0 else 0
        print("Errors corrected.")
    else:
        print("No errors detected.")

    decoded_data = array_to_check

    # Convert decoded data back to text
    decoded_text = binary_to_words(''.join(str(bit) for bit in decoded_data))
    print("Decoded text:", decoded_text)


if __name__ == '__main__':

    binary = convert_file_to_bits('text.txt')
    coded_data = coder(binary)
    write_code_to_file('encodedfile.txt', coded_data)
    decoder('file_with_errors.txt')


