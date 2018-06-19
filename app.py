from flask import Flask, render_template, request, redirect, url_for
from flask_modus import Modus
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

DB = "postgresql://localhost/mushrooms"

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
Modus(app)
toolbar = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Mushroom(db.Model):
    __tablename__ = "mushrooms"

    id = db.Column(db.Integer, primary_key=True)
    comm_name = db.Column(db.Text, unique=True)
    lat_name = db.Column(db.Text)
    sym_associations = db.Column(db.Text)

    # create tables as needed
    db.create_all()

    def __init__(self, comm_name, lat_name, sym_associations):
        self.comm_name = comm_name
        self.lat_name = lat_name
        self.sym_associations = sym_associations

    def __repr__(self):
        return self.comm_name


g_chant = Mushroom('Golden chanterelle', 'Cantharellus californicus',
                   'live oak')
b_trumpet = Mushroom('Black Trumpet', 'Craterellus cornucopioides',
                     'oak and beech')
h_hog = Mushroom('Hedgehog', 'Hydnum repandum', 'tanoak and huckleberry')

db.session.commit()


@app.route('/mushrooms', methods=['GET'])
def index():
    mush_list = Mushroom.query.all()
    return render_template('index.html', mush_list=mush_list)


@app.route('/mushrooms/new', methods=['GET'])
def new():
    return render_template('new.html')


@app.route('/mushrooms', methods=['POST'])
def create():
    comm_name = request.form['comm_name'],
    lat_name = request.form['lat_name'],
    sym_assoc = request.form['sym_assoc']

    new_mush = Mushroom(
        comm_name=comm_name, lat_name=lat_name, sym_associations=sym_assoc)
    # new_snack.save()
    db.session.add(new_mush)  # makes INSERT happen
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/mushrooms/<int:id>', methods=['GET'])
def show(id):
    mushroom = Mushroom.query.filter(Mushroom.id == id).one()
    return render_template('show.html', mushroom=mushroom)


@app.route('/mushrooms/<int:id>', methods=['DELETE'])
def destroy(id):
    found_mush = Mushroom.query.filter(Mushroom.id == id).one()
    db.session.delete(found_mush)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/mushrooms/<int:id>/edit', methods=['GET'])
def edit(id):
    # mushroom = Mushroom.query.filter(Mushroom.id == id).one()
    mushroom = Mushroom.query.get(id)
    return render_template('edit.html', mushroom=mushroom)


@app.route('/mushrooms/<int:id>', methods=['PATCH'])
def update(id):
    mushroom = Mushroom.query.filter(Mushroom.id == id).one()
    mushroom.comm_name = request.form['comm_name']
    mushroom.lat_name = request.form['lat_name']
    mushroom.sym_associations = request.form['sym_assoc']

    db.session.commit()
    return redirect(url_for('show', id=mushroom.id))