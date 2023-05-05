# 导入日历模块
import calendar
# 导入 flask 的 request 模块和 pyecharts 中的一些相关类
from flask import request
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie
# 导入自定义模块 studentdata 和学生信息类 Student
import studentdata as std

# 设置周历的第一天为星期7
calendar.setfirstweekday(firstweekday=6)
# 定义一个包含每个星期缩写字母的字符串列表
week = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']


def regist():
    # 从 HTML 页面的表单中获取用户提交的数据，并存储到相应变量中
    username = request.form.get('username')
    password = request.form.get('password')
    re_password = request.form.get('re_password')
    sys_pwd = request.form.get('sys_pwd')
    # 检查输入的两次密码是否一致，如不一致，则返回错误提示信息
    if password != re_password:
        res = '两次密码不一致'
        return res
    # 检查输入的系统密码是否正确，如不正确，则返回错误提示信息
    if sys_pwd != '123456':
        res = '系统密码错误'
        return res
    # 查询该用户名在数据库中是否已存在，如已存在，则返回错误提示信息
    if std.User(username, password).search_user():
        res = '用户名已存在'
        return res
    # 调用 User 类的实例方法 regist 提交注册信息，并将注册结果保存到变量 res 中
    res = std.User(username, password).regist()
    # 将注册结果返回给网页端
    return res


# 登录功能
def login():
    # 从 HTML 页面的表单中获取用户提交的数据，并存储到相应变量中
    username = request.form.get('username')
    password = request.form.get('password')
    # 调用 User 类的实例方法 login 进行登录验证，并将登录结果保存到变量 res 中
    res = std.User(username, password).login()
    # 将登录结果返回给网页端
    return res


# 图表展示各二级学院人数
def char_department():
    # 定义包含六个学院名称的列表 depart_lst
    depart_lst = ['理学院', '计算机学院', '电子学院', '商学院', '海外教育学院', '地理学院']
    # 遍历列表，每次查询对应学院学生数量并将其存储到 num_lst 中
    num_lst = []
    for item in depart_lst:
        student = std.Student('', '', '', '', '', f'{item}', '')
        num_lst.append(len(student.search_department()))
    # 使用 pyecharts 库生成一个柱状图 bar，并设置 x、y 轴的数据和标题等属性
    # 最后将 bar 对象的图表参数以字符串形式返回，交由前端渲染页面显示图表
    bar = (Bar(init_opts=opts.InitOpts(bg_color='lightskyblue')).add_xaxis(depart_lst).add_yaxis("人数", num_lst).set_global_opts(
        title_opts=opts.TitleOpts(title="各学院学生人数")))
    bar_options = bar.dump_options()
    return bar_options


# 图表展示男女比例
def char_gender():
    # 定义两个学生对象，分别查询男生和女生的数量
    student1 = std.Student('', '', '男', '', '', '', '')
    student2 = std.Student('', '', '女', '', '', '', '')
    # 使用 pyecharts 库生成一个饼图 pie，并设置图表标题等属性
    res1 = len(student1.search_gender())
    res2 = len(student2.search_gender())
    pie = (Pie(init_opts=opts.InitOpts(bg_color='lightgoldenrodyellow')).add('', [('男生', res1), ('女生', res2)])
           .set_global_opts(title_opts=opts.TitleOpts(title='男女学生比例'))
           .set_series_opts(label_opts=opts.LabelOpts(formatter='')))
    pie_options = pie.dump_options()
    # 最后将 pie 对象的图表参数以字符串形式返回，交由前端渲染页面显示图表
    return pie_options


