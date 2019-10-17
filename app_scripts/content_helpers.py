import datetime

def post_intro_html(post_data, intro_body_size=300):

	intro_html = ''
	text_template = '''<p>{}</p>'''

	title ='''<h3><a href="/post/{}">{}</a></h3>'''.format(post_data[0], post_data[1]) # TITLE
	publish_date = None
	author = 'Constant'

	intro_html += title

	code = False
	body = post_data[4].split('\n')
	for post_line in body:
		if post_line.startswith('[CODE]'):
			code = True
		if post_line.startswith('[/CODE]'):
			code = False

		if post_line.startswith('[SUBT]') and len(intro_html) < intro_body_size:
			intro_html += text_template.format( post_line[7:].strip() )

		elif not post_line.startswith('[') and len(intro_html) < intro_body_size and code is False:
			intro_html += text_template.format( post_line.strip() )

	return intro_html

def proj_intro_html(proj_data, intro_body_size=100000):

	intro_html = ''
	text_template = '''<p>{}</p>'''

	title_template ='''<h3><a href="/proj/{}">{}</a></h3>''' # TITLE
	link_template ='''<a href="{}">{}</a>'''
	publish_date = None

	intro_html += title_template.format(proj_data[0], proj_data[1])
	
	code = False
	body = proj_data[4].split('\n')
	for post_line in body:
		if post_line.startswith('[CODE]'):
			code = True
		if post_line.startswith('[/CODE]'):
			code = False

		if post_line.startswith('[SUBT]') and len(intro_html) < intro_body_size:
			intro_html += text_template.format( post_line[7:].strip() )
		
		if post_line.startswith('[LINK'):
			link = post_line.split(']')[1].strip()
			descr = '[{}]'.format(' '.join(post_line.split(']')[0].strip().split('_')[1:]).lower())
			intro_html += link_template.format(link, descr)

		if post_line.startswith('[nLINK'):
			link = post_line.split(']')[1].strip()
			descr = '[{}]'.format(' '.join(post_line.split(']')[0].strip().split('_')[1:]).lower())
			intro_html += link_template.format(link, descr) + '<br>'

		elif not post_line.startswith('[') and len(intro_html) < intro_body_size and code is False:
			intro_html += text_template.format( post_line.strip() )


	return intro_html

def article_to_html(post_data, this_article_id):
	article_html = ''
	article_html += '''<h2>{}</h2>'''.format(post_data[1]) # TITLE
	publish_date = None
	author = 'Constant'
	sub_title_template = '<h4>{}</h4>'
	image_template = '''<img src="{}" width="800" height="600" alt="Image">'''
	code_template = '''<figure><pre><code contenteditable spellcheck="false">{}</code></pre></figure>'''
	text_template = '''<p>{}</p>'''
	intro_link_to_article = ''
	link_template ='''<a href="{}">{}</a>'''
	code = False
	code_block = []
	for post_line in post_data[4].split('\n'):

		if post_line.startswith('[SUBT]'):
			sub_title = sub_title_template.format( post_line[7:].strip() )
			article_html += sub_title

		elif post_line.startswith('[IMG]'):
			image_html = image_template.format( post_line[6:].strip() )
			article_html += image_html

		elif post_line.startswith('[LINK'):
			link = post_line.split(']')[1].strip()
			descr = '[{}]'.format(' '.join(post_line.split(']')[0].strip().split('_')[1:]).lower())
			article_html += link_template.format(link, descr)

		elif post_line.startswith('[nLINK'):
			link = post_line.split(']')[1].strip()
			descr = '[{}]'.format(' '.join(post_line.split(']')[0].strip().split('_')[1:]).lower())
			article_html += link_template.format(link, descr) + '<br>'

		elif post_line.startswith('[CODE]'):
			code = True
		elif post_line.startswith('[/CODE]'):
			article_html += code_template.format( '\n'.join(code_block) ) # test
			code = False
			code_block = []
		elif code is True:
			code_block.append( post_line  )

		elif code is False:
			text_paragraph = text_template.format( post_line.strip() )
			article_html += text_paragraph

	article_html += '''<br><br><p><a href="/post/{}/update">{}</a></p>'''.format(post_data[0], 'Update article')
	return article_html

def project_to_html(post_data, this_article_id):
	proj_html = ''
	proj_html += '''<h2>{}</h2>'''.format(post_data[1]) # TITLE
	publish_date = None
	author = 'Constant'
	sub_title_template = '<h4>{}</h4>'
	image_template = '''<img src="{}" width="800" height="600" alt="Image">'''
	code_template = '''<figure><pre><code contenteditable spellcheck="false">{}</code></pre></figure>'''
	text_template = '''<p>{}</p>'''
	link_template ='''<a href="{}">{}</a>'''
	intro_link_to_article = ''

	# <iframe src=”https://codepen.io/champlainelearning/embed/nmJud?default-tab=html&amp;line-numbers=true&amp;height=350” width=”100%” height=”350px”></iframe>
	# https://websemantics.uk/articles/displaying-code-in-web-pages/

	code = False
	code_block = []
	for post_line in post_data[4].split('\n'):

		if post_line.startswith('[SUBT]'):
			sub_title = sub_title_template.format( post_line[7:].strip() )
			proj_html += sub_title

		elif post_line.startswith('[IMG]'):
			image_html = image_template.format( post_line[6:].strip() )
			proj_html += image_html

		elif post_line.startswith('[LINK'):
			link = post_line.split(']')[1].strip()
			descr = '[{}]'.format(' '.join(post_line.split(']')[0].strip().split('_')[1:]).lower())
			proj_html += link_template.format(link, descr)

		elif post_line.startswith('[nLINK'):
			link = post_line.split(']')[1].strip()
			descr = '[{}]'.format(' '.join(post_line.split(']')[0].strip().split('_')[1:]).lower())
			proj_html += link_template.format(link, descr) + '<br>'

		elif post_line.startswith('[CODE]'):
			code = True
		elif post_line.startswith('[/CODE]'):
			proj_html += code_template.format( '\n'.join(code_block) ) # test
			code = False
			code_block = []
		elif code is True:
			code_block.append( post_line  )

		elif code is False:
			text_paragraph = text_template.format( post_line.strip() )
			proj_html += text_paragraph

	proj_html += '''<br><br><p><a href="/proj/{}/update">{}</a></p>'''.format(post_data[0], 'Update project')

	return proj_html

def create_page_nav(nav_type, page_num, max_page):
	nav_template = ''
	nav_item_template = '''<a href="/{}/{}">{}</a>''' # .format('nav_type', p1', 'Page 1')
	prev = page_num-1 if page_num > 0 else 0
	prev_nr = 'p' + str(prev)
	next_nr = page_num+1 if page_num < max_page else max_page
	next_nr = 'p' + str(next_nr)

	# REWRITE TO 5 page tags
	n = 'p{}'.format(page_num)
	name = '   Page {}   '.format(page_num)

	this_p = nav_item_template.format(nav_type, n, name)
	
	prev_page = nav_item_template.format(nav_type, prev_nr, '<<')
	first_page = nav_item_template.format(nav_type, 'p0', 'Freshest')
	last_page = nav_item_template.format(nav_type, 'p{}'.format(max_page), 'Oldest')
	next_page = nav_item_template.format(nav_type, next_nr, '>>')

	nav_template = '    '.join([first_page, prev_page, this_p, next_page, last_page])
	return nav_template