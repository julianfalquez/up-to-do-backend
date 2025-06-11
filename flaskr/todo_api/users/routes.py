from .controllers import get_user, get_presigned_url, update_profile_pic
from . import users_bp
from ..auth.controllers import login_required  # Import from auth controllers


@users_bp.route('/me', methods=['GET'])
@login_required  # Protected route
def get_user_route():
    return get_user()


@users_bp.route('/generate-upload-url', methods=['POST'])
@login_required  # Protected route
def get_presigned_url_route():
    return get_presigned_url()


@users_bp.route('/update-profile-pic', methods=['PUT'])
@login_required  # Protected route
def update_profile_pic_route():
    return update_profile_pic()
