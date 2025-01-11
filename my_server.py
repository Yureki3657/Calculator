from flask import Flask, redirect, render_template , url_for, request, flash
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Numbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, nullable=True)
    operator = db.Column(db.Integer, nullable=True)
    
    def __repr__(self): 
        return f'<Numbers {self.num, self.operator}>'

with app.app_context():
    db.drop_all()
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def index():
    print(111)
    
    if request.method == 'POST':
        data = request.get_json()
        val = data.get('value')
        
        print(f"Received value: {val}")

        new_data = Numbers(operator=val)
        db.session.add(new_data)
        db.session.commit()
        print("Data saved to database")
        
        return {"status": "success"}, 200
    
    else:
        print(444)
        return render_template('index.html')
        


@app.route('/input', methods=['POST', 'GET'])
def input():
    if request.method == 'POST':

        val1 = int(request.form['val1']) 
        val2 = int(request.form['val2'])

        data = Numbers.query.order_by(Numbers.id.desc()).first()
        
        if data is None:  # Nếu không có bản ghi nào trong bảng Numbers
            flash("Error: No previous operation found. Please try again.", "error")
            return render_template('index.html')

        sign = data.operator

        match sign:
            case 1: #plus
                result = val1 + val2
            case 2: #minus
                result = val1 - val2
            case 3: #multi
                result = val1 * val2
            case _: #div
                if val2 == 0:
                    flash("Error: Division by zero is not allowed. Please enter a valid for second number,", "error")
                    return render_template('input.html')
                result = val1 / val2

        data.num = result
        db.session.commit()
        
        return redirect(url_for('result'))
    else:
        return render_template('input.html')


@app.route('/result', methods=['POST', 'GET'])
def result():

    if request.method == 'POST':
        return redirect(url_for('home'))
    else:
            
        number = Numbers.query.order_by(Numbers.id.desc()).first()
        
        if number:
            result = number.num
            
            while number:
                db.session.delete(number)
                db.session.commit()
                number = Numbers.query.first()

            return render_template('result.html', result=result)
        
        else:
            return render_template('result.html', result="No results found")
    
    

if __name__ == '__main__':
    app.run(debug = True)

    