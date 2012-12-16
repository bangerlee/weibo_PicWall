from core.bottle import Bottle, debug, jinja2_template as template, TEMPLATE_PATH, static_file, redirect, request, run, response
from core.lib import template_settings
from business.service.pics_services import PicsService
from business.service.users_services import UsersService
from business.service.seo_services import SeoService
from business.service.black_list_services import BlackListService
from business.service.weibo_services import WeiboService
from business.service.comments_services import CommentsService
from business.service.options_services import OptionsService, get_option
from business import auth, log
import os, json
from settings import STATIC_FILE, DEBUG, TEMP_PATH, PAGESIZE, jsversion, MEMCACHE_KEY

app = Bottle()
debug(DEBUG)
TEMPLATE_PATH.append(TEMP_PATH)

app.install(log.stopwatch)

def get_site_info():
    '''获取站点基本信息'''
    APP_TITLE = get_option('site_name')
    SITE_URL = get_option('site_url', '/')
    return dict(app_title=APP_TITLE,
        site_url=SITE_URL, static_url='%s%s'%(SITE_URL, STATIC_FILE),
        jsversion=jsversion)

#=======SEO BOF=======
@app.get('/sitemap.xml')
def sitemap():
    '''sitemap'''
    response.content_type = 'text/xml'
    return SeoService.sitemap().replace('<urlset', '<?xml-stylesheet type="text/xsl" href="/static/sitemap.xsl"?>\n<urlset')

@app.get('/robots.txt')
def robots():
    response.content_type = 'text/plain'
    return open('robots.txt', 'r').read()
#=======SEO EOF=======

#=======WEIBO BOF=======
@app.get('/callback')
def weibo_callback():
    '''微博callback'''
    r = WeiboService.get_token()
    return r.access_token

@app.get('/init-comments')
def init_comments():
    '''从weibo.com抓取评论'''
    client = WeiboService.get_active_client()
    if type(client)==dict:
        redirect(client['url'])
    return WeiboService.get_comments(client)
#=======WEIBO EOF=======

@app.get('/import')
def import_pic():
    '''抓取数据'''
    return PicsService.add()

@app.get('/index')
@app.get('/')
@app.get('/index/page/<page:re:[0-9]+>')
def index(page=None):
    '''分页获取数据'''
    if not page:
        page = 1
    _entries = PicsService.get_list_by_page(page)
    _count = PicsService.get_count()
    _pagenavi = pages(_count, page)
    return template("index.html", handler=get_site_info(), entries=_entries, pagenavi=_pagenavi, template_settings = template_settings)

@app.get('/show/<id:re:[0-9]+>')
def show(id):
    '''显示具体大图'''
    _data = PicsService.get_by_id(id)
    _sidebar_mostlike = PicsService.get_most_likes()
    _nav = dict(prev=None, next=None)
    if _data:
        _prev = PicsService.get_prev(_data['create_date'])
        _next = PicsService.get_next(_data['create_date'])
    _nav["prev"] = _prev
    _nav['next'] = _next
    _comments = CommentsService.get_by_pid(id)
    return template("show.html", handler=get_site_info(), entry=_data, sidebar_mostlikes=_sidebar_mostlike, template_settings = template_settings, nav=_nav, comments=_comments)

@app.post('/like')
def like():
    '''like图片'''
    return PicsService.like_pic()

@app.get('/init')
def update_pic_height():
    '''更新图片高度'''
    return PicsService.update_pic_height()

@app.get('/static/<filename:re:.*')
def server_static_file(filename):
    return static_file(filename, root='./static/')

def pages(count, current, param=None):
    '''分页链接'''
    #计算总页数
    _tuple = divmod(int(count), PAGESIZE)
    if _tuple[1]==0:
        _count = _tuple[0]
    else:
        _count = _tuple[0]+1

    _page = {"previous":None, "current":current, "next":None, "count":_count, "param":param}
    if int(current)>1 and int(current)<=int(_count):
        _page["previous"] = str(int(current)-1)
    elif int(current)>int(_count) and int(_count)>0:
        _page["previous"] = str(int(_count))

    if int(current)>=1 and int(current)<int(_count):
        _page["next"] = str(int(current)+1)

    return _page

#=======后台管理=======
@app.get('/init-memcache')
@auth.check_login
def update_memcache():
    '''更新memcache中数据'''
    _sitemap = json.loads(SeoService.update_memcache())
    _pages = json.loads(PicsService.init_memcache())
    return json.dumps(dict(sitemap=_sitemap, pages=_pages))