# 图表展示各年龄学生人数
def char_age():
    # 定义包含八个年龄的列表 age_lst
    age_lst = [18, 19, 20, 21, 22, 23, 24, 25]
    # 遍历列表，每次查询对应学院学生数量并将其存储到 num_lst 中
    num_lst = []
    for item in age_lst:
        student = std.Student('', '', '', f'{item}', '', '', '')
        num_lst.append(len(student.search_age()))
    # 使用 pyecharts 库生成一个柱状图 bar，并设置 x、y 轴的数据和标题等属性
    bar = (Bar(init_opts=opts.InitOpts(bg_color='cornflowerblue')).add_xaxis(age_lst).add_yaxis("人数", num_lst).set_global_opts(
        title_opts=opts.TitleOpts(title="各年龄学生人数")))
    bar_options = bar.dump_options()
    return bar_options


# 图表展示毕业去向
def char_direct():
    num_lst = []
    # 定义包含五个毕业去向的列表 direct_lst
    direct_lst = ['考研', '考公', '考编', '工作', '留学']
    # 遍历列表，每次查询对应学院学生数量并将其存储到 num_lst 中
    for item in direct_lst:
        gradu = std.Graduation('', f'{item}')
        num_lst.append(len(gradu.search_direct()))
    # 使用 pyecharts 库生成一个柱状图 bar，并设置 x、y 轴的数据和标题等属性
    bar = (Bar(init_opts=opts.InitOpts(bg_color='lightskyblue')).add_xaxis(direct_lst)
           .add_yaxis("人数", num_lst).set_global_opts(title_opts=opts.TitleOpts(title="毕业去向图")))
    bar_options = bar.dump_options()
    return bar_options


# 按学号查找单个学生的个人信息
def search_snum_data(snum):
    # 调用 Student 类的实例方法 search_datas 进行查询，并将查询结果保存到变量 data_lst1 中
    data_lst1 = [std.Student(snum, '', '', '', '', '', '').search_datas()]
    return data_lst1


# 查找全部学生的个人信息
def search_data():
    # 调用 Student 类的实例方法 search_students 进行查询，并将查询结果保存到变量 data_lst 中
    data_lst = std.Student('', '', '', '', '', '', '').search_students()
    return data_lst


# 修改学生信息
def update_data(snum):
    st = []
    lst = ['name', 'gender', 'age', 'native-place', 'department', 'class-id']
    # 遍历列表，每次获取对应表单项的值并添加到 st 列表中
    for item in lst:
        st.append(request.form.get(f'{item}'))
    # 调用 Student 类的实例方法 update_datas 进行修改
    std.Student(snum, st[0], st[1], st[2], st[3], st[4], st[5]).update_datas()


# 添加学生信息
def add_data():
    lst = ['snum1', 'name', 'gender', 'age', 'native-place', 'department', 'class-id']
    data_lst = []
    for item in lst:
        data_lst.append(request.form.get(f'{item}'))
    # 调用 Student 类的实例方法 add_datas 进行添加
    std.Student(data_lst[0], data_lst[1], data_lst[2], data_lst[3], data_lst[4], data_lst[5], data_lst[6]).add_datas()


# 按学号查找所有学生的选课信息
def show_course():
    course_lst = []
    # 遍历学号，每次查询对应学号的选课信息并将其添加到 course_lst 中
    for item in range(1006, 1106):
        course_lst.append(std.Course(f'{item}', '', '', '', '').search_course())
    return course_lst


# 按学号查找单个学生的选课信息
def show_snum_course(snum):
    # 调用 Course 类的实例方法 search_course 进行查询，并将查询结果保存到变量 course_lst 中
    course_lst = [std.Course(snum, '', '', '', '').search_course()]
    return course_lst


# 修改学生选课信息
def update_select_course(snum):
    course_lst = ['course1', 'course2', 'course3', 'course4']
    update_lst = []
    # 遍历列表，每次获取对应表单项的值并添加到 update_lst 列表中
    for item in course_lst:
        update_lst.append(request.form.get(f'{item}'))
    std.Course(snum, update_lst[0], update_lst[1], update_lst[2], update_lst[3]).update_course()


# 按学号查找单个学生的成绩
def search_snum_grade(snum):
    # 调用 Grade 类的实例方法 search_snum_grade 进行查询，并将查询结果保存到变量 grade_lst 中
    grade_lst = [std.Grade(snum, '', '', '', '').search_snum_grade()]
    return grade_lst


