from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from listr.auth import login_required
from listr.db import get_db

bp = Blueprint('list', __name__)


@bp.route('/')
def index():
    if g.user is None:
         return redirect(url_for('auth.login'))
    current_list = session.get('current_list')
    if current_list is None:
        current_list = session['root']
        flash('''There was an issue getting your current list
        please navigate to the list from your root''')
    return redirect(url_for('list.get_list', list_id=current_list))


@bp.route('/<list_id>', methods=('GET', 'POST'))
def get_list(list_id):
    db = get_db()
    cursor = db.cursor()
    user_id = session.get('user_id')
    query = '''
        SELECT id, parent, user, task, completed
        FROM listr
        WHERE id=?
        '''
    parent = cursor.execute(query,(list_id,)).fetchone()
    if parent is None:
        abort(404, "List id {list_id} does not exist.")
    elif parent['user'] != user_id:
        abort(403, "this Listr doesn't belong to you. Naughty!")
    if request.method == 'POST':
        task = request.form['task']
        error = None if not task else "You can't submit an empty task"
        if error is not None:
            flash(error)
        else:
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO listr (parent, user, task) VALUES (?, ?, ?)',
                (list_id,user_id, task)
            )
            db.commit()
    session['current_list'] = list_id
    query = '''
        SELECT id, task, completed
        FROM listr
        WHERE parent = ?;'''
    listrs = cursor.execute(query, (parent['id'],)).fetchall()
    cursor.close()
    return render_template('list/list.html', parent=parent, listrs=listrs)

@bp.route('/complete/<list_id>', methods=['GET'])
def toggle_completed(list_id:int):
    db = get_db()
    cursor = db.cursor()
    user_id = session.get('user_id')
    
    query = '''
    UPDATE listr
    SET completed
    = NOT completed
    WHERE id = ?
    AND user = ?
    '''
    cursor.execute(query,(list_id, user_id))
    db.commit()
    return redirect(url_for('list.get_list',list_id=session['current_list']))




