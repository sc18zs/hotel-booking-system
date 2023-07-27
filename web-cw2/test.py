import os
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import app,db,mail,login_manager
from app.models import users,rooms,orders,hotels
from flask import Flask,render_template,redirect,request,url_for,flash,current_app,session,Response
from flask_login import login_user, login_required, logout_user, current_user
from app.models import users, orders, rooms, hotels, load_user
from sqlalchemy import and_, or_
from flask_login import login_user
from datetime import datetime
from flask_mail import Message
import json
from datetime import datetime

class TestCase(unittest.TestCase):
    # 首先执行该方法
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        app.app_context().push()
        db.create_all()
        pass

    # 在测试方法后执行
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # 测试用户注册(增加新用户)
    def test_registration(self):
        test_user = users(user_id=1,
                          user_name='testUser',
                          password='11111111')
        db.session.add(test_user)
        db.session.commit()
        new_user = users.query.filter_by(user_id=1).first()
        self.assertIsNotNone(new_user)


    # 数据库测试
    # 测试酒店，房间和订单添加(添加的新订单关联房间信息修改)
    def test_insertOrder(self):
        user = users(user_id=1,user_name="testUser",password="11111111")
        #添加酒店到数据库
        hotel = hotels(hotel_id=1,hotel_name="成都清居酒店")
        db.session.add_all([user,hotel])
        db.session.commit()
        h = hotels.query.filter_by(hotel_name="成都清居酒店").first()
        self.assertIsNotNone(h)

        #添加房间到数据库
        for i in range(1,4):
            room = rooms(room_id=i,room_hotel_id=1,available=False)
            db.session.add(room)
            db.session.commit()
        r_number = rooms.query.count()
        self.assertEqual(r_number,3)

        #增加一个订单(关联三个房间)
        user = user.query.first()
        new_order = orders(order_id=1,quantity=3,order_user_id=user.user_id)
        db.session.add(new_order)
        db.session.commit()
        room_list = rooms.query.all()
        for i in range(0,3):
            new_order.rooms.append(room_list[i])
            room_list[i].available=False
        db.session.commit()
        #验证订单关联的房间数
        order = orders.query.first()
        room_list = order.rooms
        room_number = 0
        for room in room_list:
            if room.available==False:
                room_number+=1
        self.assertEqual(room_number,3)

        #添加多个订单
        new_order = orders(order_id=2, quantity=2, order_user_id=user.user_id)
        db.session.commit()
        room_list = room.query.filter(or_(rooms.room_id==1,rooms.room_id==2)).all()
        for i in range(0,2):
            new_order.rooms.append(room)
        #验证房间关联的订单数量
        room = rooms.query.filter_by(room_id=1).first()
        order_list = room.orders
        order_number=0
        for order in order_list:
            order_number+=1
        self.assertEqual(order_number,1)




if __name__ == '__main__':
    unittest.main()