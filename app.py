import logging

import pymongo
from flask import request, jsonify
from flask_api import FlaskAPI, status

from config import Config

app = FlaskAPI(__name__)
logger = logging.getLogger(__name__)

client = pymongo.MongoClient(
    Config.MONGO_HOST,
    Config.MONGO_PORT,
    username=Config.MONGO_USER,
    password=Config.MONGO_PASS,
    authSource=Config.MONGO_AUTH_DB,
)
db = client[Config.DB_NAME]


@app.route('/api/hospital', methods=['POST'])
def get_hospital():
    try:
        body = request.data
        url = body.get('url', '') if isinstance(body, dict) else ''
        if not url or not isinstance(url, str):
            return jsonify({'msg': 'Please provide url', 'msg_type': 2}), status.HTTP_400_BAD_REQUEST

        hospital = list(db['hospital_with_seo_url'].aggregate([
            {'$match': {'seo_url': url}},
            {'$addFields': {'HospitalID': '$_id'}},
            {'$limit': 1}]))

        if not hospital:
            return jsonify({'msg': 'Hospital not exist', 'msg_type': 2}), status.HTTP_400_BAD_REQUEST

        return jsonify({'data': hospital[0], 'msg_type': 1}), status.HTTP_200_OK

    except Exception:
        logger.exception('get_hospital failed')
        return jsonify({'msg': 'Internal Server Error, try again', 'msg_type': 2}), status.HTTP_500_INTERNAL_SERVER_ERROR
    



if __name__ == '__main__':
    app.run(debug=True, threaded=True)