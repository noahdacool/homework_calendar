from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
import datetime
import json
from .models import User, Category, Assignment
from . import db

views_blueprint = Blueprint('views_str', __name__)

@views_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if request.form.get('category'):
            text = request.form.get('category')
            add_category_and_color_from(text)
        else:
            for category in current_user.categories:
                if request.form.get(str(category.id)):
                    text = request.form.get(str(category.id))
                    add_assignment_and_date_from_text(text, category)
        return redirect(url_for('views_str.home'))

    weeks = 105
    dates = date_list_for_weeks(weeks)
    categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.index)
    return render_template('calendar.html', user=current_user, dates=dates, weeks=weeks, categories=categories)

@views_blueprint.route('/toggle-visibility', methods=['POST'])
def toggle_visibility():
    data = json.loads(request.data)
    category_id = data['category_id']
    db.session.query(Category).get(category_id).show = not db.session.query(Category).get(category_id).show
    db.session.commit()
    return jsonify({})

@views_blueprint.route('/sort-database', methods=['POST'])
def sort_database():
    data = json.loads(request.data)
    category_ids = data['category_ids']

    i = 0
    for category_id in category_ids:
        db.session.query(Category).get(category_id).index = i
        i += 1
    db.session.commit()
    return jsonify({})

@views_blueprint.route('/delete-assignment', methods=['POST'])
def delete_assignment():
    data = json.loads(request.data)
    assignment_id = data['assignment_id']
    assignment = Assignment.query.get(assignment_id)
    if assignment:
        if assignment.user_id == current_user.id:
            db.session.delete(assignment)
            db.session.commit()
            return jsonify({})

@views_blueprint.route('/delete-category', methods=['POST'])
def delete_category():
    data = json.loads(request.data)
    category_id = data['category_id']
    category = Category.query.get(category_id)
    if category:
        if category.user_id == current_user.id:
            for assignment in category.assignments:
                db.session.delete(assignment)
            db.session.delete(category)
            db.session.commit()
            return jsonify({})

def add_category_and_color_from(text):
    split = text.split(', ')
    if len(split) < 2:
        flash('Must enter both category name and color separated by a comma and space.', 'error')
        return redirect(url_for('views_str.home'))
    color = split.pop(-1).lower()
    category_name = ', '.join(split)
    if len(category_name) < 1:
        flash('Must enter category name.', 'error')
        return redirect(url_for('views_str.home'))
    if '#' in color and len(color) in [4, 7]:
        for i in range(1, len(color)):
            if color[i] not in '0123456789abcdef':
                flash('Must enter valid color.', 'error')
                return redirect(url_for('views_str.home'))
    elif color not in ['black', 'navy', 'darkblue', 'mediumblue', 'blue', 'darkgreen', 'green', 'teal', 'darkcyan', 'deepskyblue', 'darkturquoise', 'mediumspringgreen', 'lime', 'springgreen', 'aqua', 'cyan', 'midnightblue', 'dodgerblue', 'lightseagreen', 'forestgreen', 'seagreen', 'darkslategray', 'darkslategrey', 'limegreen', 'mediumseagreen', 'turquoise', 'royalblue', 'steelblue', 'darkslateblue', 'mediumturquoise', 'indigo', 'darkolivegreen', 'cadetblue', 'cornflowerblue', 'rebeccapurple', 'mediumaquamarine', 'dimgray', 'dimgrey', 'slateblue', 'olivedrab', 'slategray', 'slategrey', 'lightslategray', 'lightslategrey', 'mediumslateblue', 'lawngreen', 'chartreuse', 'aquamarine', 'maroon', 'purple', 'olive', 'gray', 'grey', 'skyblue', 'lightskyblue', 'blueviolet', 'darkred', 'darkmagenta', 'saddlebrown', 'darkseagreen', 'lightgreen', 'mediumpurple', 'darkviolet', 'palegreen', 'darkorchid', 'yellowgreen', 'sienna', 'brown', 'darkgray', 'darkgrey', 'lightblue', 'greenyellow', 'paleturquoise', 'lightsteelblue', 'powderblue', 'firebrick', 'darkgoldenrod', 'mediumorchid', 'rosybrown', 'darkkhaki', 'silver', 'mediumvioletred', 'indianred', 'peru', 'chocolate', 'tan', 'lightgray', 'lightgrey', 'thistle', 'orchid', 'goldenrod', 'palevioletred', 'crimson', 'gainsboro', 'plum', 'burlywood', 'lightcyan', 'lavender', 'darksalmon', 'violet', 'palegoldenrod', 'lightcoral', 'khaki', 'aliceblue', 'honeydew', 'azure', 'sandybrown', 'wheat', 'beige', 'whitesmoke', 'mintcream', 'ghostwhite', 'salmon', 'antiquewhite', 'linen', 'lightgoldenrodyellow', 'oldlace', 'red', 'fuchsia', 'magenta', 'deeppink', 'orangered', 'tomato', 'hotpink', 'coral', 'darkorange', 'lightsalmon', 'orange', 'lightpink', 'pink', 'gold', 'peachpuff', 'navajowhite', 'moccasin', 'bisque', 'mistyrose', 'blanchedalmond', 'papayawhip', 'lavenderblush', 'seashell', 'cornsilk', 'lemonchiffon', 'floralwhite', 'snow', 'yellow', 'lightyellow', 'ivory', 'white']:
        flash('Must enter valid color.', 'error')
        return redirect(url_for('views_str.home'))
    new_category = Category(name=category_name, color=color, user_id=current_user.id, index=len(current_user.categories))
    db.session.add(new_category)
    db.session.commit()
    return redirect(url_for('views_str.home'))

