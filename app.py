from flask import Flask, render_template, flash, redirect, request

from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, IntegerField, TextField
from wtforms.validators import DataRequired

import datetime
import os

from app_scripts.DB_manager import PortfolioPageDB
from app_scripts.content_helpers import post_intro_html, proj_intro_html, article_to_html, project_to_html, create_page_nav



app = Flask(__name__)
app.config.from_object(__name__) 
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdD2'



@app.route('/', methods=['GET', 'POST'])
def home_page():
	
	credentials = {'dbname':'lp_portfolio_articles', 'dbuser':'luke'}
	DB = PortfolioPageDB(credentials)
	articles = DB.get_articles()
	project_intros = DB.get_projects()

	display_N_articles = 3
	posts_intros_html = [post_intro_html(p, intro_body_size=150) for p in articles[:display_N_articles]]

	display_N_projects = 3
	project_intros_html = [proj_intro_html(p, intro_body_size=150) for p in project_intros[:display_N_projects]]

	return render_template('home.html', posts_intros=posts_intros_html, project_intros=project_intros_html) 


@app.route('/about', methods=['GET', 'POST'])
def about_page():
	data = 'data'
	return render_template('about.html', data=data)


@app.route('/portfolio', methods=['GET', 'POST'])
@app.route('/portfolio/p0', methods=['GET', 'POST'])
@app.route('/portfolio/<identifier>', methods=['GET', 'POST'])
def portfolio_page(identifier='p0', display_N_projects=10):	

	credentials = {'dbname':'lp_portfolio_articles', 'dbuser':'luke'}
	DB = PortfolioPageDB(credentials)
	projects = DB.get_projects()

	page_num = int(identifier[1:])

	project_intros = []
	cnt = 0
	for a in projects[display_N_projects*page_num:]:
		if cnt < display_N_projects:
			project_intros.append(a)
			cnt +=1

	project_intros_html = [proj_intro_html(p, 500) for p in project_intros]

	max_page = len(projects) / display_N_projects
	if max_page == int(max_page):
		max_page = int(max_page) - 1
	elif max_page > int(max_page):
		max_page = int(max_page)

	page_nav = create_page_nav('portfolio', page_num, max_page)
	return render_template('portfolio.html', project_intros=project_intros_html, page_nav=page_nav) 

@app.route('/blog', methods=['GET', 'POST'])
@app.route('/blog/p0', methods=['GET', 'POST'])
@app.route('/blog/<identifier>', methods=['GET', 'POST'])
def blog_page(identifier='p0', display_N_articles=10):

	credentials = {'dbname':'lp_portfolio_articles', 'dbuser':'luke'}
	DB = PortfolioPageDB(credentials)
	articles = DB.get_articles()

	page_num = int(identifier[1:])

	displayed_posts = []
	cnt = 0
	for a in articles[display_N_articles*page_num:]:
		if cnt < display_N_articles:
			displayed_posts.append(a)
			cnt +=1

	posts_intros_html = [post_intro_html(p) for p in displayed_posts]

	max_page = len(articles) / display_N_articles
	if max_page == int(max_page):
		max_page = int(max_page) - 1
	elif max_page > int(max_page):
		max_page = int(max_page)

	page_nav = create_page_nav('blog', page_num, max_page)
	return render_template('blog.html', posts_intros=posts_intros_html, page_nav=page_nav)


@app.route("/post/<identifier>")
def post(identifier):

	credentials = {'dbname':'lp_portfolio_articles', 'dbuser':'luke'}
	DB = PortfolioPageDB(credentials)
	articles = DB.get_articles()

	this_article = [a for a in articles if a[0] == int(identifier)][0]
	this_article_id = this_article[0]
	article_html = article_to_html(this_article, this_article_id)

	if article_html:
		return render_template('article_page.html', article=article_html)
	else:
		return 'Nope, 404, there is no post {}. IDs are starting from 1 and the newest post id is {}'.format(identifier, highest_id)

@app.route("/proj/<identifier>")
def project(identifier):

	credentials = {'dbname':'lp_portfolio_articles', 'dbuser':'luke'}
	DB = PortfolioPageDB(credentials)
	projects = DB.get_projects()

	this_proj = [a for a in projects if a[0] == int(identifier)][0]
	this_proj_id = this_proj[0]
	this_proj_html = project_to_html(this_proj, this_proj_id)
	
	if this_proj_html:
		return render_template('project_page.html', project_html=this_proj_html)
	else:
		return 'Nope, 404, there is no post {}. IDs are starting from 1 and the newest post id is {}'.format(identifier, highest_id)

	max_proj_id = max([i[0] for i in DB.get_column_values('id', 'lp_projects')])
	highest_id = max_proj_id
	this_project_id = highest_id
	for project_data in projects:
		if str(this_project_id) == identifier:
			project_html = project_to_html(project_data, this_project_id)
			return render_template('project_page.html', project_html=project_html)
		this_project_id -= 1
	return 'Nope, 404, there is no post {}. IDs are starting from 1 and the newest post id is {}'.format(identifier, highest_id)
    

