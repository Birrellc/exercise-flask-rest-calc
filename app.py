from flask import Flask, make_response, request, jsonify
from decimal import Decimal
import math
import statistics


app = Flask(__name__)


# helper function to change decimal to full value numbers eg: 3.0 to 3


def decimal_or_integer(x):
    value = math.ceil(x) - math.floor(x)
    if value == 0:
        return math.floor(x)
    return x

# error handler function


def error_handler(message, error_code):
    return jsonify({
        "Error": {
            "Message": message,
            "Success": False,
        }
    }), error_code

# returns the sum of path parameters x and y


@app.route('/calc/<request_type>/add/<x>/to/<y>', methods=['GET'])
def add(x, y, request_type):
    ans = decimal_or_integer(Decimal(x) + Decimal(y))
    equation = f'{str(x)} + {str(y)} = {str(ans)}'

    if request.method == 'GET' and request_type == 'web':
        return make_response(equation, 200)

    if request.method == 'GET' and request_type == 'api':
        response = jsonify({
            "Calculation": {
                "Message": "Successful result",
                "Success": True,
                "Text": equation,
                "Result": ans
            }})
        return make_response(response, 200)

# returns the difference of path parameters x and y


@app.route('/calc/<request_type>/subtract/<x>/from/<y>', methods=['GET', 'POST'])
def subtract(x, y, request_type):
    ans = decimal_or_integer(Decimal(y) - Decimal(x))
    equation = f'{(y)} - {(x)} = {(ans)}'

    if request.method == 'GET' and request_type == 'web':
        return make_response(equation, 200)

    if request.method == 'GET' and request_type == 'api':
        response = jsonify({
            "Calculation": {
                "Message": "Successful result",
                "Success": True,
                "Text": equation,
                "Result": ans
            }})
        return make_response(response, 200)


# returns the product of path parameters x and y


@app.route('/calc/<request_type>/multiply/<x>/by/<y>', methods=['GET', 'POST'])
def multiply(x, y, request_type):
    ans = decimal_or_integer(Decimal(x) * Decimal(y))
    equation = f'{str(x)} * {str(y)} = {str(ans)}'

    if request.method == 'GET' and request_type == 'web':
        return make_response(equation, 200)

    if request.method == 'GET' and request_type == 'api':
        response = jsonify({
            "Calculation": {
                "Message": "Successful result",
                "Success": True,
                "Text": equation,
                "Result": ans
            }})
        return make_response(response, 200)


@app.route('/calc/<request_type>/divide/<x>/by/<y>', methods=['GET', 'POST'])
def divide(x, y, request_type):
    try:
        ans = decimal_or_integer(Decimal(x) / Decimal(y))
        equation = f'{str(x)} / {str(y)} = {str(ans)}'

        if request.method == 'GET' and request_type == 'web':
            return make_response(equation, 200)

        if request.method == 'GET' and request_type == 'api':
            response = jsonify({
                "Calculation": {
                    "Message": "Successful result",
                    "Success": True,
                    "Text": equation,
                    "Result": ans
                }})
        return make_response(response, 200)

    except ZeroDivisionError:
        # return Cannot divide by zero error
        return make_response("Cannot divide by zero", 400)


@app.route('/calc/<request_type>/sum', methods=['GET'])
def calculate_sum(request_type):
    content_type = request.headers.get('Content-Type')
    if not content_type == 'application/json':

        ans = decimal_or_integer(
            sum(map(Decimal, request.args.getlist('numbers'))))
        equation = ' + ' .join(request.args.getlist('numbers')
                               ) + ' = ' + str(ans)

        if request.method == 'GET' and request_type == 'web':
            response = equation
            return make_response(response, 200)

        if request.method == 'GET' and request_type == 'api':
            response = jsonify({
                "Calculation": {
                    "Message": "Successful result",
                    "Success": True,
                    "Text": equation,
                    "Result": ans
                }})
            return make_response(response, 200)

    elif content_type == 'application/json':
        if not request.is_json:
            return error_handler('Missing JSON in request', 400)

        if 'Numbers' not in request.json:
            return error_handler('Missing Numbers in request', 400)

        numbers = request.json['Numbers']
        if len(numbers) == 0:
            return error_handler('Empty List', 400)

        print(numbers)
        convstr = [str(i) for i in numbers]
        ans = decimal_or_integer(sum(map(Decimal, numbers)))
        equation = ' + '.join(convstr) + ' = '

        return make_response(jsonify({
            "Calculation": {
                "Message": "Successful result",
                "Success": True,
                "Text": equation,
                "Result": ans
            }}), 200)
    else:
        return jsonify({
            "Calculation": {
                "Message": "Invalid method",
                "Success": False,
            }
        }), 400


