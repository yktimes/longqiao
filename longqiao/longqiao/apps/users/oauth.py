import requests

from bs4 import BeautifulSoup
from . import constants

from celery_tasks.course import tasks as course_tasks
from django_redis import get_redis_connection

class Spider:

    def __init__(self, url):
        self.__uid = ''  # 学号
        self.__real_base_url = ''  # 实际基地址
        self.__base_url = url # 请求地址
        self.__name = ''
        self.__base_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '',
            'ddl_kcxz': '',
            'ddl_ywyl': '',
            'ddl_kcgs': '',
            'ddl_xqbs': '',
            'ddl_sksj': '',
            'TextBox1': '',
            'dpkcmcGrid:txtChoosePage': '1',
            'dpkcmcGrid:txtPageSize': '200',
        }
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }

        self.session = requests.Session()
        self.__now_lessons_number = 0

        self.real_class=None # 班级

    def __set_real_url(self):
        '''
        得到真实的登录地址（无Cookie）
        获取Cookie（有Cookie)
        :return: 该请求
        '''
        try:
            request = self.session.get(self.__base_url, headers=self.__headers)
        except:
            raise
        real_url = request.url
        if real_url != 'http://61.178.64.20:80/' and real_url != 'http://61.178.64.20:80/index.apsx':   # 大学
            self.__real_base_url = real_url[:len(real_url) - len('default2.aspx')]
        else:
            if real_url.find('index') > 0:
                self.__real_base_url = real_url[:len(real_url) - len('index.aspx')]
            else:
                self.__real_base_url = real_url
        return request

    def get_code(self):
        '''
        获取验证码
        :return: 验证码
        '''
        try:
            if self.__real_base_url != constants.OAUTH_URL:

                request = self.session.get(self.__base_url + 'CheckCode.aspx', headers=self.__headers)
                print("得到验证码")

            else:
                print("1111")
                request = self.session.get(self.__real_base_url + 'CheckCode.aspx?', headers=self.__headers)

        except Exception:
            raise

        else:
            code = request.content

            return code



    def __get_login_data(self, uid, password,codes):
        '''
        得到登录数据
        :param uid: 学号
        :param password: 密码
        :param codes：验证码
        :return: 含登录包的data字典
        '''
        self.__uid = uid
        request = self.__set_real_url()
        print("__get_login_data")
        soup = BeautifulSoup(request.text, 'html.parser')
        form_tag = soup.find('input')
        print(form_tag)
        __VIEWSTATE = form_tag['value']
        print("__VIEWSTATE===",__VIEWSTATE)
        code = codes

        print("self.__get_code")
        data = {
            '__VIEWSTATE': __VIEWSTATE,
            'txtUserName': self.__uid,
            'TextBox2': password,
            'txtSecretCode': code,
            'RadioButtonList1': '学生'.encode('gb2312'),
            'Button1': '',
            'lbLanguage': '',
            'hidPdrs': '',
            'hidsc': '',
        }
        return data

    def login(self, uid, password,codes):
        '''
        外露的登录接口
        :param uid: 学号
        :param password: 密码
        :return: 抛出异常或返回是否登录成功的布尔值
        '''

        data = self.__get_login_data(uid, password,codes)
        if self.__real_base_url != 'http://61.178.64.20:80/':
            request = self.session.post(self.__base_url + 'default2.aspx', headers=self.__headers, data=data)

        else:
            request = self.session.post(self.__real_base_url + 'index.aspx', headers=self.__headers, data=data)

        soup = BeautifulSoup(request.text, 'html.parser')
        if request.status_code != requests.codes.ok:
            print('4XX or 5XX Error,try to login again')
            return constants.SERVICE_ERROR # 服务器错误

        if request.text.find('密码错误') > -1:
            print('Password may be error')
            return False
        if request.text.find('用户名不存在') > -1:
            print('Uid may be error')
            return False

        if request.text.find('验证码不正确') > -1:
            print('Code error,please input again')
            return constants.CODE_ERROR # 验证码错误
        try:
            name_tag = soup.find(id='xhxm')
            print(name_tag)
            self.__name = name_tag.string[:len(name_tag.string) - 2]
            print('欢迎' + self.__name)

            return True
        except:
            print('Unknown Error,try to login again.')
            return False

    def get_info(self):

        """
        http://jw.lzlqc.com/xsgrxx.aspx?xh=20160741140&xm=%D1%EE%BF%AD&gnmkdm=N121501

        :return:
        """

        data = {
            'xh': self.__uid,
            'xm': self.__name.encode('gb2312'),
            'gnmkdm': 'N121501',
        }
        self.__headers['Referer'] = self.__base_url + 'xs_main.aspx?xh=' + self.__uid
        request = self.session.get(self.__base_url + 'xsgrxx.aspx', params=data, headers=self.__headers)
        self.__headers['Referer'] = request.url
        soup = BeautifulSoup(request.text, 'html.parser')

        try:
            StudentID = soup.find('span', id='xh').string  # 学号
            name = soup.find('span', id='xm').string  # 姓名
            gender = soup.find('span', id='lbl_xb').string  # 性别
            enrollmentDate = soup.find('span', id='lbl_rxrq').string  # 入学日期
            birthday = soup.find('span', id='lbl_csrq').string  # 出身日期
            department = soup.find('span', id='lbl_xy').string # 系别
            sclass = soup.find('span', id='lbl_xzb').string  # 班级
            classes = soup.find('span', id='lbl_dqszj').string  # 级别


            self.real_class = sclass
            print("""
                            学号： {0}
                            姓名： {1}
                            性别： {2}
                            入学日期： {3}
                            生日: {4}
                            系别： {5}
                            班级： {6}

                            """.format(StudentID, name, gender, enrollmentDate, birthday, department, sclass))
        except:

            raise ("获取信息失败")
        else:
            return StudentID,name,gender,enrollmentDate,birthday,department,sclass,classes

    def get__lessons(self):
        """
        获取课表
        http://jw.lzlqc.com/tjkbcx.aspx?xh=20160741140&xm=%D1%EE%BF%AD&gnmkdm=N121613
        :return:
        """

        data = {
            'xh': self.__uid,
            'xm': self.__name.encode('gb2312'),
            'gnmkdm': 'N121613',
        }
        self.__headers['Referer'] = self.__base_url + 'xs_main.aspx?xh=' + self.__uid
        request = self.session.get(self.__base_url + 'tjkbcx.aspx', params=data, headers=self.__headers)
        self.__headers['Referer'] = request.url
        # soup = BeautifulSoup(request.text, 'html.parser')
        # # self.__set__VIEWSTATE(soup)
        # print("课程：            ")
        #
        #
        # # 获取课表，kburl是课表页面url,为什么有个Referer参数,这个参数代表你是从哪里来的。就是登录后的主界面参数。这个一定要有。
        #
        # content = soup.find('table',id='Table6')
        #
        # banji =) soup.select('option[selected="selected"]')[-1].string
        # print(banji



        course_tasks.getCourse.delay(request.text)

    def __set__VIEWSTATE(self, soup):
        __VIEWSTATE_tag = soup.find('input', attrs={'name': '__VIEWSTATE'})
        self.__base_data['__VIEWSTATE'] = __VIEWSTATE_tag['value']

