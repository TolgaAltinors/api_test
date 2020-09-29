from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import markdown

#import logging as logger
#logger.basicConfig(level="DEBUG")


# Init app
app = Flask(__name__)

# Create base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Create Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init dp
db = SQLAlchemy(app)

#Init Marshmallow
ma = Marshmallow(app)

# CV class/model
class Candidate(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    speciality = db.Column(db.String)
    strengths = db.Column(db.String)
    catchphrase= db.Column(db.String)

    def __init__(self, name, speciality, strengths, catchphrase):
        self.name = name
        self.speciality = speciality
        self.strengths = strengths
        self.catchphrase = catchphrase
    
    def __repr__(self):
        return f"Candidate(name={self.name}, speciality={self.speciality}, strengths={self.strengths}, catchphrase={self.catchphrase})"

        
#Candidate schema
class CandidateSchema(ma.Schema):
    class Meta:
        fields = ('uid', 'name', 'speciality', 'strengths', 'catchphrase')

# init schema
candidate_schema = CandidateSchema()
candidates_schema = CandidateSchema(many=True)

# # # # # # # # # # # # # # # # # # # # # #
# # Load documentation on root
# # # # # # # # # # # # # # # # # # # # # #
@app.route('/')
def index():
    # Usage guide

    # open the read me file
    readmeFile = os.path.join(basedir, 'README.md')

    with open(readmeFile, 'r') as markdown_file:

        # read the content
        content = markdown_file.read()

        # make it a html
        return markdown.markdown(content)
    
# # # # # # # # # # # # # # # # # # # # # #
# # add new candidate
# # # # # # # # # # # # # # # # # # # # # #
@app.route('/candidates', methods=['POST'])
def post():

    # # Check if name is already in database
    candidates= Candidate.query.filter_by(name=request.json['name']).first()
    if candidates:
        abort(409, "Candidate already exist...Delete or amend existing entry")

    name = request.json['name']
    speciality = request.json['speciality']
    strengths = request.json['strengths']
    catchphrase = request.json['catchphrase']

    candidate = Candidate(name, speciality, strengths, catchphrase)

    db.session.add(candidate)
    db.session.commit()

    return candidate_schema.jsonify(candidate)


# # # # # # # # # # # # # # # # # # # # # #
# Update candidate by ID
# # # # # # # # # # # # # # # # # # # # # #
@app.route('/candidates/byID/<int:uid>', methods=['PUT'])
def update_byID(uid):

    candidate = Candidate.query.get(uid)

    candidate.name = request.json['name']
    candidate.speciality = request.json['speciality']
    candidate.strengths = request.json['strengths']
    candidate.catchphrase = request.json['catchphrase']

    db.session.commit()

    return candidate_schema.jsonify(candidate)


# # # # # # # # # # # # # # # # # # # # # #
# Update candidate by Name
# # # # # # # # # # # # # # # # # # # # # #
@app.route('/candidates/byName/<string:Name>', methods=['PUT'])
def update_byName(Name):

    candidate = Candidate.query.filter_by(name=Name).first()
 
    print (candidate)

    candidate.name = request.json['name']
    candidate.speciality = request.json['speciality']
    candidate.strengths = request.json['strengths']
    candidate.catchphrase = request.json['catchphrase']

    db.session.commit()

    return candidate_schema.jsonify(candidate)


# # # # # # # # # # # # # # # # # # # # # #
# get all candidates entries
# # # # # # # # # # # # # # # # # # # # # #
@app.route('/candidates', methods=['GET'])
def get_all():
    candidates = Candidate.query.all()
    result = candidates_schema.dump(candidates)
    return jsonify(result)


# # # # # # # # # # # # # # # # # # # # # #
# get candidate by id
# # # # # # # # # # # # # # # # # # # # # #
@app.route('/candidates/byID/<int:uid>', methods=['GET'])
def get_byID(uid):
    candidate= Candidate.query.get(uid)
    if not candidate:
        abort(404, "Can not find candidate...")

    return candidate_schema.jsonify(candidate)


# # # # # # # # # # # # # # # # # # # # # #
# get candidate by name
# # # # # # # # # # # # # # # # # # # # # #
@app.route('/candidates/byName/<string:Name>', methods=['GET'])
def get_byName(Name):

    # # Check if name is in database
    candidate= Candidate.query.filter_by(name=Name).first()
    if not candidate:
        abort(404, "Can not find candidate...")
    
    return candidate_schema.jsonify(candidate)


# # # # # # # # # # # # # # # # # # # # # #
# delete candidate by ID
# # # # # # # # # # # # # # # # # # # # # #
@app.route('/candidates/byID/<int:uid>', methods=['DELETE'])
def delete(uid):

    candidate = Candidate.query.get(uid)
    if not candidate:
        abort(404, "Candidate does not exist...")

    db.session.delete(candidate)
    db.session.commit()
    return candidate_schema.jsonify(candidate)


# # # # # # # # # # # # # # # # # # # # # #
# delete candidate by Name
# # # # # # # # # # # # # # # # # # # # # #
@app.route('/candidates/byName/<string:name>', methods=['DELETE'])
def delete_byName(name):
    # # Check if name is in database
    candidate= Candidate.query.filter_by(name=request.json['name']).first()
    if not candidate:
        abort(404, "Candidate does not exist...")

    db.session.delete(candidate)
    db.session.commit()
    return candidate_schema.jsonify(candidate)


# Run Server
if __name__ == '__main__':
    #logger.debug("Starting the flask application...")
    app.run(host='0.0.0.0', port=5000)
