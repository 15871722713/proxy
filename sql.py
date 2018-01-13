#coding:utf-8

import MySQLdb
import logging

logging.basicConfig(level=logging.INFO)
def creat_db_tb():
	db_list = []
	tb_list = []
	creattable = '''CREATE TABLE iplist (id int primary key AUTO_INCREMENT,ip char(20) ,port char(10),type char(10),src char(10))engine=InnoDB;'''
	creattable_videolist = '''CREATE TABLE videolist (id int primary key AUTO_INCREMENT,name char(200) ,videopreview varchar(1000),videourl varchar(2000))engine=InnoDB;'''
	db = MySQLdb.connect("localhost","root","123456")
	c = db.cursor()
	
	database = c.execute('show databases;')
	for data in c.fetchall():
		db_list.append(data[0])
	if 'test' not in db_list:
		c.execute('create database test')
	
	c.execute('use test')
	tables = c.execute('show tables;')
	for table in c.fetchall():
		tb_list.append(table[0])
	if 'iplist' not in tb_list:
		c.execute(creattable)
	elif 'videolist' not in tb_list:
		c.execute(creattable_videolist)
	db.close()

def executesql(sql):
	db = MySQLdb.connect("localhost","root","123456","test")
	c = db.cursor()
	logging.debug('Start to executesql :%s'%sql)
	c.execute(sql)
	iplist = c.fetchall()
	db.commit()
	db.close()
	return iplist

if __name__ == '__main__':
	creat_db_tb()


