from flask import Flask, render_template, request

app = Flask(__name__)

# Rail Fence Cipher Encryption
def encrypt_rail_fence(plaintext, key):
    rail = [['\n' for i in range(len(plaintext))] for j in range(key)]
    
    dir_down = False
    row, col = 0, 0
    
    for i in range(len(plaintext)):
        if (row == 0) or (row == key - 1):
            dir_down = not dir_down
        
        rail[row][col] = plaintext[i]
        col += 1
        
        if dir_down:
            row += 1
        else:
            row -= 1
    
    encrypted_text = []
    for i in range(key):
        for j in range(len(plaintext)):
            if rail[i][j] != '\n':
                encrypted_text.append(rail[i][j])
    
    return "".join(encrypted_text)

# Rail Fence Cipher Decryption
def decrypt_rail_fence(ciphertext, key):
    rail = [['\n' for i in range(len(ciphertext))] for j in range(key)]
    
    dir_down = None
    row, col = 0, 0
    
    for i in range(len(ciphertext)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        
        rail[row][col] = '*'
        col += 1
        
        if dir_down:
            row += 1
        else:
            row -= 1
    
    index = 0
    for i in range(key):
        for j in range(len(ciphertext)):
            if rail[i][j] == '*' and index < len(ciphertext):
                rail[i][j] = ciphertext[index]
                index += 1
    
    result = []
    row, col = 0, 0
    for i in range(len(ciphertext)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        
        if rail[row][col] != '*':
            result.append(rail[row][col])
            col += 1
        
        if dir_down:
            row += 1
        else:
            row -= 1
    
    return "".join(result)

# Flask route
@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    mode = None
    if request.method == 'POST':
        mode = request.form['mode']
        text = request.form['text']
        key = int(request.form['key'])
        
        if mode == 'encrypt':
            result = encrypt_rail_fence(text, key)
        elif mode == 'decrypt':
            result = decrypt_rail_fence(text, key)
        else:
            result = "Invalid mode selected."
    
    return render_template('index.html', result=result, mode=mode)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