# 查找全部学生的成绩
def search_grade():
    # 调用 Grade 类的实例方法 search_grade 进行查询，并将查询结果保存到变量 grade_lst 中
    grade_lst = (std.Grade('', '', '', '', '').search_grade())
    return grade_lst


# 修改学生成绩
def update_grade(snum):
    st = []
    lst = ['course1', 'course2', 'course3', 'course4']
    # 遍历列表，每次获取对应表单项的值并添加到 st 列表中
    for item in lst:
        st.append(request.form.get(f'{item}'))
    # 调用 Grade 类的实例方法 update_grade 进行修改
    std.Grade(snum, st[0], st[1], st[2], st[3]).update_grade()


# 录入学生成绩
def add_grade():
    lst = ['snum', 'course1', 'course2', 'course3', 'course4']
    grade_lst = []
    # 遍历列表，每次获取对应表单项的值并添加到 grade_lst 列表中
    for item in lst:
        grade_lst.append(request.form.get(f'{item}'))
    # 调用 Grade 类的实例方法 add_grade 进行添加
    std.Grade(grade_lst[0], grade_lst[1], grade_lst[2], grade_lst[3], grade_lst[4]).add_grade()


# 图表展示各奖惩情况
def chart_reward():
    num_lst = []
    reward_lst = ['一等奖', '二等奖', '三等奖', '记过处分', '未获奖', '进步奖', '三好学生']
    # 遍历列表，每次获取对应表单项的值并添加到 num_lst 列表中
    for item in reward_lst:
        rew = std.Reward('', '', '', '', '', '', '', f'{item}')
        num_lst.append(len(rew.search_reward()))
    # 调用 Bar 类的实例方法 add_xaxis 和 add_yaxis 进行添加
    bar = (Bar().add_xaxis(reward_lst).add_yaxis("人数", num_lst).set_global_opts(title_opts=opts.TitleOpts(title="奖惩情况统计图")))
    bar_options = bar.dump_options()
    return bar_options


# 图表展示各学院获得奖项人数
def chart_reward_depart():
    num_lst = []
    depart_lst = ['理学院', '计算机学院', '电子学院', '商学院', '海外教育学院', '地理学院']
    # 遍历列表，每次获取对应表单项的值并添加到 num_lst 列表中
    for item in depart_lst:
        rew = std.Reward('', '', '', '', '', f'{item}', ',', '').search_reward_snum()
        num_lst.append(len(rew))
    # 调用 Bar 类的实例方法 add_xaxis 和 add_yaxis 进行添加
    bar = (Bar(init_opts=opts.InitOpts(bg_color='lightskyblue')).add_xaxis(depart_lst)
           .add_yaxis("人数", num_lst).set_global_opts(title_opts=opts.TitleOpts(title="各二级学院获奖人数"), ))
    bar_options = bar.dump_options()
    return bar_options


# 查询所有奖惩的学号，姓名，二级学院，奖项
def select_all_reward():
    # 调用 Reward 类的实例方法 search_all_reward 进行查询，并将查询结果保存到变量 reward_list 中
    reward_list = std.Reward('', '', '', '', '', '', '', '').search_all_reward()
    return reward_list


# 展示日历
def show_calender(date):
    # 获取当前年份
    year = date.year
    # 调用 calendar 库的 monthcalendar 方法获取当前年份的日历信息
    yearInfo = dict()
    # 遍历月份，每次获取对应月份的日历信息并添加到 yearInfo 字典中
    for month in range(1, 13):
        # 获取当前月份的日历信息
        days = calendar.monthcalendar(year, month)
        if len(days) != 6:
            # 如果当前月份的日历信息不足6行，则添加一行
            days.append([0 for _ in range(7)])
        # 获取当前月份的简写
        month_addr = calendar.month_abbr[month]
        yearInfo[month_addr] = days
    return yearInfo
