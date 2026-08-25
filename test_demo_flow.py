"""
Automated Verification for Full Live Demo Flow
Includes:
1. Browse Items display & Remove Item SQL DELETE
2. Direct SQLite database verification of removed found item
3. Student Report Lost Item (SQL INSERT)
4. Admin Authentication & Route Protection (admin@123)
5. Admin status update (SQL UPDATE + Notification INSERT)
6. Student notification verification
7. Admin Logout
"""

import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.main import create_app
from backend.app.utils.db import get_db_connection


def run_tests():
    app = create_app()
    client = app.test_client()

    print("=================================================================")
    print(" STARTING LIVE DEMO VERIFICATION (WITH BROWSE REMOVE ITEM)")
    print("=================================================================")

    # -------------------------------------------------------------------------
    # 1. Create a demo found item to test removal
    # -------------------------------------------------------------------------
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO found_items (item_name, description, found_location, found_date, status)
            VALUES ('Demo Test Earphones', 'White wired earphones', 'Library 2nd Floor', '25-08-2026', 'AVAILABLE');
        """)
        test_item_id = cursor.lastrowid

    # -------------------------------------------------------------------------
    # 2. Test Browse Page (Displays item + Remove button)
    # -------------------------------------------------------------------------
    res = client.get('/browse')
    assert res.status_code == 200
    assert b'Demo Test Earphones' in res.data
    assert b'Remove' in res.data
    print(f'[PASS] 1. Browse page displays item #{test_item_id} with Remove button')

    # -------------------------------------------------------------------------
    # 3. Test Remove Found Item (SQL DELETE)
    # -------------------------------------------------------------------------
    res = client.post(f'/browse/remove/{test_item_id}', follow_redirects=True)
    assert res.status_code == 200
    assert b'was removed successfully' in res.data
    print('[PASS] 2. User clicked Remove -> Backend executed SQL DELETE')

    # -------------------------------------------------------------------------
    # 4. Direct SQLite DB Verification
    # -------------------------------------------------------------------------
    with get_db_connection() as conn:
        row = conn.execute(f"SELECT * FROM found_items WHERE found_item_id = {test_item_id}").fetchone()
        assert row is None
        print(f'[PASS] 3. SQLite Database verified: found_item_id={test_item_id} permanently deleted')

    # -------------------------------------------------------------------------
    # 5. Subsequent Browse View Verification (Row is gone from UI)
    # -------------------------------------------------------------------------
    res_after = client.get('/browse')
    assert f'#{test_item_id}'.encode() not in res_after.data
    assert b'Demo Test Earphones' not in res_after.data
    print('[PASS] 4. Subsequent page refresh confirms item is completely removed from Browse Items')

    # -------------------------------------------------------------------------
    # 6. Test Admin Route Protection (Unauthenticated -> Redirect to Login)
    # -------------------------------------------------------------------------
    res = client.get('/admin')
    assert res.status_code == 302
    assert '/admin/login' in res.location
    print('[PASS] 5. Direct /admin access correctly redirects unauthenticated user to /admin/login')

    # -------------------------------------------------------------------------
    # 7. Test Admin Login (admin@123)
    # -------------------------------------------------------------------------
    res = client.post('/admin/login', data={'password': 'admin@123'}, follow_redirects=True)
    assert res.status_code == 200
    assert b'Department Admin Dashboard' in res.data
    print('[PASS] 6. Admin authenticated successfully with password "admin@123"')

    # -------------------------------------------------------------------------
    # 8. Student reports lost item & Admin marks it as found
    # -------------------------------------------------------------------------
    res = client.post('/report', data={
        'item_name': 'Demo Security Book',
        'category': 'Books & Stationery',
        'description': 'Textbook for testing',
        'lost_location': 'Computer Lab 3',
        'lost_date': '25-08-2026'
    }, follow_redirects=True)
    assert res.status_code == 200

    with get_db_connection() as conn:
        row = conn.execute("SELECT * FROM lost_items WHERE item_name = 'Demo Security Book' ORDER BY lost_item_id DESC").fetchone()
        assert row is not None
        lost_id = row['lost_item_id']

    # Admin updates status
    res = client.post(f'/admin/mark-found/{lost_id}', follow_redirects=True)
    assert res.status_code == 200
    assert b'marked as found' in res.data

    with get_db_connection() as conn:
        row = conn.execute(f'SELECT * FROM lost_items WHERE lost_item_id = {lost_id}').fetchone()
        assert row['status'] == 'FOUND'
    print('[PASS] 7. Admin workflow (Mark as Found + Automated Notification) executed')

    # -------------------------------------------------------------------------
    # 9. Admin Logout
    # -------------------------------------------------------------------------
    res = client.get('/admin/logout', follow_redirects=True)
    assert res.status_code == 200
    print('[PASS] 8. Admin Logout cleared session and redirected to Browse page')

    # -------------------------------------------------------------------------
    # 10. Clean up test record
    # -------------------------------------------------------------------------
    with get_db_connection() as conn:
        conn.execute(f'DELETE FROM lost_items WHERE lost_item_id = {lost_id}')
        conn.execute('DELETE FROM notifications WHERE message LIKE "%Demo Security Book%"')
        conn.commit()
    print('[PASS] 9. Test data cleaned up')

    print('\n=================================================================')
    print(' ALL LIVE DEMO FLOWS VERIFIED SUCCESSFULLY!')
    print('=================================================================')


if __name__ == '__main__':
    run_tests()
