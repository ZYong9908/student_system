# 导入日历相关模块
import calendar
# 导入日期时间相关模块
from datetime import datetime
# 导入 Flask 框架中的函数
from flask import Flask, render_template, redirect, request
# 导入自定义函数模块
import functions as func
# 导入学生数据模块
import studentdata as std

# 创建 Flask 应用实例
app = Flask(__name__, static_url_path="/")
# 配置应用的密钥，用于加密会话 cookie 和其他敏感信息
app.secret_key = 'ahdbahibaiuhjonbawiuh'
# 开启调试模式，以便更方便地进行开发和调试
app.debug = True


# 设置默认界面
# 作为默认页面处理程序，将所有请求重定向到 /login 页面。
# @app.route("/") 是一个 Flask 路由装饰器。表示将进入该装饰器下定义的函数。
# return redirect('/login') 返回一个重定向到 /login 页面的响应
@app.route("/")
def default_page():
    return redirect('/login')


# 主界面接口
@app.route('/index')
def main_interface():
    return render_template("index.html")


# 图表统计页面接口
@app.route('/charts')
def charts():
    bar_options = func.char_department()
    pie_options = func.char_gender()
    bar_options1 = func.char_age()
    return render_template('charts.html', bar_options=bar_options, pie_options=pie_options, bar_options1=bar_options1)


# 学生个人信息页面接口(按学号查)
@app.route('/student-datas', methods=['GET', 'POST'])
def student_data():
    if request.method == 'GET':
        # 当请求方法为 GET 时，渲染 student-datas.html 页面。
        return render_template('student-datas.html')
    if request.method == 'POST':
        # 当请求方法为 POST 时，使用 request.form.get() 方法获取表单提交数据，调用自定义模块中的 search_snum_data() 函数查询学生个人信息，并将查询结果作为参数传给 student-datas.html 模板进行渲染。
        data_lst = func.search_snum_data(request.form.get('snum'))
        return render_template('student-datas.html', data_lst=data_lst)


