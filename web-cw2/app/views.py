from app import app,db
from flask import render_template,redirect,request,url_for,flash,current_app,session,Response
from app.forms import LoginForm, SignupForm,adminLoginForm,passwordChangeForm
from flask_login import login_user, login_required, logout_user, current_user
from app.models import users, orders, rooms, hotels, load_user
from sqlalchemy import and_, or_
from flask_login import login_user
from datetime import datetime
from flask_mail import Message
from app import mail
from threading import Thread

#show the homepage
@app.route('/', methods=['GET','POST'])
def index():
    u = users.query.filter_by(user_name=request.cookies.get('username')).first()
    if u is not None:
        login_user(u)
        return redirect(url_for('hotelList'))
    form = LoginForm()
    if form.validate_on_submit():
        user = users.query.filter_by(user_name=form.log_name.data).first()
        if user is not None and user.verify_password(form.log_password.data):
            resp = redirect(url_for('hotelList'))
            if form.remember_me.data is True:
                resp.set_cookie('username', user.user_name)
                app.logger.info('add cookies for %s',user.user_name)
            login_user(user,form.remember_me.data)
            flash('You have successfully login.')
            app.logger.info('%s log in successfully', user.user_name)
            if current_user.user_name is None:
                app.logger.critical('%s failed to login',user.user_name)
            return resp
        flash('Invalid username or password.')
    return render_template('index.html', form=form)


#admin login page
@app.route('/adminLogin', methods=['GET','POST'])
def adminLogin():
    u = users.query.filter_by(user_name='admin').first()
    form = adminLoginForm()
    if form.validate_on_submit():
        user = users.query.filter_by(user_name='admin').first()
        if user.verify_password(form.admin_password.data):
            login_user(user)
            app.logger.info('successfully log into the management system')
            return redirect(url_for('admin.index'))
        flash('Invalid username or password.')
    return render_template('adminLogin.html', form=form)



@app.route('/secret', methods=['GET','POST'])
@login_required
def secret():
    return 'Only authenticated users are allowed!'


@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    name = current_user.user_name
    logout_user()
    resp = redirect(url_for('index'))
    resp.delete_cookie('username')
    if current_user.is_authenticated:
        app.logger.error('%s failed log out', name)
    else:
        app.logger.info('%s successfully log out', name)
    if request.cookies.get('username') is not None:
        app.logger.warning('failed to delete cookies')
    else:
        app.logger.info('delete user cookies')
    flash('You have been logged out.')
    return resp


