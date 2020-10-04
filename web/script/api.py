from flask import Blueprint, request, jsonify 

api = Blueprint('api', __name__, url_prefix='/api')

# 取得するチケットの情報を修正する(memo欄のみが修正できる)
@api.route('/ticket/result/update', methods=['POST'])
def ticket_result_update():
    print(request.data)
    return jsonify(success=True)