# 5. Miscs.
@app.route('/miscs', methods=['GET', 'POST'])
def miscs_page():
	data = 'data'
	return render_template('miscs.html', data=data)


# 6. Contact page.
@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
	data = 'data'
	return render_template('contact.html', data=data)



class AddArticleForm(FlaskForm):
	
	select_choices = [(str(sc), str(sc)) for sc in ['Article', 'Project']]
	content_type = SelectField(choices=select_choices, validators=[DataRequired()], default='Article')

	login = StringField('Login:', validators=[DataRequired()], default='a')
	password = StringField('Password:', validators=[DataRequired()], default='a')

	title = StringField('Article title:', validators=[DataRequired()])
	category = StringField('Category:', validators=[DataRequired()])
	tags = StringField('Tags:', validators=[DataRequired()])

	article = TextField('Article contents:', validators=[DataRequired()])

	art_submit_button = SubmitField('Confirm your pick.')

class AdminManageForm(FlaskForm):
	update = StringField('up:', validators=[DataRequired()], default='a',)
	delete = StringField('up:', validators=[DataRequired()], default='a')
	login = StringField('Login:', validators=[DataRequired()], default='a')
	password = StringField('Password:', validators=[DataRequired()], default='a')


@app.route('/manage', methods=['GET', 'POST'])
@app.route('/admin/manage', methods=['GET', 'POST'])
def admin_manage_page():

	# DB
	credentials = {'dbname':'lp_portfolio_articles', 'dbuser':'luke'}
	DB = PortfolioPageDB(credentials)

	def get_proj_pack():
		proj_titles = [t[0] for t in DB.get_column_values('title', 'lp_projects')]
		proj_ids = [i[0] for i in DB.get_column_values('id', 'lp_projects')]
		proj_links = ['/proj/{}'.format(i) for i in proj_ids]
		proj_pack = zip(proj_links, proj_titles, proj_ids)
		return proj_pack

	def get_art_pack():
		art_titles = [t[0] for t in DB.get_column_values('title', 'lp_articles')]
		art_ids = [i[0] for i in DB.get_column_values('id', 'lp_articles')]
		art_links = ['/post/{}'.format(i) for i in art_ids]
		art_pack = zip(art_links, art_titles, art_ids)
		return art_pack

	proj_pack = get_proj_pack()
	art_pack = get_art_pack()

	# FORM
	AMF = AdminManageForm()
		
	# AUTHORIZE 
	admin_login = 'a'
	admin_password = 'a'
	required = (admin_login, admin_password)
	current = (AMF.login.data, AMF.password.data)
	if current == required and request.method == 'POST':
		
		response = list(request.form)
		target = [w.split('_')[1] for w in response if 'update_' in w or 'delete_' in w][0]
		action_alias = [w.split('_')[0] for w in response if 'update_' in w or 'delete_' in w][0]
		position_id = [w.split('_')[2] for w in response if 'update_' in w or 'delete_' in w][0]
		
		if target == 'proj':
			if 'update' in action_alias:
				return redirect('/proj/{}/update'.format(position_id))
			elif 'delete' in action_alias:
				DB.delete_proj_by_id(position_id)
				proj_pack = get_proj_pack()
				art_pack = get_art_pack()
				return render_template('manage.html', AMF=AMF, project_titles_links=proj_pack, art_titles_links=art_pack)
		elif target == 'art':
			if 'update' in action_alias:
				return redirect('/post/{}/update'.format(position_id))
			elif 'delete' in action_alias:
				DB.delete_art_by_id(position_id)
				proj_pack = get_proj_pack()
				art_pack = get_art_pack()

				return render_template('manage.html', AMF=AMF, project_titles_links=proj_pack, art_titles_links=art_pack)

	return render_template('manage.html', AMF=AMF, project_titles_links=proj_pack, art_titles_links=art_pack)

