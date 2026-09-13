from sample_flask_auth.domain import Role, User


def test_admin_can_delete_other_users():
    admin = User(id=1, username="admin", password_hash="x", role=Role.ADMIN)
    assert admin.can_delete(2)
    assert not admin.can_delete(1)


def test_user_cannot_delete_or_update_others():
    user = User(id=2, username="user", password_hash="x", role=Role.USER)
    assert not user.can_delete(1)
    assert not user.can_delete(2)
    assert user.can_update_password(2)
    assert not user.can_update_password(3)
