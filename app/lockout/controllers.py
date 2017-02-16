from flask import Flask, Blueprint, render_template, redirect, url_for, request, session, flash, send_from_directory, make_response
import pdfkit
from app.lockout.forms import LockoutForm, LockoutLineForm, ChainOfCustodyForm
from app.lockout.models import Lockout, Lockout_Line, Open_Table, Implemented_Table, Accepted_Table, Released_Table, Cleared_Table
from app.auth.models import User
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

#Blueprint Module Creation
mod = Blueprint('lockout', __name__, template_folder='templates')

#login manager flask-login
from app import app
from app import db

from app.auth.controllers import load_user

@mod.route('/')
@login_required
def index():
    today=datetime.today()
    user=db.session.query(User).filter_by(username=current_user.username).first()
    open_lockouts=db.session.query(Open_Table).all()
    implemented_lockouts=db.session.query(Implemented_Table).all()
    accepted_lockouts=db.session.query(Accepted_Table).all()
    released_lockouts=db.session.query(Released_Table).all()
    cleared_lockouts=db.session.query(Cleared_Table).all()
    lockouts=db.session.query(Lockout).all()
    return render_template('index.html', open_lockouts=open_lockouts, accepted_lockouts=accepted_lockouts,
                            implemented_lockouts=implemented_lockouts, released_lockouts=released_lockouts,
                            cleared_lockouts=cleared_lockouts, user=user, lockouts=lockouts, today=today)

@mod.route('/create_lockout', methods=['POST', 'GET'])
@login_required
def create_lockout():
    user=db.session.query(User).filter_by(username=current_user.username).first()
    lockout_form=LockoutForm(request.form)
    lockout_line_form=LockoutLineForm(request.form)
    today=datetime.today()
    lockout=db.session.query(Lockout).all()
    last_lockout=lockout[-1].id
    next_lockout=last_lockout+1

    if request.method == 'POST':
        new_lockout=Lockout(lockout_number=lockout_form.lockout_number.data,
                            lockout_description=lockout_form.lockout_description.data,
                            lockout_status=1,
                            goggles=lockout_form.goggles.data,
                            faceshield=lockout_form.faceshield.data,
                            fullface=lockout_form.fullface.data,
                            dustmask=lockout_form.dustmask.data,
                            leathergloves=lockout_form.leathergloves.data,
                            saranax=lockout_form.saranax.data,
                            nitrilegloves=lockout_form.nitrilegloves.data,
                            chemicalgloves=lockout_form.chemicalgloves.data,
                            chemicalsuit=lockout_form.chemicalsuit.data,
                            tyrex=lockout_form.tyrex.data,
                            rubberboots=lockout_form.rubberboots.data,
                            sar=lockout_form.sar.data,
                            ppe=lockout_form.ppe.data)
        db.session.add(new_lockout)

        new_lockout_creator=Open_Table(open_status=1,created_by=user, lockout=new_lockout, date=None)
        db.session.add(new_lockout_creator)

        new_lockout_line=Lockout_Line(valve_number=lockout_line_form.valve_number.data,
                        line_description=lockout_line_form.line_description.data,
                        lock_position=lockout_line_form.lock_position.data,
                        removal_position=lockout_line_form.removal_position.data,
                        lockout=new_lockout)
        db.session.add(new_lockout_line)

        db.session.commit()
        return redirect(url_for('lockout.save_lockout'))

    else:
        return render_template('create_lockout.html', lockout=lockout, user=user, today=today, next_lockout=next_lockout, lockout_form=lockout_form, lockout_line_form=lockout_line_form)

@mod.route('/save_lockout', methods=['POST', 'GET'])
@login_required
def save_lockout():
    all_lockout=db.session.query(Lockout).all()
    this_lockout=all_lockout[-1]
    lockout_line_form=LockoutLineForm(request.form)
    lockout_lines=this_lockout.lockout
    open_table=db.session.query(Open_Table).filter_by(lockout=this_lockout).first()
    if request.method == 'POST':
        new_lockout_line=Lockout_Line(valve_number=lockout_line_form.valve_number.data,
                        line_description=lockout_line_form.line_description.data,
                        lock_position=lockout_line_form.lock_position.data,
                        removal_position=lockout_line_form.removal_position.data,
                        lockout=this_lockout)
        db.session.add(new_lockout_line)
        db.session.commit()
        return redirect(url_for('lockout.save_lockout'))
    else:
        return render_template('save_lockout.html', this_lockout=this_lockout, lockout_line_form=lockout_line_form, lockout_lines=lockout_lines, open_table=open_table)

@mod.route('/lockout/<int:this_lockout_id>', methods=['POST', 'GET'])
@login_required
def lockout(this_lockout_id):
    this_lockout=db.session.query(Lockout).filter_by(id=this_lockout_id).first()
    lockout_lines=this_lockout.lockout
    chain_of_custody_form=ChainOfCustodyForm(request.form)
    if request.method == 'POST':
        if chain_of_custody_form.implemented_by.data == None:
            print('None')
        else:
            implement_new=db.session.query(User).filter_by(username=chain_of_custody_form.implemented_by.data).first()
            db.session.add(Implemented_Table(1, implement_new, this_lockout, None))
            this_lockout.lockout_status=2

        if chain_of_custody_form.accepted_by.data == None:
            print('None')
        else:
            accepted_new=db.session.query(User).filter_by(username=chain_of_custody_form.accepted_by.data).first()
            db.session.add(Accepted_Table(1, accepted_new, this_lockout, None))
            this_lockout.lockout_status=3

        if chain_of_custody_form.released_by.data == None:
            print('None')
        else:
            released_new=db.session.query(User).filter_by(username=chain_of_custody_form.released_by.data).first()
            db.session.add(Released_Table(1, released_new, this_lockout, None))
            this_lockout.lockout_status=4

        if chain_of_custody_form.cleared_by.data == None:
            print('None')
        else:
            cleared_new=db.session.query(User).filter_by(username=chain_of_custody_form.cleared_by.data).first()
            db.session.add(Cleared_Table(1, cleared_new, this_lockout, None))
            this_lockout.lockout_status=5

        db.session.commit()

        return redirect(url_for('lockout.index'))
    else:
        return render_template('lockout.html', this_lockout=this_lockout, lockout_lines=lockout_lines, chain_of_custody_form=chain_of_custody_form)

@mod.route('/lockout/<int:this_lockout_id>/pdf')
@login_required
def pdf_template(this_lockout_id):
    path_wkthmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    pdf_config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    today=datetime.today()
    this_lockout=db.session.query(Lockout).filter_by(id=this_lockout_id).first()
    lockout_lines=this_lockout.lockout
    rendered=render_template('pdf.html', this_lockout=this_lockout, lockout_lines=lockout_lines, today=today)
    pdf = pdfkit.from_string(rendered, False,  configuration=pdf_config)
    response=make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename={{this_lockout.lockout_number}}.pdf'

    return response
