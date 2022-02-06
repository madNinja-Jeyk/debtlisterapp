import os, sys
from flask import Flask, render_template, url_for, redirect, request, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "super_secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)

class Debtor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	debts = db.relationship('Debt', backref='debtor')
	total_amount = db.Column(db.Integer)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	def __repr__(self):
		return f"{self.name} (self.debts)"
class Debt(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	itemName = db.Column(db.String(100))
	quantity = db.Column(db.Integer)
	price = db.Column(db.Integer)
	total = db.Column(db.Integer)
	debtor_id = db.Column(db.Integer, db.ForeignKey('debtor.id'))
	def __repr__(self):
		return f"{self.debtor_id} ({self.itemName} {self.quantity} {self.price})"

@app.route('/',methods=['POST','GET'])
def home():
	if request.method == "POST":
		try:
			if request.form['adddebtor']:
				nm = request.form['nm']
				
				debtor = Debtor(name=nm, total_amount=0)
				try:
					db.session.add(debtor)
					db.session.commit()
					flash("Debtor added ")
					return redirect('/')
				except:
					return "Error"
		except:
			try:
				if request.form['save_debtor']:
					id = request.form['debtor_id']
					new_nm = request.form['new_nm']
					print(id, new_nm)
					
					debtor = Debtor.query.filter_by(id=id).first()
					debtor.name = new_nm
					db.session.commit()
						
					return redirect('/')
			except:
				if request.form['delete_debtor']:
					id = request.form['debtor_id']
					new_nm = request.form['new_nm']
					debtor = Debtor.query.filter_by(id=id).first()
					for debt in debtor.debts:
						db.session.delete(Debt.query.filter_by(id=debt.id).first())
					db.session.delete(debtor)
					db.session.commit()
					return redirect('/')
	else:
		debtors = Debtor.query.order_by(Debtor.date_added)
		debtorTitle = "My Debtors"
		context = {
			'debtors': debtors,
			'debtorTitle': debtorTitle
		}
		return render_template("home.html", ctx=context)

@app.route('/list/<debtor_id>',methods=['POST','GET'])
def list(debtor_id):
	try:
		debtor = Debtor.query.filter_by(id=debtor_id).first()
	except:
		return "Debtor not found"
	if request.method == 'POST':
		try: #try adding a debt
			if request.form['adddebt']:
				item = request.form['item']
				quan = request.form['qty']
				pr = request.form['price']
				ttl = int(pr) * int(quan)
				
				new_debt = Debt(itemName=item, quantity=quan, price=pr, total=ttl, debtor=debtor)
				try:
					db.session.add(new_debt)
					debtor.total_amount += ttl
					db.session.commit()
					flash("Debt added")
					return redirect(f'/list/{debtor.id}')
				except:
					flash("Debt can't add")
					return redirect(f'/list/{debtor.id}')
		except:
			try:
				if request.form['save_debt']:
					id = request.form['debt_id']
					new_item = request.form['new_item']
					new_price = request.form['new_price']
					new_qty = request.form['new_qty']
					
					try:
						debt = Debt.query.filter_by(id=id).first()
						debt.itemName = new_item
						debt.price = new_price
						debt.quantity = new_qty
						new_total = int(new_price) * int(new_qty)
						if debt.total != new_total:
							debt.debtor.total_amount -= debt.total
							debt.debtor.total_amount += new_total
						debt.total = new_total
						
						db.session.commit()
							
						flash("Debt edited")
						return redirect(f'/list/{debtor.id}')
					except:
						flash("Cannot edit this debt")
						return redirect(f'/list/{debtor.id}')
			except:
				if request.form['delete_debt']:
					id = request.form['debt_id']
					debt = Debt.query.filter_by(id=id).first()
					
					try:
						debt.debtor.total_amount -= debt.total
						db.session.delete(debt)
						db.session.commit()
						flash("Debt deleted")
						return redirect(f'/list/{debtor.id}')
					except:
						flash("Cannot delete this debt")
						return redirect(f'/list/{debtor.id}')
	else:
		context = {
			'debtor': debtor,
			'debts': debtor.debts
		}
		return render_template("list.html", ctx=context)
if __name__ == "__main__":
	app.run(debug=True)