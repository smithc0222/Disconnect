from flask import Flask, Blueprint, render_template, redirect, url_for, request, session, flash, send_from_directory, make_response
import pdfkit
from app.lockout.forms import LockoutForm, LockoutLineForm, AcceptedForm
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
    open_lockouts=db.session.query(Open_Table).filter_by(open_status=True).all()
    implemented_lockouts=db.session.query(Implemented_Table).filter_by(implemented_status=True).all()
    accepted_lockouts=db.session.query(Accepted_Table).filter_by(accepted_status=True).all()
    released_lockouts=db.session.query(Released_Table).filter_by(released_status=True).all()
    cleared_lockouts=db.session.query(Cleared_Table).filter_by(cleared_status=True).all()
    return render_template('index.html', cleared_lockouts=cleared_lockouts,
                            open_lockouts=open_lockouts, accepted_lockouts=accepted_lockouts,
                            implemented_lockouts=implemented_lockouts, released_lockouts=released_lockouts,
                            user=user, today=today)

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

        new_lockout_creator=Open_Table(open_status=1, created_by=user,lockout=new_lockout, date=None)
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
        return render_template('save_lockout.html', this_lockout=this_lockout, lockout_line_form=lockout_line_form, lockout_lines=lockout_lines)

@mod.route('/lockout/<int:this_lockout_id>/implement', methods=['POST', 'GET'])
@login_required
def implement_lockout(this_lockout_id):
    this_lockout=db.session.query(Lockout).filter_by(id=this_lockout_id).first()
    lockout_lines=this_lockout.lockout
    accepted_form=AcceptedForm(request.form)
    if accepted_form.validate_on_submit():
        this_lockout.implemented_by=current_user
        this_lockout.implemented_status=True
        db.session.commit()
        return redirect(url_for('lockout.index'))
    else:
        return render_template('implemented_by.html', this_lockout=this_lockout, lockout_lines=lockout_lines, accepted_form=accepted_form)

@mod.route('/lockout/<int:this_lockout_id>/accept', methods=['POST', 'GET'])
@login_required
def accept_lockout(this_lockout_id):
    this_lockout=db.session.query(Lockout).filter_by(id=this_lockout_id).first()
    lockout_lines=this_lockout.lockout
    accepted_form=AcceptedForm(request.form)
    if accepted_form.validate_on_submit():
        this_lockout.accepted_by=current_user
        this_lockout.accepted_status=True
        db.session.commit()
        return redirect(url_for('lockout.index'))
    else:
        return render_template('accepted_by.html', this_lockout=this_lockout, lockout_lines=lockout_lines, accepted_form=accepted_form)

@mod.route('/lockout/<int:this_lockout_id>/released', methods=['POST','GET'])
@login_required
def released_lockout(this_lockout_id):
    this_lockout=db.session.query(Lockout).filter_by(id=this_lockout_id).first()
    lockout_lines=this_lockout.lockout
    accepted_form=AcceptedForm(request.form)
    if accepted_form.validate_on_submit():
        this_lockout.released_by.current_user
        this_lockout.work_status=True
        this_lockout.released_status=True
        return redirect(url_for('lockout.index'))
    return render_template('released_by.html',this_lockout=this_lockout, lockout_lines=lockout_lines, accepted_form=accepted_form)

@mod.route('/lockout/<int:this_lockout_id>/close', methods=['POST', 'GET'])
@login_required
def close_lockout(this_lockout_id):
    this_lockout=db.session.query(Lockout).filter_by(id=this_lockout_id).first()
    lockout_lines=this_lockout.lockout
    accepted_form=AcceptedForm(request.form)
    if accepted_form.validate_on_submit():
        this_lockout.closed_by=current_user
    #    files = request.files['file']
    #    filename=files.filename
    #    files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #    this_file=db.session.query(Lockout).filter_by(id=this_lockout.id).first()
    #    this_file.filename=files.filename
    #    this_file.data=files.read()
        this_lockout.close_status=True
        db.session.commit()
        return redirect(url_for('lockout.index'))
    else:
        return render_template('upload.html', this_lockout=this_lockout, lockout_lines=lockout_lines, accepted_form=accepted_form)

@mod.route('/upload', methods = ['GET','POST'])
@login_required
def upload():
    return render_template('upload.html')

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@mod.route('/static/lockout/<filename>')
@login_required
def uploaded_file(filename):

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@mod.route('/lockout/<int:this_lockout_id>/pdf')
@login_required
def pdf_template(this_lockout_id):
    path_wkthmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    pdf_config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

    this_lockout=db.session.query(Lockout).filter_by(id=this_lockout_id).first()
    lockout_lines=this_lockout.lockout
    rendered=render_template('pdf.html', this_lockout=this_lockout, lockout_lines=lockout_lines)
    pdf = pdfkit.from_string(rendered, False,  configuration=pdf_config)
    response=make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename={{this_lockout.lockout_number}}.pdf'

    return response
