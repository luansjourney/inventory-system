from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(25), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)


#Routes
@app.route("/")
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route("/stock")
def stock():
    items = Item.query.all()
    return render_template('items.html', items=items)

@app.route('/add_item', methods=['POST'])
def add_item():
    item_name = request.form.get('item_name')
    item_quantity = request.form.get('item_quantity')
    item_category = request.form.get('item_category')
    if item_name:
        new_item = Item(name=item_name, quantity=item_quantity, category=item_category)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/edit_item/<int:id>', methods=['GET','POST'])
def edit_item(id):
    item = Item.query.get(id)
    if request.method == 'POST':
        new_item_name = request.form.get('new_item_name')
        new_item_quantity = request.form.get('new_item_quantity')
        new_item_category = request.form.get('new_item_category')

        if new_item_name:
            item.name = new_item_name
            item.quantity = new_item_quantity
            item.category = new_item_category
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_item.html', item=item)

@app.route('/delete_item/<int:id>')
def delete_item(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/filter_by_category', methods=['POST'])
def filter_by_category():
    selected_category = request.form.get('category')
    if selected_category == "":
        items = Item.query.all()
    else:
        items = Item.query.filter_by(category=selected_category).all()
    return render_template('index.html', items=items)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()        
    app.run(debug=True)