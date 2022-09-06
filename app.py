from flask import Flask,render_template,request,url_for,redirect
import pymysql

app = Flask(__name__)

connection = pymysql.connect(host="localhost",port=3306,user="root",passwd="",database="crud")


@app.route('/')
def index():
    cur = connection.cursor()
    cur.execute("select * from employees ORDER BY id;")
    data = cur.fetchall()
    print(data)
    cur.close()
    return render_template('index.html',employees_data = data)

@app.route('/search_by_id',methods=['GET'])
def ret():
    args = request.args
    id = args.get("id")
    if id == "":
        return redirect(url_for("index"))
    
    cur = connection.cursor()
    cur.execute("select * from employees Where id={0};".format(id))
    data = cur.fetchall()
    cur.close()
    return render_template('index.html',employees_data = data)

@app.route('/insert',methods=['POST'])
def form():
    if request.method=="POST":
        cur_id = connection.cursor()
        cur_id.execute("select id from employees order by id desc limit 0,1")
        max_id_list = cur_id.fetchall()
        if(len(max_id_list)==0):
            id=0
        else:
            id = max_id_list[0][0]
        
        cur_id.close()
        
        name = request.form.get('fname')
        email = request.form.get('femail')
        phone_no = request.form.get('fphone')

        cur = connection.cursor()
        cur.execute("INSERT into employees(id,name,email,phone) VALUES({0},'{1}','{2}','{3}')".format(id+1,name,email,phone_no))
        connection.commit()
        cur.close()


        return redirect("/")

@app.route('/delete', methods = ['GET'])
def delete():
    args = request.args
    id_data = args.get("id")
    cur = connection.cursor()
    cur.execute("DELETE FROM employees WHERE id=%s", (id_data,))
    connection.commit()

    return redirect('/')

@app.route('/update/<string:id_data>', methods = ['POST'])
def update(id_data):
    name = request.form.get('fname')
    email = request.form.get('femail')
    phone_no = request.form.get('fphone')
    cur = connection.cursor()
    cur.execute("""UPDATE employees SET name=%s, email=%s, phone=%s WHERE id=%s""", (name, email, phone_no, id_data))
    connection.commit()

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