@app.get('/admin/login')
def admin_login():
    '''后台用户登陆'''
    return template("admin/login.html", handler=get_site_info())

@app.post('/admin/login')
def admin_login_post():
    '''登陆'''
    return UsersService.login()

@app.get('/admin/log-out')
def admin_log_out():
    '''退出'''
    UsersService.log_out()
    redirect('/admin/login', 302)

@app.post('/admin/check-email')
def admin_check_is_registered_post():
    '''检查是否已经注册'''
    return UsersService.check_is_registered()

@app.post('/admin/register')
def admin_register():
    '''注册用户'''
    return UsersService.register()

@app.get('/admin')
@app.get('/admin/page/<page:re:[0-9]+>')
@auth.check_login
def admin(page=None):
    '''图片管理页面'''
    if not page:
        page = 1
    _status = request.query.get('status', None)
    _entries = PicsService.get_list_by_page(page, admin=True, source=None, status=_status)
    _count = PicsService.get_count(admin=True, status=_status)
    _pagenavi = pages(_count, page)
    _pagenavi["param"] = request.query_string    #url参数
    return template("admin/pic-list.html", handler=get_site_info(), entries=_entries, pagenavi=_pagenavi, query = request.query)

@app.post('/admin')
@auth.check_login
def admin_post():
    '''删除图片'''
    _action = request.POST.get('action', '')
    if 'delete' == _action:
        return PicsService.delete_pic()
    if 'pass' == _action:
        print '332423'
        return PicsService.pass_pic()
    if 'clean' == _action:
        return PicsService.clean_pic()

@app.get('/admin/user/change-password')
@auth.check_login
def user_change_password():
    '''修改密码'''
    return template("admin/change-password.html", handler=get_site_info())

@app.post('/admin/user/change-password')
@auth.check_login
def user_change_password_post():
    '''修改密码'''
    return UsersService.change_password()

@app.get('/admin/user/manage/page/<page:re:[0-9]+>')
@app.get('/admin/user/manage')
@auth.check_login
def user_manage(page=None):
    '''用户管理'''
    if not page:
        page = 1
    _status = request.query.get('status', None)
    _search = request.query.get('search', None)
    _entries = UsersService.get_list_by_page(page, status=_status, search=_search)
    _count = UsersService.get_count(status=_status, search=_search)
    _pagenavi = pages(_count, page)
    _pagenavi["param"] = request.query_string    #url参数
    return template("admin/user-list.html", handler=get_site_info(), entries=_entries, pagenavi=_pagenavi, query = request.query)

@app.post('/admin/user/manage')
@auth.check_login
def user_manage_post():
    '''用户管理POST数据'''
    _action = request.POST.get('action', '')
    if 'unpass' == _action:
        return UsersService.unpass_user()
    if 'pass' == _action:
        return UsersService.pass_user()

@app.get('/admin/black/page/<page:re:[0-9]+>')
@app.get('/admin/black')
@auth.check_login
def black_manage(page=None):
    '''黑名单管理'''
    if not page:
        page = 1
    _type = request.query.get('type', None)
    _search = request.query.get('search', None)
    _entries = BlackListService.get_list_by_page(page, bType=_type, search=_search)
    _count = BlackListService.get_count(bType=_type, search=_search)
    _pagenavi = pages(_count, page)
    _pagenavi["param"] = request.query_string    #url参数
    return template("admin/black-list.html", handler=get_site_info(), entries=_entries, pagenavi=_pagenavi, query = request.query)

@app.get('/admin/option')
@auth.check_login
def option_manage():
    '''站点基本设置'''
    _data = OptionsService.get_option('%s%s'%(MEMCACHE_KEY, '_option'))
    return template("admin/option.html", handler=get_site_info(), data=_data)

@app.post('/admin/option')
@auth.check_login
def option_manage_post():
    '''站点基本设置POST数据'''
    return OptionsService.update('%s%s'%(MEMCACHE_KEY, '_option'))

@app.post('/admin/black')
@auth.check_login
def black_manage_post():
    '''黑名单管理POST数据'''
    _action = request.POST.get('action', '')
    if 'deleted' == _action:
        return BlackListService.delete_black()
    if 'add' == _action:
        return BlackListService.add()

if __name__ == "__main__":
    # Interactive mode
    import sys
    port = int(sys.argv[1] if len(sys.argv) > 1 else 8888)
    run(app, host='0.0.0.0', port=port, reloader=True)
elif 'SERVER_SOFTWARE' not in os.environ:
    # Mod WSGI launch
    import os
    os.chdir(os.path.dirname(__file__))
    app = app
