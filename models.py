from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False) 

def init_db(app):
    with app.app_context():
        db.create_all()
        if not Product.query.first():
            products = [
                ("Bebidas", 12, "Images/bebidas.jpeg", 10),
                ("Duraznos", 20, "Images/duraznos.webp", 15),
                ("Frutas", 35, "Images/frutas.jpeg", 20),
                ("Frutas Secas", 22, "Images/frutos secos.jpeg", 5),
                ("Arándanos", 27, "Images/grapes.jpeg", 30),
                ("Limones", 18, "Images/limonez.webp", 50),
                ("Verduras", 19, "Images/verduras.jpeg", 40),
                ("Medicamentos", 15, "Images/Medicamentos.webp", 25),
                ("Entretenimiento", 38, "Images/mario-luigi-yoschi-figures-163036.jpeg", 10)
            ]
            for product in products:
                db.session.add(Product(name=product[0], price=product[1], image=product[2], quantity=product[3]))
            db.session.commit()
            print("Database created and populated with products.")

def get_all_products():
    return Product.query.all()


def get_products_by_ids(ids):
    return Product.query.filter(Product.id.in_(ids)).all()
