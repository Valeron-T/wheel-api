from flask import Blueprint, request, jsonify
from app import mongo
from app.task import process_pdf

bp = Blueprint('risk', __name__)


def calc_var_score(scores, answers_dict):
    risk_score = sum(scores[key][value] for key, value in answers_dict.items() if key != "age")
    risk_score = (risk_score * 350 / 1200) + 500
    risk_score = round(risk_score // 50) * 50
    return risk_score, [scores[key][value] for key, value in answers_dict.items()]


@bp.route('/calculate', methods=['POST'])
def calculate_risk_score():
    data = request.get_json()

    # answer weight
    question_scores = {
        # Age - Higher the age lower the risk
        "age": {'18-25': 1, '26-30': 2, '31-35': 3, '36-40': 4, '41-45': 4, '46-50': 5, '51+': 5},
        # Job - Government --> Self employed
        "employment": {'Self Employed': 50, 'Business': 60, 'Private': 80, 'Govt.': 100},
        # Dependents --> 0 - 4+
        "dependents": {'0': 100, '1': 80, '2': 70, '3': 60, '4+': 40},
        # Which train to choose in peak hours ? --> Fast, Either, Slow
        "Which train to choose in peak hours ?": {"Fast": 100, "Either": 75, "Slow": 50},
        # What speed would you drive at? --> 40,60,80,100
        "What speed would you drive at?": {'40-60': 60, '60-80': 75, '80-100': 90, '100+': 100},
        # What are your investment goals ?
        "investment goals": {'Child Education': 50, 'Retirement': 80, 'Payback debt': 0, 'Wealth Creation': 100},
        # What amounts to invest monthly ?
        "investment_amt_monthly": {'5000 - 25000': 10, '25001 - 50000': 30, '50001 - 100000': 50, '100001 - 150000': 70,
                                   '150000+': 100},
        # In which of the following instruments would you like to invest?
        "instruments_preferred": {'Share Market': 100, 'Mutual Funds': 90, 'Bonds': 60, 'Fixed Deposits': 50,
                                  'None': 0},
        # Please describe your attitude towards risk and return.
        "Please describe your attitude towards risk and return.": {
            'I am low risk taker, I need safety and security.': 25,
            'I am a average risk taker, can invest in risky instruments to earn good return': 60,
            'I am a high risk taker, will be happy to invest in risky instruments to earn high returns': 100},
        "Corrections into the markets are normal. What percentage of fall into your portfolio would make you "
        "uncomfortable?": {
            "5%": 25, "10%": 50, "15%": 75, "20%": 100
        },
        "How many years will you allow your investments to grow before you will need to start significant withdrawals?": {
            "Less than 1 year": 10, "1-3": 30, "3-5": 50, "5-7": 70, "7-10": 100
        },
        "If there is a loss in your portfolio due to some external reasons, how long will you wait for the "
        "liquidation of your portfolio?": {
            "Less than 3 months": 0, "Upto 6 months": 25, "Upto 12 months": 50, "Upto 2 years": 100
        },
        "Which of the following portfolio would you prefer?": {
            "100 % Equity": 100,
            "80 % Equity - 20 % Debt": 80,
            "75 % Equity - 25 % Debt": 75,
            "60 % Equity - 40 % Debt": 60,
            "50 % Equity - 50 % Debt": 50,
            "40 % Equity - 60 % Debt": 40,
            "25 % Equity - 75 % Debt": 25,
        }
    }

    score, ind_scores = calc_var_score(question_scores, data)

    return jsonify({"message": f'Risk score is {score}'})
