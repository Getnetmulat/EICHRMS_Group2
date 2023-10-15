from models.modules import *
## Blueprint Configuration
collage_bp = Blueprint(
    'collage_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# route to view the collage office page
@collage_bp.route('/collage/', methods=['GET', 'POST'])
@login_required
def collage():
    # Query all list of branchs
    all_collage = db.session.query(Collage).order_by(Collage.collageName.desc())
    all_branch = db.session.query(Collage, Branch).select_from(Collage).join(Branch).all()

    if request.method == 'GET':
        return render_template('collage.html', collages = all_collage, branchs = all_branch)

    return render_template('collage.html', collages = all_collage, branchs = all_branch)

# route to register new collage office
@collage_bp.route("/add_collage",methods=['POST', 'GET'])
@login_required
def add_collage():
    if request.method == 'POST':
        # add collage to database
        collage_list = request.form.getlist('newFieldText[]')

        i = 0
        for value in collage_list:
            Collage.add_collage({
            'collageName':value.strip(),
            'date_registered':datetime.today()
            })
            i +=1
        flash('{} Registered Successfully !'.format(i), 'success')

        return redirect(url_for('collage_bp.collage'))

    return render_template('collage.html')

# deleting selected records from the table
@collage_bp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    try:
        i = 0
        if request.method == 'POST':
            # iteratively delete checked rows
            for getid in request.form.getlist('mycheckbox'):
                #print(getid)
                db.session.query(Collage).filter_by(id = getid).delete()
                db.session.commit()
                i += 1
            flash('{} Deleted'.format(i), 'danger')
            return redirect(url_for('collage_bp.collage'))

    except exc.IntegrityError:
        flash("Can't be Deleted! There is Registered Data by This Collage ID", 'danger')
        return redirect(url_for('collage_bp.collage'))

# deleting a single record from the collage table
@collage_bp.route('/deleteSingle/<int:id>/', methods=['GET', 'POST'])
@login_required
def deleteSingle(id):
    try:

        if request.method == 'GET':
            reg_del = Collage.query.get(id)
            db.session.delete(reg_del)
            db.session.commit()
            flash('1 Deleted'.format(), 'danger')
            return redirect(url_for('collage_bp.collage'))
    except exc.IntegrityError:
        flash("No Deleted! There is Registered Data by This Campus ID", 'danger')
        return redirect(url_for('collage_bp.collage'))


# deleting multiple records from the branch table
@collage_bp.route('/deletebranch', methods=['GET', 'POST'])
@login_required
def deletebranch():
    try:
        i = 0
        if request.method == 'POST':
            # iteratively delete checked rows
            for getid in request.form.getlist('mycheckbox'):
                #print(getid)
                db.session.query(Branch).filter_by(id = getid).delete()
                db.session.commit()
                i += 1
            flash('{} Deleted'.format(i))
            return redirect(url_for('collage_bp.branchInfo', id=session['collageID']))

    except exc.IntegrityError:
        flash("No Deleted! There is Registered Data by This Collage ID")
        return redirect(url_for('collage_bp.branchInfo', id=session['collageID']))

# deleting a single record from the branch table
@collage_bp.route('/deletebranchSingle/<int:id>/', methods=['GET', 'POST'])
@login_required
def deletebranchSingle(id):
    try:

        if request.method == 'GET':
            branch_del = Branch.query.get(id)
            db.session.delete(branch_del)
            db.session.commit()
            flash('1 Deleted'.format())
            return redirect(url_for('collage_bp.branchInfo', id=session['collageID']))
    except exc.IntegrityError:
        flash("No Deleted! There is Registered Data by This Collage ID", 'danger')
        return redirect(url_for('collage_bp.branchInfo', id=session['collageID']))
# Update a single row/ edit the row of the table and automatically update the
# row value in the database through ajax
@collage_bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    try:
        if request.method == 'POST':
            field = request.form['field']
            value = request.form['value']
            editid = request.form['id']
            # store columnName in session
            session['fieldName'] = None
            # Update the collageName if the field or column name is collageName
            if field == 'collageName':
                updatedName = Collage.query.filter_by(id=editid).first()
                updatedName.collageName = value.strip()
                session['fieldName'] = 'collageName'
            # update the branchName if the field or column name is branchName
            if field == 'branchName':
                session['fieldName'] = 'branchName'
                updatedName = Branch.query.filter_by(id=editid).first()
                updatedName.branchName = value.strip()
            db.session.commit() # commit to the databse
            success = 1 # update the success to 1, it  mean True if the column value is updated
            #return redirect('collage_bp.collage')
        return jsonify(success) # return success message
    except Exception as e:
        print(e)

# collage details/  display list of branchs under the selected collage
@collage_bp.route('/branchInfo/<int:id>/', methods=['GET', 'POST'])
@login_required
def branchInfo(id):
    try:
        if request.method=='GET':
            # set collage id to session
            # check the column name first
            session["collageID"] = id
            collageName = db.session.query(Collage.collageName).filter_by(id = id).first()
            all_branch = db.session.query(Branch).filter_by(collageID = id).all()

            return render_template('branch.html', branchs=all_branch, collageName = collageName)
        return render_template('branch.html', branchs=all_branch, collageName = collageName)
    except Exception as e:
        print(e)

# route to register new branch
@collage_bp.route("/add_branch",methods=['POST', 'GET'])
@login_required
def add_branch():
    if request.method == 'POST':
        # add branchs to database
        branch_list = request.form.getlist('newFieldText[]')
        i = 0
        for value in branch_list:
            Branch.add_branch({
            'collageID':request.form['collageID'],
            'branchName':value.strip(),
            'date_r':datetime.today()
            })
            i +=1
        flash("{} Registered Successfully!".format(i))
        return redirect(url_for('collage_bp.branchInfo', id=session['collageID']))
    return render_template('branch.html')
