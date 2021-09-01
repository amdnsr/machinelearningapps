import base64

class BinaryData_Base64_Utils:
    @staticmethod
    def binary_data_to_base64String(binary_data, encoding_method='utf-8'):
        base64_encoded_data = base64.b64encode(binary_data) # this is 64 bit binary-like thing, not a string yet
        base64String = base64_encoded_data.decode(encoding_method)
        return base64String
    
    @staticmethod
    def base64String_to_binary_data(base64String, encoding_method='utf-8'):
        base64_encoded_data = base64String.encode(encoding_method)
        binary_data = base64.decodebytes(base64_encoded_data)
        return binary_data
    
    @staticmethod
    def binaryFile_to_base64StringFile(binaryFilePath, base64StringFilePath, encoding_method='utf-8'):
        with open(binaryFilePath, 'rb') as binary_file:
            binary_file_data = binary_file.read()
            base64String = BinaryData_Base64_Utils.binary_data_to_base64String(binary_file_data)

        with open(base64StringFilePath, 'w') as base64String_file:
            base64String_file.write(base64String)
        
    @staticmethod
    def base64StringFile_to_binaryFile(base64StringFilePath, binaryFilePath, encoding_method='utf-8'):
        with open(base64StringFilePath, 'r') as base64String_file:
            base64String = base64String_file.read()
            binary_file_data = BinaryData_Base64_Utils.base64String_to_binary_data(base64String)
        
        with open(binaryFilePath, 'wb') as binary_file:
            binary_file.write(binary_file_data)

    def binaryFile_to_base64String(binaryFilePath, encoding_method='utf-8'):
        with open(binaryFilePath, 'rb') as binary_file:
            binary_file_data = binary_file.read()
            base64String = BinaryData_Base64_Utils.binary_data_to_base64String(binary_file_data)
        return base64String
    
    def base64StringFile_to_binary_data(base64StringFilePath, encoding_method='utf-8'):
        with open(base64StringFilePath, 'r') as base64String_file:
            base64String = base64String_file.read()
            binary_file_data = BinaryData_Base64_Utils.base64String_to_binary_data(base64String)
        return binary_file_data        

    def binary_data_to_base64StringFile(binary_data, base64StringFilePath, encoding_method='utf-8'):
        base64String = BinaryData_Base64_Utils.binary_data_to_base64String(binary_data)
        with open(base64StringFilePath, 'w') as base64String_file:
            base64String_file.write(base64String)

    def base64String_to_binaryFile(base64String, binaryFilePath, encoding_method='utf-8'):
        binary_file_data = BinaryData_Base64_Utils.base64String_to_binary_data(base64String)
        
        with open(binaryFilePath, 'wb') as binary_file:
            binary_file.write(binary_file_data)


if __name__ == "__main__":
    input_binaryFile = 'input.png'
    input_base64StringFile = "input.txt"
    output_binaryFile = 'output.png'
    output_base64StringFile = "output.txt"

    BinaryData_Base64_Utils.binaryFile_to_base64StringFile(input_binaryFile, output_base64StringFile)
    BinaryData_Base64_Utils.base64StringFile_to_binaryFile(input_base64StringFile, output_binaryFile)