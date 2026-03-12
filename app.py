from flask import Flask, request, render_template, session, redirect, url_for
import time
from dao.getCommentsData import getCommentsList
from dao.getDaPing import getDaPingData
from dao.getPublicData import *
from dao.getPageData import *
from dao.getTableData import getTableData
from dao.getDaPing import getDaPingData
from predictive.getHistoryData import *
from db import querys
import sys
import io
from predictive.machine import getUser_ratings, user_basee_collaborative_filtering
from predictive.yuce import getYuCe

# Set stdout encoding to UTF-8 to avoid garbled Chinese output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8-sig')

app = Flask(__name__)
app.secret_key = '123456789'

@app.route('/')
def hello_world():  # Main entry point of the application
    return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        request.form = dict(request.form)
        print(request.form)
        
        # Verify if the submitted credentials exist in the database (login validation)
        def filter_fns(item):
            return request.form['username'] in item and request.form['password'] in item
        
        users = querys('select * from user', [], 'select')
        login_success = list(filter(filter_fns, users))
        
        if not len(login_success):
            return 'Invalid username or password'

        session['username'] = request.form['username']
        return redirect('/home')

        return render_template('./pages-login.html')
    else:
        return render_template('./pages-login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        request.form = dict(request.form)
        
        # Check if all required fields are filled
        if request.form['username'] and request.form['password'] and request.form['passwordChecked']:
            # Verify password consistency
            if request.form['password'] != request.form['passwordChecked']:
                return 'Passwords do not match'
            else:
                # Check if username already exists
                def filter_fn(item):
                    return request.form['username'] in item
                
                users = querys('select * from user', [], 'select')
                filter_list = list(filter(filter_fn, users))
                
                if len(filter_list):
                    return 'Username already exists'
                else:
                    # Insert new user into database
                    querys('insert into user(username,password) values(%s,%s)',
                           [request.form['username'], request.form['password']])
        else:
            return 'Username or password cannot be empty'
        
        return redirect('/login')
    else:
        return render_template('./pages-register.html')

@app.route('/home', methods=['GET','POST'])
def home():
    username = session['username']
    totalCount, maxLikeUser, maxRepostUser, maxCommentUser = getHeadData()
    xData1, yData1, weibo_data = getHomeData()
    
    return render_template('index.html',
                           username=username,
                           totalCount=totalCount,
                           maxLikeUser=maxLikeUser,
                           maxRepostUser=maxRepostUser,
                           maxCommentUser=maxCommentUser,
                           xData1=xData1,
                           yData1=yData1,
                           weibo_data=weibo_data
                           )

@app.route('/tableData',methods=['GET','POST'])
def tableData():
    username = session['username']
    totalCount, maxLikeUser, maxRepostUser, maxCommentUser= getHeadData()
    bozhu_table = getTableData()
    
    names, future_reposts, future_likes = getYuCe()
    
    return render_template('tableData.html',
                           username=username,
                           totalCount=totalCount,
                           maxLikeUser=maxLikeUser,
                           maxRepostUser=maxRepostUser,
                           maxCommentUser=maxCommentUser,
                           bozhu_table=bozhu_table,
                           names=names,
                           future_reposts=future_reposts,
                           future_likes=future_likes
                           )

@app.route('/daping', methods=['GET','POST'])
def daping():
    username = session['username']
    totalCount, maxLikeUser, maxRepostUser, maxCommentUser = getHeadData()
    
    # Get dashboard data (daping = dashboard)
    total_follower_over_10m, max_hot_weibo_likes, xData2, yData2, followerList_list, xData3, yData3, userDataList, xData4, yData4_1, yData4_2, yData4_3 = getDaPingData()
    blogger_table = getTableData()
    
    return render_template('daping.html',
                           username=username,
                           totalCount=totalCount,
                           maxLikeUser=maxLikeUser,
                           maxRepostUser=maxRepostUser,
                           maxCommentUser=maxCommentUser,
                           total_follower_over_10m=total_follower_over_10m,
                           max_hot_weibo_likes=max_hot_weibo_likes,
                           bozhu_table=blogger_table,
                           xData2=xData2,
                           yData2=yData2,
                           followerList_list=followerList_list,
                           xData3=xData3,
                           yData3=yData3,
                           userDataList=userDataList,
                           xData4=xData4,
                           yData4_1=yData4_1,
                           yData4_2=yData4_2,
                           yData4_3=yData4_3
                           )

@app.route('/addHistory/<int:weiboId>', methods=['GET','POST'])
def addHistory(weiboId):
    username = session['username']
    
    # Get user ID from database
    userId = querys('select id from user where username = %s', [username], 'select')[0][0]
    # Verify weibo ID exists
    weiboID = querys('select id from weibo where id = %s', [weiboId], 'select')[0][0]
    # Get weibo profile URL
    weiboUrl = querys('select full_profile_url from weibo where id = %s', [weiboId], 'select')[0][0]
    
    # Record follow history
    getData(userId, weiboID)
    
    return redirect(weiboUrl)

@app.route('/search', methods=['GET','POST'])
def search():
    username = session['username']
    totalCount, maxLikeUser, maxRepostUser, maxCommentUser = getHeadData()
    
    if request.method == 'POST':
        searchWord = dict(request.form)['searchIpt']

        # Filter weibo data by search keyword
        def filter_fn(item):
            return item[1].find(searchWord) != -1

        # Get all weibo data
        all_weibo = getAllWeibo()

        # Use set to store seen usernames (avoid duplicates)
        seen_usernames = set()
        unique_data = []

        for item in all_weibo:
            if filter_fn(item):
                username = item[1]
                if username not in seen_usernames:
                    seen_usernames.add(username)
                    unique_data.append(item)

        data = unique_data
        
        return render_template('search.html',
                               totalCount=totalCount,
                               maxLikeUser=maxLikeUser,
                               maxRepostUser=maxRepostUser,
                               maxCommentUser=maxCommentUser,                              
                               username=username,
                               data=data
                               )
    else:
        return render_template('search.html',
                               totalCount=totalCount,
                               maxLikeUser=maxLikeUser,
                               maxRepostUser=maxRepostUser,
                               maxCommentUser=maxCommentUser,
                               username=username,
                               )

@app.route('/recommend', methods=['GET'])
def recommend():
    username = session.get('username')
    totalCount, maxLikeUser, maxRepostUser, maxCommentUser = getHeadData()
    
    if username:
        # Get user rating data for recommendation algorithm
        user_ratings = getUser_ratings()
        # Get recommendation results using user-based collaborative filtering
        recommended_items = user_basee_collaborative_filtering(username, user_ratings)
        
        # Get detailed information for recommended bloggers from database
        data = []
        for item in recommended_items:
            weibo = querys("select * from weibo where username = %s", [item], 'select')
            if weibo:
                data.append(weibo[0])  # Weibo data from database is a tuple

        return render_template('recommend.html',
                               totalCount=totalCount,
                               maxLikeUser=maxLikeUser,
                               maxRepostUser=maxRepostUser,
                               maxCommentUser=maxCommentUser,
                               username=username,
                               data=data)
    else:
        return redirect('/login')

@app.route('/comments', methods=['GET'])
def comments():
    username = session.get('username')
    totalCount, maxLikeUser, maxRepostUser, maxCommentUser = getHeadData()
    
    # Get comment list with sentiment analysis results
    comments = getCommentsList(file_path1='./predictive/bingmayong1_with_sentiment.csv')
    
    return render_template('comments.html',
                           totalCount=totalCount,
                           maxLikeUser=maxLikeUser,
                           maxRepostUser=maxRepostUser,
                           maxCommentUser=maxCommentUser,
                           username=username,
                           comments=comments
                           )

@app.route('/emotion', methods=['GET'])
def emotion():
    username = session.get('username')
    totalCount, maxLikeUser, maxRepostUser, maxCommentUser = getHeadData()
    
    return render_template('emotion.html',
                           totalCount=totalCount,
                           maxLikeUser=maxLikeUser,
                           maxRepostUser=maxRepostUser,
                           maxCommentUser=maxCommentUser,
                           username=username,
                           )

@app.route('/yuce', methods=['GET'])
def predict():  # Renamed: yuce -> predict (more semantic)
    username = session.get('username')
    totalCount, maxLikeUser, maxRepostUser, maxCommentUser = getHeadData()
    
    # Get prediction data (yuce = prediction)
    names, future_reposts, future_likes = getYuCe()
    
    return render_template('yuce.html',
                           totalCount=totalCount,
                           maxLikeUser=maxLikeUser,
                           maxRepostUser=maxRepostUser,
                           maxCommentUser=maxCommentUser,
                           username=username,
                           names=names,
                           future_reposts=future_reposts,
                           future_likes=future_likes,
                           )

@app.route('/loginOut', methods=['GET','POST'])
def logout():  # Renamed: loginOut -> logout (standard naming convention)
    # Clear user session for logout
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run()