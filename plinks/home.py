from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from plinks.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
	if request.method == 'POST':
        	link_alias = request.form['link_alias']
        	full_link = request.form['full_link']
        	db = get_db()
        	error = None

        	if not full_link:
            		error = 'Full link is required.'
        	elif not link_alias:
            		error = 'Alias is required.'
        	elif db.execute('SELECT full_link FROM links WHERE link_alias = ?', (link_alias,)).fetchone() is not None:
            		return ("Alias %s is already added." % link_alias)

        	if error is None:
            		db.execute('INSERT INTO links (link_alias, full_link) VALUES (?, ?)',(link_alias, full_link))
            		db.commit()
            		return "Alias added"

        	flash(error)

	return render_template('base.html')

@bp.route('/<string:alias>', methods=('GET',))
def alias_redirection(alias):
	if request.method == 'GET':
		if alias is not None:
			db = get_db()
			link_row = db.execute('SELECT full_link FROM links WHERE link_alias = ?', (alias,)).fetchone()
			if link_row is not None:
				link = link_row['full_link']
				return redirect(link)

	return redirect(url_for('home.index'))
