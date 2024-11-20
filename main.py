from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'perpustakaan'

mysql = MySQL(app)

@app.route('/buku', methods=['POST', 'GET'])
def buku():
    # kode yang dijalankan jika method pada request berupa POST
    if request.method == 'POST':
        # mendapatkan data dari request body
        data = request.json

        print(data)

        penulis = data.get('penulis')
        judul = data.get('judul')

        # tulis query (pake procedure)
        query = "INSERT INTO buku (judul, penulis) VALUES (%s, %s)"
        # CALL tambah_buku(%s, %s)

        # menjalankan query yang ditulis
        cursor = mysql.connection.cursor()
        cursor.execute(query, (judul, penulis))
        mysql.connection.commit()
        cursor.close()

        # return response (jsonify untuk mengembalikan data dalam bentuk json)
        return jsonify({'message': 'success'})
    
    # kode yang dijalankan jika method pada request berupa GET
    elif request.method == 'GET':

        # Blok kode untuk menjalankan query
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM buku")
        data = cursor.fetchall()

        # ubah data dari list (karena fetchall() return list) ke dictionary (seperti json))
        data = [{'id': row[0], 'judul': row[1], 'penulis': row[2]} for row in data]
        cursor.close()

        # return response
        return jsonify({'message': 'success', 'data': data})

# tambah parameter (<int:id>) id /buku/3 -> id = 3
@app.route('/buku/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def buku_spesifik(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM buku WHERE id = %s", (id,))
        data = cursor.fetchone()
        cursor.close()
        if not data:
            return jsonify({'message': 'not found'})
        data = {'id': data[0], 'judul': data[1], 'penulis': data[2]}
        return jsonify({'message': 'success', 'data': data})

    elif request.method == 'PUT':
        data = request.json
        penulis = data.get('penulis')
        judul = data.get('judul')

        query = "UPDATE buku SET judul = %s, penulis = %s WHERE id = %s"

        cursor = mysql.connection.cursor()
        cursor.execute(query, (judul, penulis, id))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'success'})

    elif request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM buku WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'success'})





if __name__ == '__main__':
    app.run(debug=True)