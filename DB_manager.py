import psycopg2

class PortfolioPageDB():

	def __init__(self, credentials):
		self.dbname = credentials['dbname']
		self.dbuser = credentials['dbuser']



	def create_lp_articles_table(self):
		table_name = 'lp_articles'
		columns_types = [ ('id', 'serial PRIMARY KEY'), ('title', 'text'),  ('author', 'text' ), ('publish_date', 'timestamp'), ('body', 'text'), ('category','text'), ('tags','text') ]
		columns_types = ', '.join( [ '"{}" {}'.format(tc[0], tc[1]) for tc in columns_types])
		command = 'CREATE TABLE IF NOT EXISTS {} ( {} );'.format(table_name,columns_types)
		self.db_do( command)

	def create_lp_projects_table(self):
		table_name = 'lp_projects'
		columns_types = [ ('id', 'serial PRIMARY KEY'), ('title', 'text'),  ('author', 'text' ), ('publish_date', 'timestamp'), ('body', 'text'), ('category','text'), ('tags','text') ]
		columns_types = ', '.join( [ '"{}" {}'.format(tc[0], tc[1]) for tc in columns_types])
		command = 'CREATE TABLE IF NOT EXISTS {} ( {} );'.format(table_name,columns_types)
		self.db_do( command)


	def db_do(self, command):
		try:
			self.conn = psycopg2.connect('dbname={} user={}'.format(self.dbname, self.dbuser))
			self.cur = self.conn.cursor()
			self.cur.execute(command)
			self.conn.commit()
			self.conn.close()
			self.cur.close()
		except Exception as e:
			print(e)


	# Executes command.
	def db_fetch(self, command):
		try:
			self.conn = psycopg2.connect('dbname={} user={}'.format(self.dbname, self.dbuser))
			self.cur = self.conn.cursor()
			self.cur.execute(command)
			result = self.cur.fetchall()
			self.conn.close()
			self.cur.close()
			return result
		except Exception as e:
			print(e)
			return []

	def delete_art_by_id(self, content_id):
		command = '''DELETE FROM lp_articles WHERE id='{}';'''.format(content_id)
		self.db_do(command)
	def delete_proj_by_id(self,content_id):
		command = '''DELETE FROM lp_projects WHERE id='{}';'''.format(content_id)
		self.db_do(command)


	def get_column_values(self, column_name, table_name):
		command =  '''SELECT {} from {} Order By publish_date DESC;'''.format(column_name, table_name)
		existing_articles = self.db_fetch(command)
		return existing_articles

	def get_articles(self):
		command =  '''SELECT * from lp_articles Order By publish_date DESC;'''
		existing_articles = self.db_fetch(command)
		return existing_articles

	def get_projects(self):
		command =  '''SELECT * from lp_projects Order By publish_date DESC;'''
		existing_articles = self.db_fetch(command)
		return existing_articles


	def update_content_by_id(self, table_name, updated_content, content_id):
		updates = '''title='{}', body='{}', category='{}', tags='{}' '''.format(*updated_content)
		command	= '''UPDATE {} SET {} where id={};'''
		command = command.format(table_name, updates, content_id)
		self.db_do(command)


	def db_get_top_id(self):
		try:
			command =  '''SELECT "id" from lp_articles;'''
			existing_ids = self.db_fetch(command)
			max_id = max([d[0] for d in existing_ids])
			return max_id
		except Exception as e:
			print(e)
			return 0

	def db_get_top_project_id(self):
		try:
			command =  '''SELECT "id" from lp_projects;'''
			existing_ids = self.db_fetch(command)
			max_id = max([d[0] for d in existing_ids])
			return max_id
		except Exception as e:
			print(e)
			return 0

	def get_article_titles(self):
		command = '''SELECT "title" from lp_articles;'''
		existing_titles = self.db_fetch(command)
		existing_titles = [t[0] for t in existing_titles]
		return existing_titles
		
	def get_projects_titles(self):
		command = '''SELECT "title" from lp_projects;'''
		existing_titles = self.db_fetch(command)
		existing_titles = [t[0] for t in existing_titles]
		return existing_titles

	def add_article_to_lp_articles(self, article_data_list):
		self.create_lp_articles_table()

		table_name = 'lp_articles'
		columns = ['id', 'title', 'author', 'publish_date', 'body', 'category', 'tags']
		columns = ', '.join([ '"{}"'.format(col) for col in columns]) # set_name, keyword
		values  = ', '.join(["'{}'".format(v) for v in article_data_list])
		command = 'INSERT INTO {} ( {}) VALUES ( {});'.format(table_name, columns, values)
		self.db_do(command)

	def add_project_to_lp_projects(self, project_data_list):
		self.create_lp_projects_table()

		table_name = 'lp_projects'
		columns = ['id', 'title', 'author', 'publish_date', 'body', 'category', 'tags']
		columns = ', '.join([ '"{}"'.format(col) for col in columns]) # set_name, keyword
		values  = ', '.join(["'{}'".format(v) for v in project_data_list])
		command = 'INSERT INTO {} ( {}) VALUES ( {});'.format(table_name, columns, values)
		self.db_do(command)

# credentials = {'dbname':'lp_portfolio_articles', 'dbuser':'luke'}
# PADB = PageArticlesDB(credentials)
# PADB.create_db()