# 添加学生信息
@app.route('/add-student-data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'GET':
        # 当请求方法为 GET 时，渲染 add-student-data.html 页面，供用户添加学生信息。
        return render_template('add-student-data.html')
    if request.method == 'POST':
        # 当请求方法为 POST 时，使用自定义模块中的 add_data() 函数将表单提交的学生信息添加到数据库中，并重定向到 /student-datas 路由来查看更新后的数据。
        func.add_data()
        return redirect('/student-datas')


# 查找全部学生信息接口
@app.route('/all-student-datas')
def all_student_data():
    # 使用自定义模块中 functions.py 文件中的 search_data() 函数来查询所有学生信息。将查询结果保存在 data1_lst 变量中。
    data1_lst = func.search_data()
    # 渲染 student-datas.html 模板，将获取到的学生信息数据 data1_lst 传递给模板进行渲染。
    return render_template('student-datas.html', data1_lst=data1_lst)


# 修改学生信息的接口
@app.route('/update-student-data/<data2_list>', methods=['GET', 'POST'])
def update_student_data(data2_list):
    # 根据 URL 中传递的参数 data2_list 截取出学号 snum。
    snum = data2_list[2:6]
    # 使用自定义模块中的 search_snum_data 函数来查询对应学号的学生详细信息。
    data_list = func.search_snum_data(snum)
    # 判断请求方法是否为 GET。
    if request.method == 'GET':
        # 当请求方法为 GET 时，渲染 update-student-data.html 页面，并将 snum 和 data_list 参数传递给模板。
        return render_template('update-student-data.html', snum=snum, data_list=data_list)
    # 判断请求方法是否为 POST。
    if request.method == 'POST':
        # 当请求方法为 POST 时，使用自定义模块中的 update_data 函数更新数据库中对应的学生信息。
        func.update_data(snum)
        # 更新完成后重定向到 /student-datas 接口查看更新后的所有学生信息。
        return redirect('/student-datas')



# 删除学生信息的接口
@app.route('/delete-student-data/<data_list>')
def delete_student_data(data_list):
    # 使用 URL 中传递的参数 data_list 截取出学号 num。
    num = data_list[2:6]
    # 调用自定义模块中的 Student 类和类方法 delete_data() 来删除对应学号的学生信息。
    std.Student(num, '', '', '', '', '', '').delete_data()
    # 删除完成后重定向到 /student-datas 接口查看删除后的所有学生信息。
    return redirect('/student-datas')



# 毕业学生去向界面的接口
@app.route('/graduation')
def graduation():
    bar_options2 = func.char_direct()
    return render_template('graduation.html', bar_options2=bar_options2)


# 学生选课界面接口(按学号查询）
@app.route('/select-course', methods=['GET', 'POST'])
def select_course():
    if request.method == 'GET':
        return render_template('select-course.html')
    if request.method == 'POST':
        snum = request.form.get('snum')
        course_lst = func.show_snum_course(snum)
        return render_template('select-course.html', course_lst=course_lst)


# 修改学生选课接口
@app.route('/update-select-course/<course_lst>', methods=['GET', 'POST'])
def update_course(course_lst):
    snum = course_lst[1:5]
    course_lst1 = func.show_snum_course(snum)
    if request.method == 'GET':
        return render_template('update-select-course.html', snum=snum, course_lst1=course_lst1)
    if request.method == 'POST':
        func.update_select_course(snum)
        return redirect('/select-course')


# 学生选课界面(全部)
@app.route('/all-select-course')
def all_select_course():
    course_lst1 = func.show_course()
    return render_template('select-course.html', course_lst1=course_lst1)


# 学生成绩界面接口(按学号查)
@app.route('/grade', methods=['GET', 'POST'])
def grade():
    if request.method == 'GET':
        return render_template('grade.html')
    if request.method == 'POST':
        grade_lst = func.search_snum_grade(request.form.get('snum'))
        return render_template('grade.html', grade_lst=grade_lst)


# 全部学生成绩界面接口
@app.route('/all-grade')
def all_grade():
    grade_lst1 = func.search_grade()
    return render_template('grade.html', grade_lst1=grade_lst1)


# 修改学生成绩
@app.route('/update-grade/<grade_list>', methods=['GET', 'POST'])
def update_grade(grade_list):
    snum = grade_list[2:6]
    grade_list1 = func.search_snum_grade(snum)
    if request.method == 'GET':
        return render_template('update-grade.html', grade_list1=grade_list1, snum=snum)
    if request.method == 'POST':
        func.update_grade(snum)
        return redirect('/grade')


# 删除学生成绩的接口
@app.route('/delete-grade/<grade_list>')
def delete_grade(grade_list):
    num = grade_list[2:6]
    std.Grade(num, '', '', '', '').delete_grade()
    return redirect('/grade')


# 录入学生成绩的接口
@app.route('/add-grade', methods=['GET', 'POST'])
def add_grade():
    if request.method == 'GET':
        return render_template('add-grade.html')
    if request.method == 'POST':
        func.add_grade()
        return redirect('/grade')


# 奖惩情况界面接口
@app.route('/reward')
def reward():
    bar_options = func.chart_reward()
    bar_options1 = func.chart_reward_depart()
    reward_list = func.select_all_reward()
    return render_template('reward.html', bar_options=bar_options, bar_options1=bar_options1, reward_list=reward_list)


# 删除奖惩情况
@app.route('/delete-reward/<reward_list>')
def delete_reward(reward_list):
    snum = reward_list[2:6]
    std.Reward(snum, '', '', '', '', '', '', '').delete_reward()
    return redirect('/reward')


# 登录接口
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        res = func.login()
        if res == 1:
            return redirect('/index')
        else:
            return res


@app.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == "GET":
        return render_template("regist.html")
    if request.method == "POST":
        res = func.regist()
        if res == 1:
            return redirect('/login')
        else:
            return res


# 日历接口
@app.route('/calendar')
def show_calendar():
    date = datetime.today()
    this_month = calendar.month_abbr[date.month]
    return render_template('calendar.html', this_month=this_month, date=date, content=func.show_calender(date))


if __name__ == '__main__':
    app.run(port=8000)
