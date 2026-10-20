import logging

from flask import Blueprint, request, jsonify
from flask_api import status

from db import db

logger = logging.getLogger(__name__)

hospital_bp = Blueprint('hospital', __name__)


@hospital_bp.route('/hospital', methods=['POST'])
def get_hospital():
    """
        To show the hospital details
        :param: None
        :return: Return the json response to the user
    """
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