@app.route('/calc/<request_type>/product', methods=['GET', 'POST'])
def calculate_product(request_type):
    ans = decimal_or_integer(
        math.prod(map(Decimal, request.args.getlist('numbers'))))
    equation = ' x ' .join(request.args.getlist(
        'numbers')) + ' = '

    if request.method == 'GET' and request_type == 'web':
        response = equation
        return make_response(response, 200)

    if request.method == 'GET' and request_type == 'api':
        response = jsonify({
            "Calculation": {
                "Message": "Successful result",
                "Success": True,
                "Text": equation,
                "Result": ans
            }})
        return make_response(response, 200)

    elif request.method == 'POST' and request_type == 'api':
        if not request.is_json:
            return jsonify({
                "Calculation": {
                    "Message": "Missing JSON in request",
                    "Success": False,
                }
            }), 400

        if 'Numbers' not in request.json:
            return jsonify({
                "Calculation": {
                    "Message": "Missing numbers in request",
                    "Success": False,
                }
            }), 400

        numbers = request.json['Numbers']
        if len(numbers) == 0:
            return jsonify({
                "Calculation": {
                    "Message": "Empty List",
                    "Success": False,
                }
            }), 400

        print(numbers)
        ans = decimal_or_integer(math.prod(map(Decimal, numbers)))
        convstr = [str(i) for i in numbers]
        equation = ' x '.join(convstr) + ' = '

        response = {
            "Calculation": {
                "Message": "Successful result",
                "Success": True,
                "Text": equation,
                "Result": ans
            }
        }
        return make_response(jsonify(response), 200)

    else:
        return jsonify({
            "Calculation": {
                "Message": "Invalid method",
                "Success": False,
            }
        }), 400


@app.route('/calc/<request_type>/mean', methods=['GET', 'POST'])
def calculate_average(request_type):
    ans = decimal_or_integer(
        statistics.mean(map(Decimal, request.args.getlist('numbers'))))

    equation = '(' + ' + ' .join(request.args.getlist(
        'numbers')) + ') / ' + str(len(request.args.getlist('numbers'))) + ' = '

    if request.method == 'GET' and request_type == 'web':
        response = equation
        return make_response(response, 200)

    if request.method == 'GET' and request_type == 'api':
        response = jsonify({
            "Calculation": {
                "Message": "Successful result",
                "Success": True,
                "Text": equation,
                "Result": ans
            }})
        return make_response(response, 200)

    elif request.method == 'POST' and request_type == 'api':
        if not request.is_json:
            return jsonify({
                "Calculation": {
                    "Message": "Missing JSON in request",
                    "Success": False,
                }
            }), 400

        if 'Numbers' not in request.json:
            return jsonify({
                "Calculation": {
                    "Message": "Missing numbers in request",
                    "Success": False,
                }
            }), 400

        numbers = request.json['Numbers']
        if len(numbers) == 0:
            return jsonify({
                "Calculation": {
                    "Message": "Empty List",
                    "Success": False,
                }
            }), 400

        ans = decimal_or_integer(
            statistics.mean(map(Decimal, numbers)))
        convstr = [str(i) for i in numbers]
        equation = '(' + ' + '.join(convstr) + ') / ' + \
            str(len(convstr)) + ' = '

        response = {
            "Calculation": {
                "Message": "Successful result",
                "Success": True,
                "Text": equation,
                "Result": ans
            }
        }
        return make_response(jsonify(response), 200)

    else:
        return jsonify({
            "Calculation": {
                "Message": "Invalid method",
                "Success": False,
            }
        }), 400