# show the registration page
@app.route('/register', methods=['GET','POST'])
def register():
    form = SignupForm()
    num = users.query.count()
    if form.validate_on_submit():
        user = users(user_id=num+1,
                    user_name=form.username.data,
                    password=form.password.data,
                    email=form.email.data,
                    phone=form.phone_number.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!')
        app.logger.info('%s successfully sign up',user.user_name)
        u = users.query.filter_by(user_name=user.user_name).first()
        if u is None:
            app.logger.error('failed to insert %s into users table',user.user_name)
        return redirect(url_for('index'))
    return render_template('register.html',form=form)


# password change
@app.route('/passwordChange', methods=['GET','POST'])
def passwordChange():
    form = passwordChangeForm()
    if form.validate_on_submit():
        user = users.query.filter_by(user_name=form.username.data).first()
        if user is not None and user.verify_password(form.old_password.data):
            user.changePassword(form.new_password.data)
            flash('You have successfully change the password.')
            db.session.commit()
            if user.verify_password(form.new_password.data):
                app.logger.info('%s have successfully change the password',user.user_name)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('passwordChange.html',form=form)



# show the hotel list
@app.route('/hotelList', methods=['GET','POST'])
def hotelList():
    hotel_list = hotels.query.all()
    if request.method == 'POST':
        query = hotels.query
        name = request.form['hotel-name']
        app.logger.debug('get the hotel name %s',name)
        check_in = request.form['check-in']
        app.logger.debug('get the chech-in time %s', check_in)
        check_out = request.form['check-out']
        app.logger.debug('get the check-out time %s', check_out)
        if name is not None:
            query = hotels.query.filter(or_(hotels.hotel_name.like('%'+ name +'%'),
                                                 hotels.hotel_description.like('%'+ name +'%')))
        # get the hotel list with specific name
        hotel_list = query.all()
        if check_in != "" and check_in is not None and check_out !="" and check_out is not None:
            for hotel in hotel_list:
                # 获取符合条件的酒店下的房间列表
                room_list = hotel.rooms
                room_number = 0
                for room in room_list:
                    # 计算当前空闲的房间
                    if room.available==True:
                        room_number += 1
                    else:
                        # 计算在输入日期之前完成订单的房间
                        order_list = room.orders
                        o_list = order_list.filter_by(complete=False).all()
                        flag = 0
                        for order in o_list:
                            if order is not None:
                                if (compare_date(order.end_time,check_in) == 1) or\
                                        (compare_date(order.start_time,check_out) == 0):
                                    flag+=1
                        if (flag==len(o_list)):
                            room_number += 1
                if (room_number == 0):
                    hotel_list.remove(hotel)
                app.logger.debug('Search results: the total number of available rooms in the hotel %s is %d',hotel.hotel_name,room_number)
    return render_template('hotelList.html', hotel_list=hotel_list)

# 比较两个日期
def compare_date(date1, date2):
    d1 = datetime.combine(date1, datetime.min.time())
    d2 = datetime.strptime(date2, "%Y-%m-%d")
    diff = d2 - d1
    if (diff.days <= 0):
        return 0 # date2在前
    else:
        return 1 # date1在前



# show the hotel details
@app.route('/details/<hotel_id>', methods=['GET','POST'])
def details(hotel_id):
    hotel_id=hotel_id
    room_name = []
    room_number_list =[]
    session['check-in-date'] = None
    session['check-out-date'] = None
    query = rooms.query.filter_by(room_hotel_id=hotel_id).group_by(rooms.room_name)
    if request.method == 'POST':
        session['check-in-date'] = request.form['check-in']
        app.logger.debug('set check-in date session as %s',session['check-in-date'])
        session['check-out-date'] = request.form['check-out']
        app.logger.debug('set check-out date session as %s',session['check-out-date'])
        type = request.form['type']
        if type is not None and type != 'All':
            query = query.filter_by(type=type)

    # 获取房间型号的列表
    room_list = query.all()
    if room_list is not None:
        for room in room_list:
            room_name.append(room.room_name)
    else:
        app.logger.error('failed to get room list')
    if session['check-in-date']!="" and session['check-in-date'] is not None:
        #获取每一个型号房间的房间数量
        for name in room_name:
            # 获取符合条件的所有房间列表
            r_list = rooms.query.filter_by(room_name=name)
            room_number = 0
            for r in r_list:
                # 计算当前空闲的房间
                if r.available == True:
                    room_number += 1
                else:
                    # 计算在输入日期之前完成订单的房间
                    order_list = r.orders
                    o_list = order_list.filter_by(complete=False).all()
                    flag = 0
                    for order in o_list:
                        if order is not None:
                            #不符合时间条件时flag加一
                            if (compare_date(order.end_time,session['check-in-date']) == 1) or\
                                (compare_date(order.start_time,session['check-out-date']) == 0):
                                flag += 1
                    if (flag==len(o_list)):
                        room_number += 1
            # 如果房间数量为零则不显示
            if (room_number == 0):
                room_list.remove(query.filter_by(room_name=name).first())
                app.logger.debug('room %s has no available room',name)
            else:
                room_number_list.append(room_number)
                app.logger.debug('Search results: the total number of available rooms %s is %d',name,room_number)
    num = len(room_list)
    return render_template('details.html', room_list=room_list,num=num,
                           hotel_id=hotel_id,check_in=session['check-in-date'],check_out=session['check-out-date'],
                           room_number_list=room_number_list)



# show the order form
@app.route('/order/<hotel_id>,<room_name>,<check_in>,<check_out>,<room_number>', methods=['GET','POST'])
def order(hotel_id,room_name,check_in,check_out,room_number):
    if request.method == 'POST':
        order_number = orders.query.count()
        room_chosen = []
        # 获取需要预定的房间数量和房间列表
        room_list = rooms.query.filter(and_(rooms.room_name == room_name, rooms.room_hotel_id == hotel_id)).all()
        price = room_list[0].price
        n = int(request.form['quantity'])
        for room in room_list:
            # 首先预订当前没有订单的房间
            if room.available == True and n != 0:
                room.available = False
                room_chosen.append(room)
                n -= 1
        for room in room_chosen:
            room_list.remove(room)
        # 剩余房间继续预定
        if (n > 0):
            for room in room_list:
                if n!=0:
                    order_list = room.orders
                    o_list = order_list.filter_by(complete=False).all()
                    flag = 0
                    for order in o_list:
                        if order is not None:
                            if (compare_date(order.end_time, session['check-in-date']) == 1) or\
                                    (compare_date(order.start_time, session['check-out-date']) == 0):
                                flag+=1
                    if (flag==len(o_list)):
                        room_chosen.append(room)
                        n-=1
                else:
                    break
        if (n>0):
            app.logger.error('Shortage of rooms')
        # 插入新的订单记录
        new_order = orders(order_id = order_number+1,
                           quantity = request.form['quantity'],
                           total = price*int(request.form['quantity']),
                           start_time = datetime.strptime(check_in, "%Y-%m-%d").date(),
                           end_time = datetime.strptime(check_out, "%Y-%m-%d").date(),
                           name = request.form['name'],
                           ID_type = request.form['type'],
                           ID_number = request.form['ID-number'],
                           order_email = request.form['email'],
                           order_phone = request.form['phone'],
                           note = request.form['note'],
                           complete = False,
                           order_user_id=current_user.user_id)
        #在中间表中填入数据
        for room in room_chosen:
            new_order.rooms.append(room)
        if (new_order.rooms.count() == int(request.form['quantity'])):
            app.logger.debug('Associated with the correct number of rooms %s',request.form['quantity'])
        else:
            app.logger.debug('Associated with the incorrect number of rooms %d',new_order.rooms.count())
        db.session.add(new_order)
        db.session.commit()
        if (orders.query.count() == order_number):
            app.logger.error('failed to insert a new order into database')
        else:
            app.logger.info('successfully insert a new order into database')
        return redirect(url_for('sendEmail'))
    return render_template('order.html',check_in=check_in,check_out=check_out,room_number=int(room_number),hotel_id=hotel_id)

# show the map
@app.route('/position/<keywords>', methods=['GET','POST'])
def position(keywords):
    address = keywords
    return render_template('position.html', address=address)

# display the account page
@app.route('/account', methods=['GET','POST'])
def account():
    if request.method == 'POST':
        user = users.query.filter_by(user_id=current_user.user_id).first()
        if request.form['modi-name'] is not None and request.form['modi-name']!="":
            if users.query.filter_by(user_name=request.form['modi-name']).first() is not None:
                flash('This username has been used.')
            else:
                user.user_name = request.form['modi-name']
        if request.form['modi-email'] is not None and request.form['modi-email']!="":
            if users.query.filter_by(email=request.form['modi-email']).first() is not None:
                flash('This email has been registered.')
            else:
                user.email = request.form['modi-email']
        if request.form['modi-phone'] is not None and request.form['modi-phone']!="":
            user.phone = request.form['modi-phone']
        db.session.add(user)
        db.session.commit()
        app.logger.info('user %s personal information has been modified',user.user_name)
        return redirect(url_for('account'))
    return render_template('account.html')

# reset sessions
@app.route('/reset')
def reset():
    session['complete'] = 'All'
    session['check-in'] = None
    session['check-out'] = None
    app.logger.debug('account session value has been reset')
    return redirect(url_for('show'))


# display the order list
@app.route('/show',methods=['GET','POST'])
def show():
    # pagination
    page = request.args.get('page', 1, type=int)
    query = orders.query.filter_by(order_user_id=current_user.user_id)
    if request.method == 'POST':
        session['complete'] = request.form['complete']
        session['check-in'] = request.form['check-in']
        session['check-out'] = request.form['check-out']
        app.logger.debug('set account sessions %s, %s, %s',session['complete'],session['check-in'],session['check-out'])
        query = searchActivity(session['complete'],session['check-in'],session['check-out'],query)

    if session['complete'] is not None or session['check-in'] is not None or session['check-out'] is not None:
        query = searchActivity(session['complete'],session['check-in'],session['check-out'],query)

    pagination = query.order_by(orders.set_time.desc()).paginate(page,
           per_page=current_app.config['FLASKY_ORDERS_PER_PAGE'], error_out=False)
    order_list = pagination.items
    # get the order information
    hotel_list = []
    address_list = []
    type_list = []
    num = len(order_list)
    if num != 0:
        app.logger.info('%d matched records in page %d',num,page)
        for order in order_list:
            r_list = order.rooms.all()
            h = hotels.query.filter_by(hotel_id=r_list[0].room_hotel_id).first()
            hotel_list.append(h.hotel_name)
            address_list.append(h.address)
            type_list.append(r_list[0].type)
    else:
        app.logger.info('no matched records')
    return render_template('show.html',pagination=pagination,order_list=order_list,hotel_list=hotel_list,
                           address_list = address_list,type_list=type_list,num=num)

# search orders
def searchActivity(complete,check_in,check_out,query):
    if complete == 'Complete':
        query = query.filter_by(complete=True)
    elif complete == 'Incomplete':
        query = query.filter_by(complete=False)
    if check_in != "" and check_in is not None:
        query = query.filter_by(start_time=datetime.strptime(check_in, "%Y-%m-%d").date())
    if check_out != "" and check_out is not None:
        query = query.filter_by(end_time=datetime.strptime(check_out, "%Y-%m-%d").date())
    return query


#delete orders
@app.route('/delete/<order_id>',methods=['GET','POST'])
def delete(order_id):
    order = orders.query.filter_by(order_id=order_id).first()
    order_id = order.order_id
    room_list = order.rooms.all()
    for room in room_list:
        order.rooms.remove(room)
    db.session.delete(order)
    db.session.commit()
    app.logger.info('%s delete the order %d record', current_user.user_name, order_id)
    return redirect(url_for('reset'))

# Cancel orders
@app.route('/cancel/<order_id>',methods=['GET','POST'])
def cancel(order_id):
    order = orders.query.filter_by(order_id=order_id).first()
    order.complete = True
    room_list = order.rooms.all()
    db.session.commit()
    for room in room_list:
        if room.orders.filter_by(complete=False).count() == 0:
            room.available=True
            db.session.commit()
            app.logger.info('%s cancel the order %d',current_user.user_name,order.order_id)
    return redirect(url_for('reset'))

# send email to confirm
#异步发送电子邮件
def _send_async_mail(app,message):
    with app.app_context():
        mail.send(message)

def send_email(to,template,**kwargs):
    msg = Message(sender=app.config['MAIL_DEFAULT_SENDER'],recipients=[to])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+'.html',**kwargs)
    thr = Thread(target=_send_async_mail, args=[app, msg])
    thr.start()
    return thr

@app.route('/sendEmail',methods=['GET','POST'])
def sendEmail():
    order_number = orders.query.count()
    order = orders.query.filter_by(order_id=order_number).first()
    rooms = order.rooms.all()
    hotel_id = rooms[0].room_hotel_id
    hotel = hotels.query.filter_by(hotel_id=hotel_id)
    order = orders.query.filter_by(order_id=order_number).first()
    send_email(order.order_email,'confirm',order=order,room=rooms[0],hotel=hotel)
    flash('A confirm email has been sent to your email')
    return redirect(url_for('hotelList'))