@app.route('/admin', methods=['GET', 'POST'])
@app.route('/create', methods=['GET', 'POST'])
@app.route('/admin/create', methods=['GET', 'POST'])
def admin_create_page():

	# DB
	credentials = {'dbname':'lp_portfolio_articles', 'dbuser':'luke'}
	DB = PortfolioPageDB(credentials)
	existing_art_titles = DB.get_article_titles()
	existing_proj_titles = DB.get_projects_titles()

	# FORM
	AAF = AddArticleForm()
		
	# AUTHORIZE 
	admin_login = 'a'
	admin_password = 'a'
	required = (admin_login, admin_password)
	current = (AAF.login.data, AAF.password.data)
	if current == required and request.method == 'POST':

		if AAF.content_type.data == 'Article' and not AAF.title.data in existing_art_titles:

			art_id = str( DB.db_get_top_id()+1)
			art_publish_date = datetime.datetime.now(datetime.timezone.utc)
			art_author = 'xxx'

			art_title = AAF.title.data
			art_body = AAF.article.data
			art_category = AAF.category.data
			art_tags = AAF.tags.data

			article_data_pack = [art_id, art_title, art_author, art_publish_date, art_body, art_category, art_tags ]
		
			DB.add_article_to_lp_articles(article_data_pack)
			flash('Added {} to articles.'.format(art_title))

		elif AAF.content_type.data == 'Article' and AAF.title.data in existing_proj_titles:
			flash('The title {} already exists.'.format(AAF.title.data))
		
		elif AAF.content_type.data == 'Project' and not AAF.title.data in existing_proj_titles:

			art_id = str( DB.db_get_top_project_id()+1)
			art_publish_date = datetime.datetime.now(datetime.timezone.utc)
			art_author = 'xxx'

			art_title = AAF.title.data
			art_body = AAF.article.data
			art_category = AAF.category.data
			art_tags = AAF.tags.data

			article_data_pack = [art_id, art_title, art_author, art_publish_date, art_body, art_category, art_tags ]

			DB.add_project_to_lp_projects(article_data_pack)

		elif AAF.content_type.data == 'Project' and AAF.title.data in existing_art_titles:
			flash('The title {} already exists.'.format(AAF.title.data))
	
		elif current != required:
			flash('Wrong login/password.')

	return render_template('create.html', AAF=AAF)


@app.route('/post/<identifier>/update', methods=['GET', 'POST'])
def admin_update_post_page(identifier):

	# DB
	credentials = {'dbname':'lp_portfolio_articles', 'dbuser':'luke'}
	DB = PortfolioPageDB(credentials)

	# CONTENT
	articles = DB.get_articles()
	this_article_data = [a for a in articles if a[0] == int(identifier)][0]
	this_article_id = this_article_data[0]

	class UpdateArticleForm(FlaskForm):
		login = StringField('Login:', validators=[DataRequired()], default='a')
		password = StringField('Password:', validators=[DataRequired()], default='a')
		title_field = StringField('Article title:', validators=[DataRequired()], default=this_article_data[1])
		category_field =  StringField('Category:', validators=[DataRequired()], default=this_article_data[5])
		tags_field =  StringField('Tags:', validators=[DataRequired()], default=this_article_data[6])
		body_field = TextField('Article contents:', validators=[DataRequired()], default=this_article_data[4])

		submit_button = SubmitField('Confirm your pick.')
		delete_button = SubmitField('Delete post.')

	UAF = UpdateArticleForm()
	admin_login = 'a'
	admin_password = 'a'
	required = (admin_login, admin_password)
	current = (UAF.login.data, UAF.password.data)
	if current == required and request.method == 'POST':

		if not UAF.delete_button.data:
			# Update content data.
			new_title = UAF.title_field.data
			new_body = UAF.body_field.data
			new_category = UAF.category_field.data
			new_tags = UAF.tags_field.data
			updated_content = [new_title, new_body, new_category, new_tags]

			# Update position in db.
			DB.update_content_by_id('lp_articles', updated_content, this_article_id)
			return redirect('/post/{}'.format(this_article_id))
		else:
			DB.delete_art_by_id(this_article_id)
			return redirect('/blog')

	return render_template('update_article.html', UAF=UAF )


@app.route('/proj/<identifier>/update', methods=['GET', 'POST'])
def admin_update_proj_page(identifier):

	credentials = {'dbname':'lp_portfolio_articles', 'dbuser':'luke'}
	DB = PortfolioPageDB(credentials)

	projects = DB.get_projects()
	this_project_data = [a for a in projects if a[0] == int(identifier)][0]
	this_project_id = this_project_data[0]

	class UpdateProjectForm(FlaskForm):
		login = StringField('Login:', validators=[DataRequired()], default='a')
		password = StringField('Password:', validators=[DataRequired()], default='a')
		title_field = StringField('Project title:', validators=[DataRequired()], default=this_project_data[1])
		category_field =  StringField('Category:', validators=[DataRequired()], default=this_project_data[5])
		tags_field =  StringField('Tags:', validators=[DataRequired()], default=this_project_data[6])
		body_field = TextField('Project contents:', validators=[DataRequired()], default=this_project_data[4])

		submit_button = SubmitField('Update update.')
		delete_button = SubmitField('Delete post.')

	UAF = UpdateProjectForm()

	admin_login = 'a'
	admin_password = 'a'
	required = (admin_login, admin_password)
	current = (UAF.login.data, UAF.password.data)
	if current == required and request.method == 'POST':
		
		if not UAF.delete_button.data:
			# Update content data.
			new_title = UAF.title_field.data
			new_body = UAF.body_field.data
			new_category = UAF.category_field.data
			new_tags = UAF.tags_field.data
			updated_content = [new_title, new_body, new_category, new_tags]

			# Update position in db.
			DB.update_content_by_id('lp_projects', updated_content, this_project_id)
			return redirect('/proj/{}'.format(this_project_id))
		else:
			DB.delete_proj_by_id(this_project_id)
			return redirect('/portfolio')
			
	return render_template('update_project.html', UAF=UAF )

if __name__ == "__main__":
	app.run()