def add_assignment_and_date_from_text(text, category):
    split = text.split(', ')
    if len(split) < 2:
        flash('Must enter both assignment name and date separated by a comma and space.', 'error')
        return redirect(url_for('views_str.home'))
    date_str = split.pop(-1).lower()
    assignment_name = ', '.join(split)
    if len(assignment_name) < 1:
        flash('Must enter assignment_name.', 'error')
        return redirect(url_for('views_str.home'))
    date_str = date_str.split('/')
    if len(date_str) != 3 or '' in date_str:
        flash('Must enter valid date.', 'error')
        return redirect(url_for('views_str.home'))
    if len(date_str[2])==2:
        date_str[2] = '20' + date_str[2]
    date = datetime.datetime(int(date_str[2]), int(date_str[0]), int(date_str[1]))
    new_assignment = Assignment(name=assignment_name, date=date, index=len(category.assignments), category_id=category.id, user_id=category.user_id)
    db.session.add(new_assignment)
    db.session.commit()
    return redirect(url_for('views_str.home'))

def date_list_for_weeks(weeks):
    dates = [['01', 1, '#DDD', [], False]]
    counter = datetime.datetime(2023, 1, 1)
    last_end = 1
    now = datetime.datetime.now()
    date_colors = []
    assignments = Assignment.query.filter_by(user_id=current_user.id).order_by(Assignment.date)
    for a in assignments:
        date_colors.append([datetime.datetime(a.date.year, a.date.month, a.date.day), Category.query.get(a.category_id).color])
    for i in range(0, weeks*7-1):
        counter += datetime.timedelta(days=1)
        date = [counter.strftime('%d'), int(counter.strftime('%m'))]
        if counter == datetime.datetime(now.year, now.month, now.day):
            date.append('lightgreen')
        else:
            date.append('#FFF' if date[1]%2==0 else '#DDD')

        assigned_colors = []
        for date_color in date_colors:
            if date_color[0] == counter:
                assigned_colors.append(date_color[1])
        date.append(assigned_colors)

        if date[1] != dates[-1][1]:
            lastMonth = counter + datetime.timedelta(days=-2)
            date += [True, last_end, (i+8)//7, lastMonth.strftime('%B'), lastMonth.strftime('%Y'), lastMonth.strftime('%y')]
            last_end = (i+8)//7
        else:
            date += [False]
        dates.append(date)
    return dates