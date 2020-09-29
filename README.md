## WEB_API_FLASK app

This is a simple web api written in python 3 utilising:

-Flask

-SQLAlchemy

and

-Postman


## Access
The host is set to 0.0.0.0:5000

app.run(host='0.0.0.0', port=5000)

## Data format
Data structure is based on JSON notation

{

    "name":"Name of the candidate",

    "speciality":"Skills the character is known for",

    "catchphrase":"Instantly recognisable phrases",

    "strengths":"What sets him/her/it apart from the rest"

}


## Usage
It allows the following HTTP commands with corresponding paths

    ## POST
        @app.route('/candidates', methods=['POST'])

        **Arguments**
            -"name":"Name of the candidate",
            -"speciality":"Skills the character is known for",
            -"catchphrase":"Instantly recognisable phrases",
            -"strengths":"What sets him/her/it apart from the rest"

        If the name already exsist no change will occur.

        **Response**
            -"uid":"unique identifier for the entry",
            -"name":"Name of the candidate",
            -"speciality":"Skills the character is known for",
            -"catchphrase":"Instantly recognisable phrases",
            -"strengths":"What sets him/her/it apart from the rest"

    ## PUT
        You can amend the entries by either using the unique ID or name field.
        All fields are required for this operation to work.

        @app.route('/candidates/byID/<int:uid>', methods=['PUT'])
        @app.route('/candidates/byName/<string:Name>', methods=['PUT'])

        **Arguments**
            -"name":"Name of the candidate",
            -"speciality":"Skills the character is known for",
            -"catchphrase":"Instantly recognisable phrases",
            -"strengths":"What sets him/her/it apart from the rest"

        **Response**
            -"uid":"unique identifier for the entry",
            -"name":"Name of the candidate",
            -"speciality":"Skills the character is known for",
            -"catchphrase":"Instantly recognisable phrases",
            -"strengths":"What sets him/her/it apart from the rest"

    ## GET
        We have 3 paths for the GET method. You can either retrieve all entries or
        individual ones based on unique ID or name

        @app.route('/candidates', methods=['GET'])
        @app.route('/candidates/byID/<int:uid>', methods=['GET'])
        @app.route('/candidates/byName/<string:Name>', methods=['GET'])

    ## DELETE
        Similar to the other methods, the unique ID and name fields can be used to delete entries.

        @app.route('/candidates/byID/<int:uid>', methods=['DELETE'])
        @app.route('/candidates/byName/<string:Name>', methods=['DELETE'])


