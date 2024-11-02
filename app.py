from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для витрат
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    comment = db.Column(db.String(200), nullable=True)

# Модель для доходів
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    comment = db.Column(db.String(200), nullable=True)

# Ініціалізація бази даних
with app.app_context():
    db.create_all()

# Додавання витрат
@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.json
    new_expense = Expense(
        category=data['category'],
        amount=data['amount'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        comment=data.get('comment')
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Expense added successfully!"}), 201

# Додавання доходу
@app.route('/income', methods=['POST'])
def add_income():
    data = request.json
    new_income = Income(
        source=data['source'],
        amount=data['amount'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        comment=data.get('comment')
    )
    db.session.add(new_income)
    db.session.commit()
    return jsonify({"message": "Income added successfully!"}), 201

# Перегляд звітів
@app.route('/reports', methods=['GET'])
def get_report():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    expenses = Expense.query.filter(Expense.date.between(start_date, end_date)).all()
    income = Income.query.filter(Income.date.between(start_date, end_date)).all()

    total_expenses = sum(exp.amount for exp in expenses)
    total_income = sum(inc.amount for inc in income)
    balance = total_income - total_expenses

    return jsonify({
        "totalIncome": total_income,
        "totalExpenses": total_expenses,
        "balance": balance
    })

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)

